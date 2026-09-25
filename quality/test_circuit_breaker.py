from quality.circuit_breaker import CircuitBreaker


def test_circuit_stays_closed_at_2_percent():
    breaker = CircuitBreaker(threshold=2.0)

    # 98 valid + 2 invalid = exactly 2%
    for _ in range(98):
        breaker.record_valid()

    for _ in range(2):
        breaker.record_invalid()

    assert breaker.error_rate() == 2.0
    assert breaker.state == breaker.CLOSED
    assert breaker.is_open() is False


def test_circuit_opens_above_2_percent():
    breaker = CircuitBreaker(threshold=2.0)

    # 98 valid + 3 invalid = 2.97%
    for _ in range(98):
        breaker.record_valid()

    for _ in range(3):
        breaker.record_invalid()

    assert breaker.error_rate() > 2.0
    assert breaker.state == breaker.OPEN
    assert breaker.is_open() is True


def test_circuit_reset():
    breaker = CircuitBreaker(threshold=2.0)

    for _ in range(98):
        breaker.record_valid()

    for _ in range(3):
        breaker.record_invalid()

    assert breaker.is_open() is True

    breaker.reset()

    assert breaker.state == breaker.CLOSED
    assert breaker.is_open() is False
    assert breaker.total_records == 0
    assert breaker.invalid_records == 0
    assert breaker.error_rate() == 0.0