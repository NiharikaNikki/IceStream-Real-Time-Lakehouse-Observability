class CircuitBreaker:
    CLOSED = "CLOSED"
    OPEN = "OPEN"

    def __init__(self, threshold=2.0):
        self.threshold = threshold
        self.state = self.CLOSED
        self.total_records = 0
        self.invalid_records = 0

    def record_valid(self):
        self.total_records += 1
        self._evaluate()

    def record_invalid(self):
        self.total_records += 1
        self.invalid_records += 1
        self._evaluate()

    def error_rate(self):
        if self.total_records == 0:
            return 0.0

        return (self.invalid_records / self.total_records) * 100

    def _evaluate(self):
        if self.error_rate() > self.threshold:
            self.state = self.OPEN
        else:
            self.state = self.CLOSED

    def is_open(self):
        return self.state == self.OPEN

    def reset(self):
        self.total_records = 0
        self.invalid_records = 0
        self.state = self.CLOSED

    def status(self):
        return {
            "state": self.state,
            "total_records": self.total_records,
            "invalid_records": self.invalid_records,
            "error_rate": round(self.error_rate(), 2),
            "threshold": self.threshold,
        }