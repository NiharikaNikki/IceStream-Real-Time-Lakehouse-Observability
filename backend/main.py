from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.websocket import router as websocket_router
from backend.websocket import broadcast_alert
from backend.incidents import IncidentLogger


# =========================================================
# INCIDENT LOGGER
# =========================================================

incident_logger = IncidentLogger()


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="IceStream Observability API",
    description="Real-time lakehouse observability backend",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# WEBSOCKET ROUTER
# =========================================================

app.include_router(websocket_router)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():
    return {
        "project": "IceStream",
        "service": "Observability API",
        "status": "running",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# =========================================================
# PIPELINE METRICS
# =========================================================

@app.get("/metrics")
def metrics():
    return {
        "total_records": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "error_rate": 0.0,
        "dlq_count": 0,
        "circuit_state": "CLOSED",
    }


# =========================================================
# DAY 12 - TEST CIRCUIT OPEN ALERT
# =========================================================

@app.post("/alerts/test")
async def test_alert():
    await broadcast_alert(
        alert_type="CIRCUIT_OPEN",
        message="Error rate exceeded 2%. Circuit breaker opened.",
        severity="CRITICAL",
        error_rate=3.25,
        dlq_count=5,
        circuit_state="OPEN",
    )

    return {
        "status": "alert_sent",
        "alert_type": "CIRCUIT_OPEN",
    }


# =========================================================
# DAY 12 - RECOVERY ALERT
# =========================================================

@app.post("/alerts/recovery")
async def recovery_alert():
    await broadcast_alert(
        alert_type="RECOVERY",
        message="Pipeline recovered. Circuit breaker closed.",
        severity="INFO",
        error_rate=0.5,
        dlq_count=0,
        circuit_state="CLOSED",
    )

    return {
        "status": "alert_sent",
        "alert_type": "RECOVERY",
    }


# =========================================================
# DAY 14 - GET INCIDENT HISTORY
# =========================================================

@app.get("/incidents")
def get_incidents():
    return {
        "count": incident_logger.count(),
        "incidents": incident_logger.get_incidents(),
    }


# =========================================================
# DAY 14 - CREATE TEST INCIDENT
# =========================================================

@app.post("/incidents/test")
async def create_test_incident():
    incident = incident_logger.create_incident(
        incident_type="CIRCUIT_OPEN",
        message="Error rate exceeded 2%. Pipeline automatically paused.",
        severity="CRITICAL",
        error_rate=3.25,
        dlq_count=5,
        circuit_state="OPEN",
    )

    return incident


# =========================================================
# DAY 14 - CREATE RECOVERY INCIDENT
# =========================================================

@app.post("/incidents/recovery")
async def create_recovery_incident():
    incident = incident_logger.create_incident(
        incident_type="RECOVERY",
        message="Pipeline recovered and circuit breaker returned to CLOSED state.",
        severity="INFO",
        error_rate=0.5,
        dlq_count=0,
        circuit_state="CLOSED",
    )

    return incident