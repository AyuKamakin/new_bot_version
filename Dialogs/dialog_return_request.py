import operator

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Getters.create_request_getters import get_numbers_of_postamats, get_changable_request_info
from Getters.show_requests_getters import get_request_info
from Request_classes.Request_collection import *
from SG.Start_SG import Start_SG
from SG.Return_request_SG import *


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def to_local_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.start)


async def to_show_in_usage(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = IN_USAGE
    await manager.switch_to(Return_Request_SG.show_in_usage)


async def to_return_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.show_return_basket)


async def get_basket_return_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      basket_return_collection.values()]
    return {"equipment": equipment_list}


async def get_deleted_return_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("return_request_to_change_id")
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["успешно удален", "не удалось удалить, попробуйте позже"]
    if basket_return_collection.get(curr_id) is not None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}

async def get_added_to_basket_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("return_request_to_change_id")
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["успешно добавлен", "не удалось добавить, попробуйте позже"]
    if basket_return_collection.get(curr_id) is None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}

async def get_return_sent_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    for i in list(basket_return_collection.keys()):
        if request_collection[i].status != PROCEEDING_RETURN:
            return {"status": 'не удалось отправить запросы на возврат, попробуйте позже'}
    return {"status": 'Запросы на возврат отправлены!'}


async def update_return_basket_request(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["return_request_to_change_id"] = button_id
    await manager.switch_to(Return_Request_SG.show_chosen_request)


async def to_del_from_return_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.delition_confirmation)


async def to_send_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.send_return_requests)


async def to_show_chosen_req(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.show_chosen_request)


# дописать отправку запросы на возврат
async def send_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection_return: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback.from_user.id)]
    basket_collection_return.update_requests_parameters_by_id(list(basket_collection_return.keys()),
                                                              status=PROCEEDING_RETURN)
    await manager.switch_to(Return_Request_SG.sent_for_return_confirmed_message)


async def choose_postamat_return_dialog(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['chosen_postamat'] = button_id
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(manager.event.from_user.id)]
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    req = request_collection[manager.dialog_data.get("return_request_to_change_id")]
    basket_return_collection.add_existing_request(req)
    await manager.switch_to(Return_Request_SG.added_to_basket_message)


window_start = Window(
    Const("Меню создания запроса"),
    Const("Для возврата оборудования выберите запрос с оборудованием в пользовании и добавьте в список возврата"),
    Const("Для отправки запроса на возврат, перейдите в список возврата и отправьте запрос на возврат"),
    Button(Const("Просмотреть оборудование в пользовании"), id="to_add_return_equipment", on_click=to_show_in_usage),
    Button(Const("Просмотреть список возврата"), id="to_basket", on_click=to_return_basket),
    Button(Const("Вернуться"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.start,
)

window_basket = Window(
    Const("Ваш cписок возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=update_return_basket_request
        ),
        id="equipments",
        width=1,
        height=6,
    ),
    Button(Const("Отправить запрос"), id="to_send_return_request", on_click=to_send_request),
    Button(Const("Вернуться"), id="go_back_101", on_click=to_menu),
    state=Return_Request_SG.show_return_basket,
    getter=get_basket_return_requests_list
)

window_show_in_usage = Window(
    Format('ID: {id}'),
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Button(Const("Вернуть оборудование"), id="add_to_return_basket", on_click=choose_postamat_return_dialog),
    Button(Const("Вернуться"), id="to_show_return_reqs", on_click=to_return_basket),
    state=Return_Request_SG.show_in_usage,
    getter=get_request_info
)

window_choose_postamat = Window(
    Const("Доступные постаматы для возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_postamat",
            on_click=choose_postamat_return_dialog
        ),
        id="choose_num",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back100", on_click=to_show_chosen_req),
    state=Return_Request_SG.choose_postamat,
    getter=get_numbers_of_postamats
)

window_show_chosen_request = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Button(Const("Удалить из списка возврата"), id="del_from_return_basket", on_click=to_del_from_return_basket),
    Button(Const("Вернуться"), id="go_back102", on_click=to_return_basket),
    state=Return_Request_SG.show_chosen_request,
    getter=get_changable_request_info
)

window_send_confirmation = Window(
    Const('Вы уверены что хотите отправить запрос на возврат используемого оборудования ?'),
    Button(Const("Отправить"), id="send_reqs", on_click=send_requests),
    Button(Const("Вернуться"), id="go_back11", on_click=to_return_basket),
    state=Return_Request_SG.send_return_requests,
)

window_requests_sent_message = Window(
    Format('{status}'),
    Button(Const("Перейти к созданию запросов"), id="send_reqs", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="send_reqs", on_click=to_menu),
    state=Return_Request_SG.requests_sent_message,
    getter=get_return_sent_status
)
window_added_message = Window(
    Format('{status}'),
    Button(Const("Перейти к созданию запросов"), id="send_reqs", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="send_reqs", on_click=to_menu),
    state=Return_Request_SG.added_to_basket_message,
    getter=get_added_to_basket_status
)

dialog_return_request = Dialog(window_added_message,window_requests_sent_message,window_send_confirmation,
                               window_show_chosen_request, window_choose_postamat, window_show_in_usage,
                               window_basket, window_start)