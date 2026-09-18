from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.websocket import router as websocket_router


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