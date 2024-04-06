from aiogram.types import CallbackQuery
from aiogram_dialog import (
    Dialog, DialogManager, StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from SG.Change_User_SG import Change_User_SG
from SG.Start_SG import Start_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def enter_login(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()


window_start = Window(
    Const('Доступные действия: '),
    Button(Const("Ввести логин"), id="enter_login", on_click=enter_login),
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
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
