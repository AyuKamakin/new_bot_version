from SG import Change_User_SG
from aiogram.types import CallbackQuery
from aiogram_dialog import (
    Dialog, DialogManager, StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from SG.Start_SG import Start_SG
from SG.Change_User_SG import Change_User_SG
from SG.Show_requests_SG import Show_requests_SG

async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()


window_start = Window(
    Const("Авторизация успешна"),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Start_SG.start,
)


async def go_to_change_user(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Change_User_SG.start, mode=StartMode.RESET_STACK)
async def go_to_show_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Show_requests_SG.start, mode=StartMode.RESET_STACK)


window_menu = Window(
    Const("Вы перешли в меню"),
    Button(Const("Мои запросы"), id="my_reqs", on_click=go_to_show_requests),
    Button(Const("Создать запрос"), id="create_req"),
    Button(Const("Сменить пользователя"), id="change_user", on_click=go_to_change_user),
    state=Start_SG.menu,
)
dialog_menu = Dialog(window_start, window_menu)
