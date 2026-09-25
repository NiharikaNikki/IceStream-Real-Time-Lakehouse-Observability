from quality.schema_detector import detect_schema_drift


def valid_event():
    return {
        "transaction_id": "TXN-001",
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-11T10:00:00+00:00",
    }


def test_valid_schema():
    result = detect_schema_drift(valid_event())

    assert result["is_drift"] is False
    assert result["missing_fields"] == []
    assert result["extra_fields"] == []
    assert result["reason"] == "Schema matches expected schema"


def test_extra_field_schema_drift():
    event = valid_event()
    event["discount_code"] = "NEW10"

    result = detect_schema_drift(event)

    assert result["is_drift"] is True
    assert result["missing_fields"] == []
    assert "discount_code" in result["extra_fields"]
    assert result["reason"] == "Schema drift detected"


def test_missing_field_schema_drift():
    event = valid_event()
    del event["tax_amount"]

    result = detect_schema_drift(event)

    assert result["is_drift"] is True
    assert "tax_amount" in result["missing_fields"]
    assert result["extra_fields"] == []
    assert result["reason"] == "Schema drift detected"