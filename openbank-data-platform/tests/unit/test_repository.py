from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.transform.app.models import Base, RawTransaction, CuratedTransaction


def test_repository_insert_and_query() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    raw = RawTransaction(
        transaction_id="tx_1",
        account_id="acc_1",
        transaction_timestamp=datetime.utcnow(),
        amount=100.0,
        currency="SEK",
        merchant="ICA",
        merchant_category="Grocery",
        country="SE",
        payment_method="Card",
        channel="POS",
        status="COMPLETED",
    )
    curated = CuratedTransaction(
        transaction_id="tx_1",
        account_id="acc_1",
        transaction_timestamp=datetime.utcnow(),
        amount=100.0,
        currency="SEK",
        merchant="ICA",
        country="SE",
        risk_flag=False,
        risk_reason=None,
    )
    session.add(raw)
    session.add(curated)
    session.commit()

    assert session.query(RawTransaction).count() == 1
    assert session.query(CuratedTransaction).count() == 1
