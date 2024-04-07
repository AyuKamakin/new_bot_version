import operator
import random

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from Dialog_functions.create_request_functions import to_menu, go_back, go_to_add_equipment, go_to_basket, \
    go_to_send_request, go_to_search_by_name, go_to_search_by_category, choose_category, choose_equipment, \
    choose_number, choose_postamat
from Getters.create_request_getters import get_caterories, get_equipment_from_cat, get_numbers_of_eq, \
    get_numbers_of_postamats, get_adding_status
from Request_classes.Request_collection import PROCEEDING
from SG.Create_Request_SG import Create_Request_SG
from inventory_information import devices_with_categories_info
from encoding import get_name_from_num, get_num_from_name, get_num_from_cat, get_cat_from_num


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
    Button(Const("Поиск по категории"), id="choose_category", on_click=go_to_search_by_category),
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
    Const("Доступные наименования"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment_list",
            id="eq_choosing_from_cat",
            on_click=choose_equipment
        ),
        id="eqs_from_cats",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back3", on_click=go_back),
    state=Create_Request_SG.choose_equipment_by_category,
    getter=get_equipment_from_cat
)

window_choose_equipment_number = Window(
    Const("Доступное количество"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_number",
            on_click=choose_number
        ),
        id="choose_num",
        width=10,
        height=10,
    ),
    Button(Const("Вернуться"), id="go_back4", on_click=go_back),
    state=Create_Request_SG.choose_number,
    getter=get_numbers_of_eq
)

window_choose_postamat = Window(
    Const("Доступные постаматы"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_postamat",
            on_click=choose_postamat
        ),
        id="choose_num",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back5", on_click=go_back),
    state=Create_Request_SG.choose_postamat,
    getter=get_numbers_of_postamats
)
window_added_to_basket = Window(
    Format("{status}"),
    Button(Const("Перейти в корзину"), id="to_basket_2", on_click=go_to_basket),
    Button(Const("Вернуться в меню"), id="go_back_to_menu1", on_click=to_menu),
    state=Create_Request_SG.successfully_added,
    getter=get_adding_status
)

dialog_create_request = Dialog(window_start, window_search_menu, window_choose_category, window_choose_from_category,
                               window_choose_equipment_number, window_choose_postamat, window_added_to_basket)
