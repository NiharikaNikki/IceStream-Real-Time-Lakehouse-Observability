from datetime import datetime, timezone


class IncidentLogger:
    def __init__(self):
        self.incidents = []

    def create_incident(
        self,
        incident_type,
        message,
        severity="CRITICAL",
        error_rate=0.0,
        dlq_count=0,
        circuit_state="OPEN",
    ):
        incident = {
            "incident_id": f"INC-{len(self.incidents) + 1:04d}",
            "incident_type": incident_type,
            "message": message,
            "severity": severity,
            "error_rate": error_rate,
            "dlq_count": dlq_count,
            "circuit_state": circuit_state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.incidents.append(incident)

        return incident

    def get_incidents(self):
        return self.incidents

    def count(self):
        return len(self.incidents)

    def clear(self):
        self.incidents.clear()