from loguru import logger
from aio_pika.abc import AbstractIncomingMessage

async def process_event(event: AbstractIncomingMessage) -> None:
    async with event.process():
        event = event.body.decode()
        logger.info(f"Got event from charge point node (event={event})")
