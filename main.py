import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)
from Request_collection import Request_collection
from Request import Request
from Start_SG import Start_SG
from dialog_menu import dialog_menu
from dispatcher import dp
from request_collection_middleware import RequestCollectionMiddleware

with open('.env', 'r') as file:
    API_TOKEN = file.readline().strip().split('=')[1]

bot = Bot(token=API_TOKEN)
setup_dialogs(dp)
#вот такие данные запихать куда надо, пусть пока в этой коллекции лежат запросы нашего условного пользователя

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