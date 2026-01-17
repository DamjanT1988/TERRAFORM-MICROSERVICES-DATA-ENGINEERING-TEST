import pandera as pa
from pandera import Column, DataFrameSchema, Check


transaction_schema = DataFrameSchema(
    {
        "transaction_id": Column(str, nullable=False),
        "account_id": Column(str, nullable=False),
        "transaction_timestamp": Column(pa.DateTime, nullable=False),
        "amount": Column(float, nullable=False),
        "currency": Column(str, Check.str_length(3, 3)),
        "merchant": Column(str, nullable=False),
        "merchant_category": Column(str, nullable=True),
        "country": Column(str, Check.str_length(2, 2)),
        "payment_method": Column(str, nullable=True),
        "channel": Column(str, nullable=True),
        "status": Column(str, nullable=True),
    },
    coerce=True,
)
