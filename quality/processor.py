from .validator import validate_event
from .metrics import QualityMetrics


class QualityProcessor:
    def __init__(self):
        self.metrics = QualityMetrics()

    def process(self, event):
        is_valid, reason = validate_event(event)

        if is_valid:
            self.metrics.record_valid()
            status = "VALID"
        else:
            self.metrics.record_invalid()
            status = "INVALID"

        return {
            "event": event,
            "status": status,
            "reason": reason,
        }

    def get_metrics(self):
        return self.metrics.summary()