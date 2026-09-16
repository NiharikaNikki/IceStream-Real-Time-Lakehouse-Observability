from datetime import datetime, timezone


class DeadLetterQueue:
    def __init__(self, pipeline="IceStream"):
        self.pipeline = pipeline
        self.records = []

    def quarantine(self, event, reason, error_type="DATA_QUALITY"):
        record = {
            "original_event": event,
            "reason": reason,
            "error_type": error_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline": self.pipeline,
        }

        self.records.append(record)

        return record

    def count(self):
        return len(self.records)

    def get_records(self):
        return self.records

    def summary(self):
        return {
            "pipeline": self.pipeline,
            "dlq_count": self.count(),
        }