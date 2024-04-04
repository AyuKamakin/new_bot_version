import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from Request_collection import Request_collection
from Request import Request

devices_info = {
    "Плата": [
        "Arduino UNO",
        "Arduino MEGA",
        "Arduino NANO",
        "Raspberry Pi Zero",
        "Raspberry Pi 4",
        "Raspberry Pi 5",
        "DE-10 Lite",
        "Плата расширения Relay Shield",
        "Макетная плата"
    ],
    "Датчик": [
        "Rfid-считыватель RDM 6300",
        "Rfid-считыватель RC 522",
        "Ультразвуковой дальномер HC-SR04",
        "Инфракрасный дальномер 10-80 см",
        "Геркон",
        "Реле SRD-12VDC-SL-C",
        "DHT-11 Датчик температуры и влажности",
        "Датчик водорода VQ-8",
        "Датчик угарного газа MQ-9",
        "Пьезоэлемент"
    ],
    "Провода": [
        "Кабель ethernet 20 метров"
    ],
    "Экран": [
        "LCD Дисплей",
        "Экран сенсорный 6 дюймов"
    ],
    "Компьютерные части": [
        "Видеокарта Nvidia RTX Quadro 4000",
        "Xiaomi Mi Router 4C"
    ],
    "Иное": [
        "ESP 8266",
        "Матричная клавиатура 4x4"
    ]
}
devices_list = [item for sublist in devices_info.values() for item in sublist]

all_user_reqs = {'curr': Request_collection()}
all_user_reqs['curr'].generate_random_requests(num=random.randint(10, 30))
# t.me/TestBotHelloWorld_bot

with open('.env', 'r') as file:
    token = file.readline().strip().split('=')[1]

API_TOKEN = token


class MySG(StatesGroup):
    state_watch_requests = State()
    state_show_awaiting = State()

async def clicked_show_awaiting(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.show(MySG.state_show_awaiting)

async def clicked_show_approved(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Добавьте обработчик для кнопки "Одобренные"
    pass

async def clicked_show_processing(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Добавьте обработчик для кнопки "В обработке"
    pass

async def clicked_show_declined(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Добавьте обработчик для кнопки "Отказано"
    pass
# Создаем окна
window_show_requests = Window(
    Const("Выберите категорию:"),
    Button(Const("Ожидающие выдачи"), id="show_awaiting", on_click=clicked_show_awaiting),
    Button(Const("Одобренные"), id="show_approved", on_click=clicked_show_approved),
    Button(Const("В обработке"), id="show_processing", on_click=clicked_show_processing),
    Button(Const("Отказано"), id="show_declined", on_click=clicked_show_declined),
    state=MySG.state_watch_requests
)

window_show_awaiting = Window(
    Const("Ожидающие выдачи"),
    state=MySG.state_show_awaiting
)

# Создаем диалог и добавляем в него окна
dialog = Dialog(window_show_requests, window_show_awaiting)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(dialog)

# Регистрируем диалог и состояния в диспетчере
bot = Bot(token=API_TOKEN)
setup_dialogs(dp)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.state_watch_requests, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    bot.request_timeout = 30
    dp.run_polling(bot, skip_updates=True)
