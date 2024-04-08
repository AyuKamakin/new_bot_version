import logging
import random

from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import (
    DialogManager, setup_dialogs, StartMode, )
from Request_classes.Request_collection import Request_collection
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

all_reqs = Request_collection()
all_reqs.generate_random_requests(num=random.randint(10, 30), user_id=1)
middleware = RequestCollectionMiddleware(all_reqs)

dp.message.middleware(middleware)
dp.callback_query.middleware(middleware)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Start_SG.start, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot, skip_updates=True)
