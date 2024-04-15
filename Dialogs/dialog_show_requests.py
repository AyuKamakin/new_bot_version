import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Dialog_functions.show_requests_functions import show_awaiting, show_approved, show_proceeding, \
    show_declined, to_menu, show_or_delete_chosen_request, to_show_reqs, show_chosen_request, \
    show_requests_by_condition, deletion_confirmed, confirm_deletion, go_back, show_in_usage, show_ready_return, \
    show_proceeding_return, show_return_done
from Getters.show_requests_getters import get_requests_counts, get_requests_list, get_request_info, get_deleted_req_info
from SG.Show_requests_SG import Show_requests_SG

window_start = Window(

    Const('Выберите какие запросы желаете просмотреть'),
    Const(' '),
    Button(Format("Ожидающие, {READY} шт"), id="show_awaiting", on_click=show_awaiting),
    Button(Format("Одобренные, {APPROVED} шт"), id="show_approved", on_click=show_approved),
    Button(Format("В обработке на получение, {PROCEEDING} шт"), id="show_proceeding", on_click=show_proceeding),
    Button(Format("В пользовании, {IN_USAGE} шт"), id="show_proceeding", on_click=show_in_usage),
    Button(Format("Ожидающие возврата, {READY_RETURN} шт"), id="show_approved", on_click=show_ready_return),
    Button(Format("В обработке на возврат, {PROCEEDING_RETURN} шт"), id="show_proceeding", on_click=show_proceeding_return),
    Button(Format("Возвращенные, {RETURN_DONE} шт"), id="show_declined", on_click=show_return_done),
    Button(Format("Отклоненные, {DECLINED} шт"), id="show_declined", on_click=show_declined),
    Button(Format("Вернуться в меню"), id="to_menu", on_click=to_menu),
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
            id='equipment_choosing4',
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

window_show_in_usage = Window(
    Const("На данный момент оборудование из следующих запросов в пользовании."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='equipment_choosing5',
            on_click=show_chosen_request
        ),
        id="equipments5",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_in_usage,
    getter=get_requests_list
)

window_show_return_done = Window(
    Const("На данный момент следующие запросы успешно возвращены."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='equipment_choosing6',
            on_click=show_chosen_request
        ),
        id="equipments6",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_return_done,
    getter=get_requests_list
)

window_show_proceeding_return = Window(
    Const("На данный момент следующие запросы на возврат в обработке."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='equipment_choosing7',
            on_click=show_or_delete_chosen_request
        ),
        id="equipments7",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_proceeding_return,
    getter=get_requests_list
)

window_show_ready_return = Window(
    Const("На данный момент оборудование из следующих запросов возможно вернуть."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='equipment_choosing8',
            on_click=show_or_delete_chosen_request
        ),
        id="equipments8",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_ready_return,
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
                              window_confirm_deletion, window_deletion_confirmed, window_show_in_usage,
                              window_show_proceeding_return, window_show_return_done, window_show_ready_return)
