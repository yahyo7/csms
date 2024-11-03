import os

from loguru import logger

DEBUG = os.environ.get("DEBUG", "0") == "1"

WS_SERVER_PORT=int(os.environ["WS_SERVER_PORT"])

# Queue names
TASKS_QUEUE_NAME = os.environ.get("TASKS_QUEUE_NAME", "tasks_queue")
EVENTS_QUEUE_NAME = os.environ.get("EVENTS_QUEUE_NAME", "events_queue")

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")  # Default to localhost
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5672))     # Default to 5672 if not set
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "csms")       # Default user
RABBITMQ_PW = os.environ.get("RABBITMQ_PW", "csms")  

logger.add(
    "csms.log",
    enqueue=True,
    backtrace=True,
    diagnose=DEBUG,
    format="{time} - {level} - {message}",
    rotation="10 MB",
    level="INFO"
)
