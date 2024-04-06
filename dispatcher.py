from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Dialogs.dialog_show_requests import dialog_show_requests
from Dialogs.dialog_menu import dialog_menu
from Dialogs.dialog_change_user import dialog_change_user
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(dialog_menu)
dp.include_router(dialog_change_user)
dp.include_router(dialog_show_requests)

