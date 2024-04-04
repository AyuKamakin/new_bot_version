from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dialog_menu import dialog_menu

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(dialog_menu)

