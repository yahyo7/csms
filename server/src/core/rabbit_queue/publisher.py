# The publish function provides a way to asynchronously send JSON-formatted data to a specified RabbitMQ 
# queue using the default exchange. By connecting to RabbitMQ and using the get_channel utility, 
# it ensures the message is routed correctly, and the encoding (UTF-8) and content type (JSON) are set for compatibility.

import aio_pika

from core.rabbit_queue.queue import get_connection, get_channel

# asynchronous - designed to send (publish) a message to a specified queue in RabbitMQ.
async def publish(data: str, to: str) -> None:
    connection = await get_connection()
    channel = await get_channel(connection, to)
    
    await channel.default_exchange.publish(
        aio_pika.Message(
            bytes(data, "utf-8"),
            content_type="json",
            
            ),
        routing_key=to
    )
