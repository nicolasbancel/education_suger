import os
import requests
import pandas as pd
from datetime import datetime, timezone

BASE_URL = "https://api.openai.com/v1"


def _auth_headers() -> dict:
    api_key = os.environ["OPENAI_API_KEY"]
    return {"Authorization": f"Bearer {api_key}"}


def fetch_completions_usage(date_from: str, date_to: str) -> pd.DataFrame:
    """
    date_from / date_to: YYYY-MM-DD
    Retour: DataFrame avec colonnes (date, model, input_tokens, output_tokens, total_tokens)
    """
    url = f"{BASE_URL}/organization/usage/completions"
    params = {
        "start_date": date_from,
        "end_date": date_to,
        "bucket_width": "1d",  # buckets journaliers (selon API)
    }
    r = requests.get(url, headers=_auth_headers(), params=params, timeout=60)
    r.raise_for_status()
    data = r.json()

    rows = []
    # La forme exacte peut évoluer; on parse défensivement
    for bucket in data.get("data", []):
        day = bucket.get("start_time") or bucket.get("date") or bucket.get("start_date")
        # Normalisation date
        if isinstance(day, (int, float)):
            day = datetime.fromtimestamp(day, tz=timezone.utc).date().isoformat()
        elif isinstance(day, str) and "T" in day:
            day = day.split("T", 1)[0]

        for item in bucket.get("results", bucket.get("data", [])) or []:
            model = item.get("model", "unknown")
            in_tok = int(item.get("input_tokens", item.get("prompt_tokens", 0)) or 0)
            out_tok = int(
                item.get("output_tokens", item.get("completion_tokens", 0)) or 0
            )
            rows.append(
                {
                    "date": day,
                    "model": model,
                    "input_tokens": in_tok,
                    "output_tokens": out_tok,
                    "total_tokens": in_tok + out_tok,
                }
            )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.groupby(["date", "model"], as_index=False)[
            ["input_tokens", "output_tokens", "total_tokens"]
        ].sum()
    return df
