from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from SG.Change_User_SG import Change_User_SG
from SG.Create_Request_SG import Create_Request_SG
from SG.Show_requests_SG import Show_requests_SG


async def go_to_change_user(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Change_User_SG.start, mode=StartMode.RESET_STACK)


async def go_to_return_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Change_User_SG.start, mode=StartMode.RESET_STACK)


async def go_to_show_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Show_requests_SG.start, mode=StartMode.RESET_STACK)


async def go_to_create_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Create_Request_SG.start, mode=StartMode.RESET_STACK)


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()
