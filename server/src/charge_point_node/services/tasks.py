# charge_point_node/services/tasks.py

import json
from loguru import logger
from aio_pika import IncomingMessage
from core.rabbit_queue.publisher import publish
from charge_point_node.settings import EVENTS_QUEUE_NAME

async def process_tasks(message: IncomingMessage):
    """
    Process incoming tasks from the queue.
    
    This function is called for each message in the TASKS_QUEUE_NAME queue.
    It processes the message, performs the required task, and publishes
    an event if necessary.
    """
    try:
        # Decode and parse the message body
        message_content = message.body.decode("utf-8")
        task_data = json.loads(message_content)
        
        # Log the incoming task
        logger.info(f"Processing task: {task_data}")
        
        # Simulate task handling
        # (e.g., interacting with the charge point or updating status)
        charge_point_id = task_data.get("charge_point_id")
        task_type = task_data.get("task_type")
        
        # Handle the task based on its type (example logic)
        if task_type == "start_charge":
            # Example: process a "start charge" task
            logger.info(f"Starting charge for charge point {charge_point_id}")
            # Publish event that charging has started
            event = json.dumps({"event": "charging_started", "charge_point_id": charge_point_id})
            await publish(event, to=EVENTS_QUEUE_NAME)
        
        elif task_type == "stop_charge":
            # Example: process a "stop charge" task
            logger.info(f"Stopping charge for charge point {charge_point_id}")
            # Publish event that charging has stopped
            event = json.dumps({"event": "charging_stopped", "charge_point_id": charge_point_id})
            await publish(event, to=EVENTS_QUEUE_NAME)
        
        # Acknowledge the message to remove it from the queue
        await message.ack()
        logger.info("Task processed and acknowledged")

    except Exception as e:
        # Log any exceptions and reject the message
        logger.error(f"Failed to process task: {e}")
        await message.nack(requeue=True)
