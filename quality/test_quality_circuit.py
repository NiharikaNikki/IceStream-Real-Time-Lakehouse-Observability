from quality.validator import validate_event
from quality.circuit_breaker import CircuitBreaker


def base_event(transaction_id="TXN-001"):
    return {
        "transaction_id": transaction_id,
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-15T10:00:00+00:00",
    }


def process_event(event, breaker):
    is_valid, reason = validate_event(event)

    if is_valid:
        breaker.record_valid()
        status = "VALID"
    else:
        breaker.record_invalid()
        status = "INVALID"

    return status, reason


def test_quality_circuit_opens_above_threshold():
    breaker = CircuitBreaker(threshold=2.0)

    # 98 valid records
    for i in range(98):
        event = base_event(f"TXN-{i:06d}")
        status, reason = process_event(event, breaker)

        assert status == "VALID"
        assert reason == "VALID"

    # 3 invalid records
    for i in range(3):
        event = base_event(f"BAD-{i:06d}")
        event["amount"] = -100

        status, reason = process_event(event, breaker)

        assert status == "INVALID"
        assert "amount" in reason

    assert breaker.total_records == 101
    assert breaker.invalid_records == 3
    assert breaker.error_rate() > 2.0
    assert breaker.state == breaker.OPEN
    assert breaker.is_open() is True


def test_quality_circuit_stays_closed_at_threshold():
    breaker = CircuitBreaker(threshold=2.0)

    for i in range(98):
        event = base_event(f"TXN-{i:06d}")
        process_event(event, breaker)

    for i in range(2):
        event = base_event(f"BAD-{i:06d}")
        event["amount"] = -100
        process_event(event, breaker)

    assert breaker.total_records == 100
    assert breaker.invalid_records == 2
    assert breaker.error_rate() == 2.0
    assert breaker.state == breaker.CLOSED
    assert breaker.is_open() is False