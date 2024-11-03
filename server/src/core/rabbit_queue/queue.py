# core/rabbit_queue/__init__.py

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from loguru import logger

from charge_point_node.settings import TASKS_QUEUE_NAME, EVENTS_QUEUE_NAME, RABBITMQ_USER, RABBITMQ_PW, RABBITMQ_PORT, RABBITMQ_HOST

_connection: AbstractRobustConnection | None = None
_tasks_channel: AbstractRobustChannel | None = None
_events_channel: AbstractRobustChannel | None = None

async def get_connection(
    user=RABBITMQ_USER,
    password=RABBITMQ_PW,
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
) -> AbstractRobustConnection:
    global _connection
    if _connection is None:
        _connection = await connect_robust(
            (
                f"amqp://"
                f"{user}:"
                f"{password}@"
                f"{host}:"
                f"{port}"
            ),
            timeout=20
        )
        logger.info(f"Got Queue connection for user: {user} on host: {host} on port: {port}")
    return _connection

async def get_channel(
    connection: AbstractRobustConnection,
    queue: str
) -> AbstractRobustChannel:
    global _tasks_channel, _events_channel
    if queue == TASKS_QUEUE_NAME:
        if _tasks_channel is None:
            _tasks_channel = await connection.channel()
            logger.info(f"Got channel for queue: {queue}")
        return _tasks_channel
    elif queue == EVENTS_QUEUE_NAME:
        if _events_channel is None:
            _events_channel = await connection.channel()
            logger.info(f"Got channel for queue: {queue}")
        return _events_channel
    else:
        raise ValueError(f"Unknown queue: {queue}")
