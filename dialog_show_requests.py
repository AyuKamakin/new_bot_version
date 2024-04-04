from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from Change_User_SG import Change_User_SG
from Start_SG import Start_SG
from dialog_menu import dialog_menu
from Show_requests_SG import Show_requests_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def show_declined(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def show_awaiting(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def show_approved(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


async def show_proceeding(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    pass


# тут дописать,
window_start = Window(
    Const('На данный момент у вас запросов:'),
    Format('{} ожидающих;'),
    Format('{} одобренных в процессе доставки;'),
    Format('{} в обработке;'),
    Format('{} отклоненных'),
    Button(Const("Просмотреть ожидающие"), id="show_awaiting", on_click=show_awaiting),
    Button(Const("Просмотреть одобренные"), id="show_approved", on_click=show_approved),
    Button(Const("Просмотреть в обработке"), id="show_proceeding", on_click=show_proceeding),
    Button(Const("Просмотреть отклоненные"), id="show_declined", on_click=show_declined),
    Button(Const("Вернуться в меню"), id="to_menu", on_click=to_menu),
    state=Change_User_SG.start,
)


async def to_show_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


window_show_awaiting = Window(
    Const("На данный момент следующие запросы ожидают."),
    Const("Вы можете просмотреть информацию по каждому запросу нажав на соответствующую кнопку."),
    # тут миллион кнопок
    Button(Const("Вернуться"), id="to_show_reqs1", on_click=to_show_reqs),
    state=Show_requests_SG.show_awaiting,
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
