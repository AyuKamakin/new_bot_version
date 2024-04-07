import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Dialog_functions.dialog_show_requests_functions import show_awaiting, show_approved, show_proceeding, \
    show_declined, to_menu, show_or_delete_chosen_request, to_show_reqs, show_chosen_request, \
    show_requests_by_condition, deletion_confirmed, confirm_deletion, go_back
from Getters.getters_show_requests import get_requests_counts, get_requests_list, get_request_info, get_deleted_req_info
from SG.Show_requests_SG import Show_requests_SG

window_start = Window(
    Const('На данный момент у вас запросов:'),
    Format('{ready} ожидающих;'),
    Format('{approved} одобренных в процессе доставки;'),
    Format('{proceeding} в обработке;'),
    Format('{declined} отклоненных'),
    Button(Const("Просмотреть ожидающие"), id="show_awaiting", on_click=show_awaiting),
    Button(Const("Просмотреть одобренные"), id="show_approved", on_click=show_approved),
    Button(Const("Просмотреть в обработке"), id="show_proceeding", on_click=show_proceeding),
    Button(Const("Просмотреть отклоненные"), id="show_declined", on_click=show_declined),
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
    state=Show_requests_SG.start,
    getter=get_requests_counts
)

window_show_awaiting = Window(
    Const("На данный момент следующие запросы ожидают."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id="equipment_choosing1",
            on_click=show_or_delete_chosen_request
        ),
        id="equipments1",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs1", on_click=to_show_reqs),
    state=Show_requests_SG.show_awaiting,
    getter=get_requests_list
)

window_show_approved = Window(
    Const("На данный момент следующие запросы одобрены."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id="equipment_choosing2",
            on_click=show_or_delete_chosen_request
        ),
        id="equipments2",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs2", on_click=to_show_reqs),
    state=Show_requests_SG.show_approved,
    getter=get_requests_list
)

window_show_proceeding = Window(
    Const("На данный момент следующие запросы в обработке."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id="equipment_choosing3",
            on_click=show_or_delete_chosen_request
        ),
        id="equipments3",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs3", on_click=to_show_reqs),
    state=Show_requests_SG.show_proceeding,
    getter=get_requests_list
)

window_show_declined = Window(
    Const("На данный момент следующие запросы отклонены."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=show_chosen_request
        ),
        id="equipments4",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_declined,
    getter=get_requests_list
)

window_show_chosen_request = Window(
    Format('ID: {id}'),
    Format('Статус: {status}'),
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Format('Постамат: {postamat}'),
    Button(Const("Вернуться"), id="to_show_reqs_5", on_click=show_requests_by_condition),
    state=Show_requests_SG.show_chosen_request,
    getter=get_request_info
)

window_show_or_delete_chosen_request = Window(
    Format('ID: {id}'),
    Format('Статус: {status}'),
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Format('Постамат: {postamat}'),
    Button(Const("Отменить этот запрос"), id="to_confirm_deletion", on_click=confirm_deletion),
    Button(Const("Вернуться"), id="to_show_reqs_6", on_click=show_requests_by_condition),
    state=Show_requests_SG.show_or_delete_chosen_request,
    getter=get_request_info
)

window_confirm_deletion = Window(
    Const("Вы уверены, что хотите отменить запрос ?"),
    Button(Const("Подтвердить"), id="to_confirm_deletion", on_click=deletion_confirmed),
    Button(Const("Вернуться"), id="to_show_req", on_click=go_back),
    state=Show_requests_SG.confirm_deletion,
)

window_deletion_confirmed = Window(
    Format("Запрос {id} {status}"),
    Button(Const("Вернуться в меню"), id="to_menu2", on_click=to_menu),
    Button(Const("Просмотреть запросы"), id="to_show_reqs_5", on_click=to_show_reqs),
    state=Show_requests_SG.deletion_confirmed,
    getter=get_deleted_req_info
)
dialog_show_requests = Dialog(window_start, window_show_awaiting, window_show_approved, window_show_proceeding,
                              window_show_declined, window_show_chosen_request, window_show_or_delete_chosen_request,
                              window_confirm_deletion, window_deletion_confirmed)
