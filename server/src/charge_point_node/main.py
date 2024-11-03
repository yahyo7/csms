import websockets
import asyncio
from websockets.legacy.server import WebSocketServerProtocol

from charge_point_node.services.tasks import process_tasks
from core.rabbit_queue.publisher import publish
from core.rabbit_queue.consumer import start_consume
from charge_point_node.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME, EVENTS_QUEUE_NAME

from charge_point_node import settings
from loguru import logger
import json

async def on_connect(connection: WebSocketServerProtocol, path: str):
    charge_point_id = path.strip("/")
    logger.info(f"New charge point connection from path={path}, charge_point_id={charge_point_id}")
    event = json.dumps({"event": "new_connection", "charge_point_id": charge_point_id})
    await publish(event, to=EVENTS_QUEUE_NAME)

async def main():
    asyncio.ensure_future(
        start_consume(TASKS_QUEUE_NAME, on_message=process_tasks)
    )
    
    server = await websockets.serve(
        on_connect,
        "0.0.0.0", 
        WS_SERVER_PORT)
    await server.wait_closed()
    
if __name__ == "__main__":
    asyncio.run(main())