import websockets
import asyncio
from pydantic import BaseModel
from enum import Enum
from websockets.legacy.server import WebSocketServerProtocol

from charge_point_node.services.tasks import process_tasks
from core.rabbit_queue.publisher import publish
from core.rabbit_queue.consumer import start_consume
from charge_point_node.settings import WS_SERVER_PORT, TASKS_QUEUE_NAME, EVENTS_QUEUE_NAME

from charge_point_node import settings
from loguru import logger
import json

class EventName(str, Enum):
    NEW_CONNECTION = "new_connection"
    
class BaseEvent(BaseModel):
    name: EventName
    queue: str = EVENTS_QUEUE_NAME
    priority: int = 10
    
class OnConnectionEvent(BaseEvent):
    charge_point_id: str
    name: EventName = EventName.NEW_CONNECTION

async def on_connect(connection: WebSocketServerProtocol, path: str):
    charge_point_id = path.strip("/")
    logger.info(f"New charge point connection from path={path}, charge_point_id={charge_point_id}")
    event = OnConnectionEvent(charge_point_id=charge_point_id, value=1)
    await publish(event.json(), to=EVENTS_QUEUE_NAME)

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