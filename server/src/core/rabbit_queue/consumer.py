#The start_consume function creates an asynchronous consumer that:
#Establishes a connection and channel to RabbitMQ.
#Declares the specified queue and sets QoS for efficient message processing.
#Continuously listens for incoming messages and processes each one using the on_message callback function.
#Runs indefinitely, handling messages as they arrive until manually stopped.

import asyncio

from core.rabbit_queue.queue import get_connection, get_channel

async def start_consume(
    queue_name,
    on_message,
    prefetch_count=100,
    durable=True
    )-> None:
    connection = await get_connection()
    channel = await get_channel(connection, queue_name)
    
    await channel.set_qos(prefetch_count=prefetch_count)
    queue = await channel.declare_queue(queue_name, durable=durable)
    await queue.consume(on_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()

        