from typing import Any, Awaitable, Callable, Dict, Union
from Request_collection import Request_collection
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization


class RequestCollectionMiddleware(BaseMiddleware):

    def __init__(self, request_collection: Request_collection):
        super().__init__()
        self.__request_collection = request_collection

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        data["request_collection"] = self.__request_collection
        return await handler(event, data)
