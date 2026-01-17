from services.transform.app.risk import assess_risk


def test_assess_risk_flags_high_value_and_country() -> None:
    risk_flag, reason = assess_risk(50000.0, "RU", "Some Merchant")
    assert risk_flag is True
    assert "high_value_amount" in reason
    assert "high_risk_country" in reason


def test_assess_risk_no_flags() -> None:
    risk_flag, reason = assess_risk(50.0, "SE", "ICA")
    assert risk_flag is False
    assert reason is None
