from dataclasses import dataclass


@dataclass(frozen=True)
class CarbonResult:
    kwh: float
    gco2e: float


def estimate_energy_kwh(
    tokens_total: int, wh_per_1k_tokens: float, wh_fixed_per_request: float = 0.0
) -> float:
    wh = wh_fixed_per_request + (tokens_total / 1000.0) * wh_per_1k_tokens
    return wh / 1000.0  # Wh -> kWh


def estimate_carbon(
    tokens_total: int,
    carbon_intensity_g_per_kwh: float,
    wh_per_1k_tokens: float,
    wh_fixed_per_request: float = 0.0,
) -> CarbonResult:
    kwh = estimate_energy_kwh(tokens_total, wh_per_1k_tokens, wh_fixed_per_request)
    gco2e = kwh * carbon_intensity_g_per_kwh
    return CarbonResult(kwh=kwh, gco2e=gco2e)
