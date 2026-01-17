import pandas as pd

from services.transform.app.validation import transaction_schema


def test_validation_accepts_valid_rows() -> None:
    df = pd.DataFrame(
        [
            {
                "transaction_id": "tx_1",
                "account_id": "acc_1",
                "transaction_timestamp": "2024-01-01T10:00:00",
                "amount": 100.0,
                "currency": "SEK",
                "merchant": "ICA",
                "merchant_category": "Grocery",
                "country": "SE",
                "payment_method": "Card",
                "channel": "POS",
                "status": "COMPLETED",
            }
        ]
    )
    validated = transaction_schema.validate(df)
    assert len(validated) == 1
