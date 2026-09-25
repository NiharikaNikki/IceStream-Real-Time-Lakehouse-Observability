from quality.processor import QualityProcessor


def valid_event(transaction_id="TXN-001"):
    return {
        "transaction_id": transaction_id,
        "customer_id": "CUST-001",
        "amount": 1000,
        "tax_amount": 180,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-10T10:00:00+00:00",
    }


def test_processor_valid_event():
    processor = QualityProcessor()

    result = processor.process(valid_event())

    assert result["status"] == "VALID"
    assert result["reason"] == "VALID"


def test_processor_invalid_customer():
    processor = QualityProcessor()

    event = valid_event("TXN-002")
    event["customer_id"] = None

    result = processor.process(event)

    assert result["status"] == "INVALID"
    assert "customer_id" in result["reason"]


def test_processor_negative_amount():
    processor = QualityProcessor()

    event = valid_event("TXN-003")
    event["amount"] = -500

    result = processor.process(event)

    assert result["status"] == "INVALID"
    assert "amount" in result["reason"]


def test_processor_metrics():
    processor = QualityProcessor()

    valid = valid_event("TXN-001")

    invalid_customer = valid_event("TXN-002")
    invalid_customer["customer_id"] = None

    invalid_amount = valid_event("TXN-003")
    invalid_amount["amount"] = -500

    processor.process(valid)
    processor.process(invalid_customer)
    processor.process(invalid_amount)

    metrics = processor.get_metrics()

    assert metrics["total_records"] == 3
    assert metrics["valid_records"] == 1
    assert metrics["invalid_records"] == 2
    assert metrics["error_rate"] == round((2 / 3) * 100, 2)