from quality.metrics import QualityMetrics


def test_quality_metrics():
    metrics = QualityMetrics()

    metrics.record_valid()
    metrics.record_valid()
    metrics.record_valid()

    metrics.record_invalid()
    metrics.record_invalid()

    assert metrics.total_records == 5
    assert metrics.valid_records == 3
    assert metrics.invalid_records == 2
    assert metrics.error_rate() == 40.0


def test_empty_metrics():
    metrics = QualityMetrics()

    assert metrics.total_records == 0
    assert metrics.valid_records == 0
    assert metrics.invalid_records == 0
    assert metrics.error_rate() == 0.0


def test_metrics_summary():
    metrics = QualityMetrics()

    metrics.record_valid()
    metrics.record_invalid()

    summary = metrics.summary()

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["invalid_records"] == 1
    assert summary["error_rate"] == 50.0