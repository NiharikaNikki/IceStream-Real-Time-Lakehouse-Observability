import asyncio
import json

import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/events"

    async with websockets.connect(uri) as websocket:

        message = await websocket.recv()

        print("Server Message:")
        print(message)

        event = {
            "event_type": "quality_alert",
            "status": "OPEN",
            "error_rate": 3.25,
            "dlq_count": 5,
            "message": "Error rate exceeded 2%",
        }

        await websocket.send(json.dumps(event))

        print("\nEvent Sent:")
        print(event)


if __name__ == "__main__":
    asyncio.run(test_websocket())