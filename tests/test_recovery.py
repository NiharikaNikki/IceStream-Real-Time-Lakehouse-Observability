from quality.circuit_breaker import CircuitBreaker


def test_circuit_recovery():
    circuit = CircuitBreaker(threshold=2.0)

    # Healthy traffic
    for _ in range(98):
        circuit.record_valid()

    assert circuit.state == circuit.CLOSED

    # Bad traffic
    for _ in range(3):
        circuit.record_invalid()

    assert circuit.state == circuit.OPEN
    assert circuit.error_rate() > 2.0

    # Recovery
    circuit.reset()

    assert circuit.state == circuit.CLOSED
    assert circuit.error_rate() == 0.0
    assert circuit.total_records == 0
    assert circuit.invalid_records == 0