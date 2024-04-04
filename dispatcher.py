from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dialog_menu import dialog_menu
from dialog_change_user import dialog_change_user
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(dialog_menu)
dp.include_router(dialog_change_user)

