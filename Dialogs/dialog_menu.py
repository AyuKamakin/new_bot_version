from Dialog_functions.menu_functions import go_to_show_requests, go_to_change_user, to_menu, go_to_create_request, \
    go_to_return_reqs
from aiogram_dialog import (
    Dialog, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from SG.Start_SG import Start_SG

window_start = Window(
    Const("Авторизация успешна"),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Start_SG.start,
)


window_menu = Window(
    Const("Вы перешли в меню"),
    Button(Const("Мои запросы"), id="my_reqs", on_click=go_to_show_requests),
    Button(Const("Создать запрос"), id="create_req", on_click=go_to_create_request),
    Button(Const("Вернуть оборудование"), id="return_reqs", on_click=go_to_return_reqs),
    Button(Const("Сменить пользователя"), id="change_user", on_click=go_to_change_user),
    state=Start_SG.menu,
)
dialog_menu = Dialog(window_start, window_menu)
