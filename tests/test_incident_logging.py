from backend.incidents import IncidentLogger


def test_create_incident():
    logger = IncidentLogger()

    incident = logger.create_incident(
        incident_type="CIRCUIT_OPEN",
        message="Error rate exceeded 2%",
        severity="CRITICAL",
        error_rate=3.25,
        dlq_count=5,
        circuit_state="OPEN",
    )

    assert incident["incident_id"] == "INC-0001"
    assert incident["incident_type"] == "CIRCUIT_OPEN"
    assert incident["severity"] == "CRITICAL"
    assert incident["error_rate"] == 3.25
    assert incident["dlq_count"] == 5
    assert incident["circuit_state"] == "OPEN"


def test_incident_count():
    logger = IncidentLogger()

    logger.create_incident(
        incident_type="CIRCUIT_OPEN",
        message="Test incident",
    )

    logger.create_incident(
        incident_type="RECOVERY",
        message="Pipeline recovered",
        severity="INFO",
        circuit_state="CLOSED",
    )

    assert logger.count() == 2