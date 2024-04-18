from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from Dialogs.dialog_return_request import dialog_return_request
from Dialogs.dialog_show_requests import dialog_show_requests
from Dialogs.dialog_menu import dialog_menu
from Dialogs.dialog_change_user import dialog_change_user
from Dialogs.dialog_create_request import dialog_create_request
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(dialog_menu)
dp.include_router(dialog_change_user)
dp.include_router(dialog_show_requests)
dp.include_router(dialog_create_request)
dp.include_router(dialog_return_request)

