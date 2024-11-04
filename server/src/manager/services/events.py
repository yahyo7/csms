from loguru import logger
import json
from aio_pika.abc import AbstractIncomingMessage

from charge_point_node.main import OnConnectionEvent, EventName
from manager.services.charge_points import update_charge_point_status
from sse.controller import sse_publisher
from charge_point_node.main import BaseEvent


@sse_publisher.publish
async def process_event(message: AbstractIncomingMessage) -> BaseEvent:
    async with message.process():
        data = json.loads(message.body.decode())
        event_name = data["name"]
        event = {
            EventName.NEW_CONNECTION.value: OnConnectionEvent
        }[event_name](**data)
        logger.info(f"Got event from charge point node (event={event})")
        
        
        if event_name == EventName.NEW_CONNECTION.value:
            await update_charge_point_status(charge_point_id=event.charge_point_id, status="available")

    
    return event