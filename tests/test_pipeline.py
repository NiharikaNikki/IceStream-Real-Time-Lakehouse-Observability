from quality.validator import validate_event
from quality.circuit_breaker import CircuitBreaker
from quality.dlq import DeadLetterQueue
from backend.incidents import IncidentLogger


def create_valid_event(transaction_id="TXN-TEST-001"):
    return {
        "transaction_id": transaction_id,
        "customer_id": "CUST-1001",
        "amount": 1000.0,
        "tax_amount": 180.0,
        "currency": "INR",
        "payment_method": "UPI",
        "timestamp": "2026-09-24T10:00:00+00:00",
    }


def create_invalid_event(transaction_id="TXN-BAD-001"):
    return {
        "transaction_id": transaction_id,
        "customer_id": None,
        "amount": -500.0,
        "tax_amount": None,
        "currency": "INR",
        "payment_method": "CARD",
        "timestamp": "2026-09-24T10:00:00+00:00",
    }


def test_end_to_end_pipeline():
    circuit = CircuitBreaker(threshold=2.0)
    dlq = DeadLetterQueue()
    incidents = IncidentLogger()

    # Normal traffic
    for i in range(98):
        event = create_valid_event(f"TXN-GOOD-{i:03d}")

        is_valid, reason = validate_event(event)

        assert is_valid is True

        circuit.record_valid()

    # Bad traffic
    for i in range(3):
        event = create_invalid_event(f"TXN-BAD-{i:03d}")

        is_valid, reason = validate_event(event)

        assert is_valid is False

        dlq.quarantine(
            event,
            reason=reason,
            error_type="DATA_QUALITY",
        )

        circuit.record_invalid()

    # Circuit should open
    assert circuit.is_open() is True

    # DLQ should contain bad records
    assert dlq.count() == 3

    # Incident should be created
    incident = incidents.create_incident(
        incident_type="CIRCUIT_OPEN",
        message="Error rate exceeded 2%",
        severity="CRITICAL",
        error_rate=circuit.error_rate(),
        dlq_count=dlq.count(),
        circuit_state=circuit.state,
    )

    assert incident["circuit_state"] == "OPEN"
    assert incident["dlq_count"] == 3
    assert incident["error_rate"] > 2.0