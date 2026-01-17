from typing import Tuple


HIGH_RISK_COUNTRIES = {"RU", "NG", "UA", "MT"}
HIGH_VALUE_THRESHOLD = 10000.0


def assess_risk(amount: float, country: str, merchant: str) -> Tuple[bool, str | None]:
    reasons: list[str] = []
    if abs(amount) >= HIGH_VALUE_THRESHOLD:
        reasons.append("high_value_amount")
    if country.upper() in HIGH_RISK_COUNTRIES:
        reasons.append("high_risk_country")
    if "unknown" in merchant.lower():
        reasons.append("unknown_merchant")

    if reasons:
        return True, ",".join(reasons)
    return False, None
