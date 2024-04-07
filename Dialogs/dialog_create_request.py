import operator

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from Dialog_functions.create_request_functions import to_menu, go_back, go_to_add_equipment, go_to_basket, \
    go_to_send_request, go_to_search_by_name, go_to_search_by_category, choose_category, choose_equipment, \
    choose_number, choose_postamat, update_basket_request, go_to_update_num, go_to_update_postamat, \
    go_to_show_chosen_request, update_postamat, update_num
from Getters.create_request_getters import get_caterories, get_equipment_from_cat, get_numbers_of_eq, \
    get_numbers_of_postamats, get_adding_status, get_basket_requests_list, get_changable_request_info
from SG.Create_Request_SG import Create_Request_SG

window_start = Window(
    Const("Меню создания запроса"),
    # поменять позже следующую строку
    Const("Добавьте оборудование в корзину, после чего перейдите в корзину и отправьте запрос"),
    Button(Const("Добавить оборудование"), id="to_add_equipment", on_click=go_to_add_equipment),
    Button(Const("Просмотреть корзину"), id="to_basket", on_click=go_to_basket),
    Button(Const("Вернуться"), id="to_menu", on_click=to_menu),
    state=Create_Request_SG.start,
)


window_basket = Window(
    Const("Ваша корзина"),
    Const("Для удаления или изменения количества оборудования или желаемого постамата нажмите на наименование"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=update_basket_request
        ),
        id="equipments",
        width=1,
        height=6,
    ),
    Button(Const("Отправить запрос"), id="to_send_request", on_click=go_to_send_request),
    Button(Const("Вернуться"), id="go_back_6", on_click=to_menu),
    state=Create_Request_SG.show_basket,
    getter=get_basket_requests_list
)

window_show_chosen_request = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Format('Постамат: {postamat}'),
    Button(Const("Изменить количество"), id="change_num", on_click=go_to_update_num),
    Button(Const("Изменить постамат"), id="change_postamat", on_click=go_to_update_postamat),
    Button(Const("Вернуться"), id="go_back7", on_click=go_to_basket),
    state=Create_Request_SG.show_chosen_request,
    getter=get_changable_request_info
)

window_update_number = Window(
    Const("Доступное количество"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="updating_number",
            on_click=update_num
        ),
        id="choose_num_for_change",
        width=10,
        height=10,
    ),
    Button(Const("Вернуться"), id="go_back8", on_click=go_to_show_chosen_request),
    state=Create_Request_SG.change_number,
    getter=get_numbers_of_eq
)

window_update_postamat = Window(
    Const("Доступные постаматы"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="update_postamat",
            on_click=update_postamat
        ),
        id="choose_num",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back9", on_click=go_to_show_chosen_request),
    state=Create_Request_SG.change_postamat,
    getter=get_numbers_of_postamats
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
                               window_choose_equipment_number, window_choose_postamat, window_added_to_basket,
                               window_basket,window_show_chosen_request, window_update_postamat, window_update_number)
