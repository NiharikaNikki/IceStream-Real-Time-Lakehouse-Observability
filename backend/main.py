from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.websocket import router as websocket_router
from backend.websocket import broadcast_alert


app = FastAPI(
    title="IceStream Observability API",
    description="Real-time lakehouse observability backend",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(websocket_router)


@app.get("/")
def root():
    return {
        "project": "IceStream",
        "service": "Observability API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


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