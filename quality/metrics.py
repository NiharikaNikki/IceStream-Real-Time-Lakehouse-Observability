class QualityMetrics:
    def __init__(self):
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0

    def record_valid(self):
        self.total_records += 1
        self.valid_records += 1

    def record_invalid(self):
        self.total_records += 1
        self.invalid_records += 1

    def error_rate(self):
        if self.total_records == 0:
            return 0.0

        return (self.invalid_records / self.total_records) * 100

    def summary(self):
        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "error_rate": round(self.error_rate(), 2),
        }