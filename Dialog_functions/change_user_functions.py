from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from SG.Start_SG import Start_SG


async def to_menu_2(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def enter_login(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()
