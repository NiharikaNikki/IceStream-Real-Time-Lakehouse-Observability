from quality.validator import validate_event
from quality.dlq import DeadLetterQueue


def valid_event(transaction_id="TXN-001"):
    return {
        "transaction_id": transaction_id,
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-16T10:00:00+00:00",
    }


def test_valid_events_not_sent_to_dlq():
    dlq = DeadLetterQueue()

    for i in range(3):
        event = valid_event(f"TXN-{i + 1:03d}")

        is_valid, reason = validate_event(event)

        assert is_valid is True
        assert reason == "VALID"

        # Valid records should not enter DLQ.
        assert dlq.count() == 0


def test_invalid_events_are_quarantined():
    dlq = DeadLetterQueue()

    # Invalid: null customer
    event1 = valid_event("BAD-001")
    event1["customer_id"] = None

    # Invalid: negative amount
    event2 = valid_event("BAD-002")
    event2["amount"] = -500

    # Invalid: schema drift
    event3 = valid_event("BAD-003")
    event3["discount_code"] = "NEW10"

    invalid_events = [event1, event2, event3]

    for event in invalid_events:
        is_valid, reason = validate_event(event)

        assert is_valid is False

        dlq.quarantine(
            event,
            reason,
            "DATA_QUALITY",
        )

    assert dlq.count() == 3


def test_quality_pipeline_summary():
    dlq = DeadLetterQueue()

    valid_count = 0
    invalid_count = 0

    events = []

    # 3 valid events
    for i in range(3):
        events.append(valid_event(f"TXN-{i + 1:03d}"))

    # 3 invalid events
    event = valid_event("BAD-001")
    event["customer_id"] = None
    events.append(event)

    event = valid_event("BAD-002")
    event["amount"] = -500
    events.append(event)

    event = valid_event("BAD-003")
    event["discount_code"] = "NEW10"
    events.append(event)

    for event in events:
        is_valid, reason = validate_event(event)

        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            dlq.quarantine(
                event,
                reason,
                "DATA_QUALITY",
            )

    assert len(events) == 6
    assert valid_count == 3
    assert invalid_count == 3
    assert dlq.count() == 3