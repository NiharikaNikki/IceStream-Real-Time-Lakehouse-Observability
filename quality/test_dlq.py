from quality.dlq import DeadLetterQueue


def valid_event():
    return {
        "transaction_id": "TXN-001",
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-16T10:00:00+00:00",
    }


def test_dlq_quarantine():
    dlq = DeadLetterQueue()

    event = valid_event()
    event["customer_id"] = None

    record = dlq.quarantine(
        event,
        "customer_id is null",
        "NULL_VALUE",
    )

    assert dlq.count() == 1
    assert record["original_event"]["transaction_id"] == "TXN-001"
    assert record["reason"] == "customer_id is null"
    assert record["error_type"] == "NULL_VALUE"
    assert record["pipeline"] == "IceStream"
    assert "timestamp" in record


def test_dlq_multiple_records():
    dlq = DeadLetterQueue()

    event1 = valid_event()
    event1["customer_id"] = None

    event2 = valid_event()
    event2["amount"] = -500

    event3 = valid_event()
    event3["tax_amount"] = None

    dlq.quarantine(
        event1,
        "customer_id is null",
        "NULL_VALUE",
    )

    dlq.quarantine(
        event2,
        "amount must be greater than 0",
        "INVALID_AMOUNT",
    )

    dlq.quarantine(
        event3,
        "tax_amount is null",
        "NULL_VALUE",
    )

    assert dlq.count() == 3

    records = dlq.get_records()

    assert len(records) == 3
    assert records[0]["error_type"] == "NULL_VALUE"
    assert records[1]["error_type"] == "INVALID_AMOUNT"
    assert records[2]["error_type"] == "NULL_VALUE"


def test_dlq_summary():
    dlq = DeadLetterQueue()

    event = valid_event()

    dlq.quarantine(
        event,
        "Test quarantine",
        "TEST_ERROR",
    )

    summary = dlq.summary()

    assert summary["pipeline"] == "IceStream"
    assert summary["dlq_count"] == 1