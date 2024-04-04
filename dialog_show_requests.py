import operator

from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)
from aiogram import Dispatcher
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Request_collection import Request_collection, statuses
from Change_User_SG import Change_User_SG
from Start_SG import Start_SG
from dialog_menu import dialog_menu
from Show_requests_SG import Show_requests_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def show_declined(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def show_awaiting(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = "awaiting"
    await manager.switch_to(Show_requests_SG.show_awaiting)


async def show_approved(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def show_proceeding(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def get_requests_counts(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwargs):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    return {
        statuses[0]: len(request_collection.get_requests_by_status(statuses[0])),
        statuses[1]: len(request_collection.get_requests_by_status(statuses[1])),
        statuses[2]: len(request_collection.get_requests_by_status(statuses[2])),
        statuses[3]: len(request_collection.get_requests_by_status(statuses[3])),
    }


async def get_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")
    equipment_list = [(i.equipment, i.id) for i in request_collection.get_requests_by_status(dialog_manager.dialog_data.get("request_status"))]
    return {"equipment": equipment_list}

# тут дописать,
window_start = Window(
    Const('На данный момент у вас запросов:'),
    Format('{ready} ожидающих;'),
    Format('{approved} одобренных в процессе доставки;'),
    Format('{awaiting} в обработке;'),
    Format('{declined} отклоненных'),
    Button(Const("Просмотреть ожидающие"), id="show_awaiting", on_click=show_awaiting),
    Button(Const("Просмотреть одобренные"), id="show_approved", on_click=show_approved),
    Button(Const("Просмотреть в обработке"), id="show_proceeding", on_click=show_proceeding),
    Button(Const("Просмотреть отклоненные"), id="show_declined", on_click=show_declined),
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
    state=Show_requests_SG.start,
    getter=get_requests_counts
)


async def to_show_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


window_show_awaiting = Window(
    Const("На данный момент следующие запросы ожидают."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id="equipment_choosing",
        ),
        id="equipments",
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
    # тут миллион кнопок
    Button(Const("Вернуться"), id="to_show_reqs2", on_click=to_show_reqs),
    state=Show_requests_SG.show_approved,
)

window_show_proceeding = Window(
    Const("На данный момент следующие запросы в обработке."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    # тут миллион кнопок
    Button(Const("Вернуться"), id="to_show_reqs3", on_click=to_show_reqs),
    state=Show_requests_SG.show_proceeding,
)

window_show_declined = Window(
    Const("На данный момент следующие запросы отклонены."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    # тут миллион кнопок
    Button(Const("Вернуться"), id="to_show_reqs4", on_click=to_show_reqs),
    state=Show_requests_SG.show_declined,
)
dialog_show_requests = Dialog(window_start, window_show_awaiting, window_show_approved, window_show_proceeding,
window_show_declined)
