from fastapi import FastAPI
import asyncio

from manager.controllers.status import status_router
from manager.services.events import process_event
from core.rabbit_queue.consumer import start_consume
from charge_point_node.settings import EVENTS_QUEUE_NAME

asyncio.ensure_future(
    start_consume(queue_name=EVENTS_QUEUE_NAME, on_message=process_event)
)

app = FastAPI()
app.include_router(status_router)