from aiogram_dialog import (
    Dialog, Window
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from Dialog_functions.change_user_functions import enter_login, to_menu, to_menu_2
from SG.Change_User_SG import Change_User_SG

window_start = Window(
    Const('Доступные действия: '),
    Button(Const("Ввести логин"), id="enter_login", on_click=enter_login),
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
    state=Change_User_SG.start,
)

window_enter_login = Window(
    Const("Введите логин"),
    Button(Const("Вернуться"), id="to_menu_2", on_click=to_menu_2),
    state=Change_User_SG.enter_login,
)
dialog_change_user = Dialog(window_start, window_enter_login)
