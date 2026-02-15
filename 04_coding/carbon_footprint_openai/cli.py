from pathlib import Path
import pandas as pd
import typer

from chatgpt_carbon.config import CarbonConfig
from chatgpt_carbon.carbon import estimate_carbon
from chatgpt_carbon.sources.openai_usage_api import fetch_completions_usage
from chatgpt_carbon.sources.chatgpt_export import iter_messages_from_export_zip
from chatgpt_carbon.tokens import count_tokens_tiktoken

app = typer.Typer(no_args_is_help=True)


@app.command()
def api_usage(
    date_from: str, date_to: str, out_csv: Path = Path("outputs/daily_usage.csv")
):
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df = fetch_completions_usage(date_from, date_to)
    df.to_csv(out_csv, index=False)
    typer.echo(f"Écrit: {out_csv}")


@app.command()
def export_tokens(zip_path: Path, out_csv: Path = Path("outputs/export_tokens.csv")):
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    msgs = list(iter_messages_from_export_zip(zip_path))
    df = count_tokens_tiktoken(msgs)
    df.to_csv(out_csv, index=False)
    typer.echo(f"Écrit: {out_csv}")


@app.command()
def carbon_from_daily_usage(
    usage_csv: Path = Path("outputs/daily_usage.csv"),
    out_csv: Path = Path("outputs/daily_carbon.csv"),
):
    cfg = CarbonConfig()
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(usage_csv)
    if df.empty:
        raise typer.Exit(code=1)

    def row_carbon(tokens: int):
        res = estimate_carbon(
            tokens_total=int(tokens),
            carbon_intensity_g_per_kwh=cfg.carbon_intensity_g_per_kwh,
            wh_per_1k_tokens=cfg.wh_per_1k_tokens,
            wh_fixed_per_request=cfg.wh_fixed_per_request,
        )
        return res.kwh, res.gco2e

    kwh_list, g_list = [], []
    for t in df["total_tokens"].fillna(0).astype(int).tolist():
        kwh, g = row_carbon(t)
        kwh_list.append(kwh)
        g_list.append(g)

    df["kwh_est"] = kwh_list
    df["gco2e_est"] = g_list

    # Agrège par jour (tous modèles)
    daily = df.groupby("date", as_index=False)[
        ["total_tokens", "kwh_est", "gco2e_est"]
    ].sum()
    daily.to_csv(out_csv, index=False)

    # Extrapolation simple à l'année: moyenne journalière * 365
    mean_g = daily["gco2e_est"].mean()
    annual_g = mean_g * 365.0
    typer.echo(
        f"Moyenne: {mean_g:.2f} gCO2e/jour -> ~{annual_g/1000:.2f} kgCO2e/an (extrapolation)"
    )

    typer.echo(f"Écrit: {out_csv}")


if __name__ == "__main__":
    app()
