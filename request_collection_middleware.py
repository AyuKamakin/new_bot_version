from typing import Any, Awaitable, Callable, Dict, Union
from Request_classes.Request_collection import Request_collection
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message


class RequestCollectionMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.__request_collection = {}
        self.__basket_collection = {}
        self.__basket_return_collection = {}
        self.__additional_info_collection = {}

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        data["request_collection"] = self.__request_collection
        data["basket_collection"] = self.__basket_collection
        data["basket_return_collection"] = self.__basket_return_collection
        data["additional_info_collection"] = self.__additional_info_collection
        return await handler(event, data)
