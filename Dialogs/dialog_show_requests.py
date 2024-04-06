import operator
import random

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    Dialog, DialogManager, StartMode, Window,
)
from aiogram import Dispatcher
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Request_classes.Request_collection import Request_collection, statuses, APPROVED, READY, PROCEEDING, DECLINED
from SG.Start_SG import Start_SG
from SG.Show_requests_SG import Show_requests_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


# удаление запроса, дописать удаление из базы
async def deletion_confirmed(callback: CallbackQuery, button: Button, manager: DialogManager):
    print(len(manager.middleware_data.get("request_collection")))
    manager.middleware_data.get("request_collection").delete_by_id_list([manager.dialog_data.get("current_request_id")])
    print(len(manager.middleware_data.get("request_collection")))
    await manager.switch_to(Show_requests_SG.deletion_confirmed)

async def go_back_show_reqs(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    if manager.dialog_data.get("request_status")==APPROVED:
        await manager.switch_to(Show_requests_SG.show_approved)
    elif manager.dialog_data.get("request_status")==READY:
        await manager.switch_to(Show_requests_SG.show_awaiting)
    elif manager.dialog_data.get("request_status")==PROCEEDING:
        await manager.switch_to(Show_requests_SG.show_proceeding)
    elif manager.dialog_data.get("request_status")==DECLINED:
        await manager.switch_to(Show_requests_SG.show_declined)

async def show_declined(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = DECLINED
    await manager.switch_to(Show_requests_SG.show_declined)


async def show_awaiting(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = READY
    await manager.switch_to(Show_requests_SG.show_awaiting)


async def show_approved(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = APPROVED
    await manager.switch_to(Show_requests_SG.show_approved)


async def to_show_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Show_requests_SG.start)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()

async def go_to_show_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Show_requests_SG.start, mode=StartMode.RESET_STACK)


async def show_chosen_request(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, button_id):
    dialog_manager.dialog_data["current_request_id"] = int(button_id)
    await dialog_manager.switch_to(Show_requests_SG.show_chosen_request)


async def show_or_delete_chosen_request(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                        button_id):
    dialog_manager.dialog_data["current_request_id"] = int(button_id)
    await dialog_manager.switch_to(Show_requests_SG.show_or_delete_chosen_request)


async def show_proceeding(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = PROCEEDING
    await manager.switch_to(Show_requests_SG.show_proceeding)


async def confirm_deletion(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Show_requests_SG.confirm_deletion)


async def get_requests_counts(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwargs):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    return {
        APPROVED: len(request_collection.get_requests_id_by_status(APPROVED)),
        DECLINED: len(request_collection.get_requests_id_by_status(DECLINED)),
        PROCEEDING: len(request_collection.get_requests_id_by_status(PROCEEDING)),
        READY: len(request_collection.get_requests_id_by_status(READY)),
    }


async def get_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      request_collection.get_requests_by_status(dialog_manager.dialog_data.get("request_status"))]
    return {"equipment": equipment_list}


async def get_request_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    req = request_collection[dialog_manager.dialog_data.get("current_request_id")]
    status = ''
    if req.status == statuses[0]:
        status = 'Одобрен'
    elif req.status == statuses[1]:
        status = 'Ожидает получения'
    elif req.status == statuses[2]:
        status = 'Отклонен'
    elif req.status == statuses[3]:
        status = 'В обработке'
    return {"id": req.id,
            "equipment": req.equipment,
            "number": req.number,
            "status": status,
            "postamat": req.postamat_id}


# сделать еще одну проверку
async def get_deleted_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("current_request_id")
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    phrases = ["успешно удален", "не удалось удалить, попробуйте позже"]
    if request_collection.get(curr_id) is not None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}


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
    Button(Const("Вернуться"), id="to_show_reqs_5", on_click=go_back_show_reqs),
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
    Button(Const("Вернуться"), id="to_show_reqs_6", on_click=go_back_show_reqs),
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
    Button(Const("Просмотреть запросы"), id="to_show_reqs_5", on_click=go_to_show_requests),
    state=Show_requests_SG.deletion_confirmed,
    getter=get_deleted_req_info
)
dialog_show_requests = Dialog(window_start, window_show_awaiting, window_show_approved, window_show_proceeding,
                              window_show_declined, window_show_chosen_request, window_show_or_delete_chosen_request,
                              window_confirm_deletion, window_deletion_confirmed)
