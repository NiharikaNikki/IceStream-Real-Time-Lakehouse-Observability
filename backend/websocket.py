from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        await websocket.send_json(
            {
                "type": "connection",
                "status": "connected",
                "message": "IceStream WebSocket connected",
            }
        )

        while True:
            data = await websocket.receive_json()

            await manager.broadcast(
                {
                    "type": "pipeline_event",
                    "data": data,
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_alert(
    alert_type,
    message,
    severity,
    error_rate=0.0,
    dlq_count=0,
    circuit_state="CLOSED",
):
    alert = {
        "type": "alert",
        "alert_type": alert_type,
        "severity": severity,
        "message": message,
        "error_rate": error_rate,
        "dlq_count": dlq_count,
        "circuit_state": circuit_state,
    }

    await manager.broadcast(alert)