from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from Change_User_SG import Change_User_SG
from Start_SG import Start_SG
from dialog_menu import dialog_menu


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def enter_login(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()


window_start = Window(
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
    Button(Const("Ввести логин"), id="to_menu", on_click=enter_login),
    state=Change_User_SG.start,
)


async def to_menu_2(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


window_enter_login = Window(
    Const("Введите логин"),
    Button(Const("Вернуться"), id="to_menu_2", on_click=to_menu_2),
    state=Change_User_SG.enter_login,
)
dialog_change_user = Dialog(window_start, window_enter_login)
