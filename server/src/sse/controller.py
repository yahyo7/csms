from fastapi import APIRouter
from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import List, Callable
from charge_point_node.main import BaseEvent
from functools import wraps
from charge_point_node.main import EventName


stream_router = APIRouter(tags=["stream"])

ALLOWED_SSE_EVENTS = [
    EventName.NEW_CONNECTION
]


class Publisher:
    observers: List["Observer"] = []
    
    async def ensure_observers(self) -> None:
        for observer in self.observers:
            if await observer.request.is_disconnected():
                self.observers.remove(observer)
                del observer
                
    
    async def add_observer(self, observer: "Observer") -> None:
        await self.ensure_observers()
        self.observers.append(observer)
        
    async def remove_observer(self, observer: "Observer") -> None:
        self.observers.remove(observer)
        
    def publish(self, func) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            event = await func(*args, **kwargs)
            if event.name in ALLOWED_SSE_EVENTS:
                for observer in self.observers:
                    await observer.put(event)
        return wrapper


class Observer(asyncio.Queue):
    
    def __init__(self, request: Request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    async def subscribe(self, publisher) -> None:
        await publisher.add_observer(self)
    
    async def unsubscribe(self, publisher) -> None:
        await publisher.remove_observer(self)



async def event_generator(observer: Observer):
    delay = 0.5 # seconds
    while True:
        event = await observer.get()
        if event is not None:
            yield event
        await asyncio.sleep(delay)
        
sse_publisher = Publisher()

@stream_router.get("/stream")
async def stream(request: Request):
    observer = Observer(request)
    await observer.subscribe(sse_publisher)
    return EventSourceResponse(event_generator(observer))