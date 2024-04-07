import operator

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from Dialog_functions.create_request_functions import to_menu, go_back, go_to_add_equipment, go_to_basket, \
    go_to_send_request, go_to_search_by_name, go_to_search_by_category
from SG.Create_Request_SG import Create_Request_SG
from inventory_information import devices_info
from encoding import text_to_number, number_to_text


async def get_caterories(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    category_list = [(i, text_to_number(i)) for i in list(devices_info.keys())]
    return {"category_list": category_list}


async def choose_category(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['current_category'] = number_to_text(button_id)
    print(number_to_text(button_id))
    await manager.switch_to(Create_Request_SG.search_menu)


window_start = Window(
    Const("Меню создания запроса"),
    # поменять позже следующую строку
    Const("Для отправки запроса перейдите в корзину"),
    Button(Const("Добавить оборудование"), id="to_add_equipment", on_click=go_to_add_equipment),
    Button(Const("Просмотреть корзину"), id="to_basket", on_click=go_to_basket),
    Button(Const("Отправить запрос"), id="to_send_request", on_click=go_to_send_request),
    Button(Const("Вернуться"), id="to_menu", on_click=to_menu),
    state=Create_Request_SG.start,
)
window_search_menu = Window(
    Const("Как вы хотите добавить оборудование ?"),
    Button(Const("Поиск по категории"), id="search_by_category", on_click=go_to_search_by_category),
    Button(Const("Поиск по названию"), id="search_by_name", on_click=go_to_search_by_name),
    Button(Const("Вернуться"), id="go_back1", on_click=go_back),
    state=Create_Request_SG.search_menu,
)

window_choose_category = Window(
    Const("Доступные категории оборудования"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="category_list",
            id="category_choosing",
            on_click=choose_category
        ),
        id="categories",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back2", on_click=go_back),
    state=Create_Request_SG.choose_category,
    getter=get_caterories
)

window_choose_from_category = Window(
    Const("Доступные категории оборудования"),
    Button(Const("Вернуться"), id="go_back3", on_click=go_back),
    state=Create_Request_SG.choose_equipment_by_category,
)
dialog_create_request = Dialog(window_start, window_search_menu,window_choose_category, window_choose_from_category)
