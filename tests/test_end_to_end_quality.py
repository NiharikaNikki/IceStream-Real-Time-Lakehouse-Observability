from quality.validator import validate_event


def valid_event():
    return {
        "transaction_id": "TXN-001",
        "customer_id": "CUST-001",
        "amount": 1000.0,
        "tax_amount": 180.0,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-24T10:00:00+00:00",
    }


def test_valid_event():
    is_valid, reason = validate_event(valid_event())

    assert is_valid is True
    assert reason == "VALID"


def test_null_customer():
    event = valid_event()
    event["customer_id"] = None

    is_valid, reason = validate_event(event)

    assert is_valid is False
    assert "customer_id" in reason


def test_negative_amount():
    event = valid_event()
    event["amount"] = -100

    is_valid, reason = validate_event(event)

    assert is_valid is False
    assert "amount" in reason


def test_null_tax():
    event = valid_event()
    event["tax_amount"] = None

    is_valid, reason = validate_event(event)

    assert is_valid is False
    assert "tax_amount" in reason


def test_schema_drift():
    event = valid_event()
    event["discount_code"] = "NEW10"

    is_valid, reason = validate_event(event)

    assert is_valid is False
    assert "unexpected fields" in reason