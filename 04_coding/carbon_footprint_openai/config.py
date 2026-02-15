from dataclasses import dataclass
import os


@dataclass(frozen=True)
class CarbonConfig:
    # intensité carbone électricité (gCO2e/kWh)
    # -> mets une valeur par défaut (ex: 50), mais idéalement tu renseignes ta valeur
    carbon_intensity_g_per_kwh: float = float(
        os.getenv("CARBON_INTENSITY_G_PER_KWH", "50")
    )

    # Estimation d'énergie par 1k tokens (Wh / 1k tokens) -> très incertain, à calibrer
    # Mets une valeur conservative et ajuste après.
    wh_per_1k_tokens: float = float(os.getenv("WH_PER_1K_TOKENS", "1.0"))

    # coût fixe par requête (Wh) optionnel
    wh_fixed_per_request: float = float(os.getenv("WH_FIXED_PER_REQUEST", "0.0"))
