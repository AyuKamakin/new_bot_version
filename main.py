import logging
import random

from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import (
    DialogManager, setup_dialogs, StartMode, )
from Request_classes.Request_collection import Request_collection
from Request_classes.Request_additional_info_collection import Request_additional_info_collection
from SG.Start_SG import Start_SG
from dispatcher import dp
from encoding import find_similar_strings, merge_lists_from_dict
from inventory_information import devices_with_categories_info
from request_collection_middleware import RequestCollectionMiddleware

with open('.env', 'r') as file:
    API_TOKEN = file.readline().strip().split('=')[1]

bot = Bot(token=API_TOKEN)
setup_dialogs(dp)
# вот такие данные запихать куда надо, пусть пока в этой коллекции лежат запросы нашего условного пользователя

middleware = RequestCollectionMiddleware()

dp.message.middleware(middleware)
dp.callback_query.middleware(middleware)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    dialog_manager.middleware_data.get('request_collection')[int(message.from_user.id)] = Request_collection()
    dialog_manager.middleware_data.get('request_collection')[int(message.from_user.id)].generate_random_requests(
        num=random.randint(10, 30), user_id=message.from_user.id)
    dialog_manager.middleware_data.get('basket_collection')[int(message.from_user.id)] = Request_collection()
    dialog_manager.middleware_data.get('basket_return_collection')[int(message.from_user.id)] = Request_collection()
    dialog_manager.middleware_data.get('additional_info_collection')[int(message.from_user.id)] = Request_additional_info_collection()
    await dialog_manager.start(Start_SG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot, skip_updates=True)
