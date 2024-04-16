import operator

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Request_classes.Request_collection import *
from SG.Start_SG import Start_SG
from SG.Return_request_SG import *


async def get_numbers_of_postamats(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    numbers_list = [(str(i), i) for i in range(6)]
    return {"numbers_list": numbers_list}


async def get_request_in_usage_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    req = request_collection[int(dialog_manager.dialog_data.get("chosen_request_id"))]
    return {"equipment": req.equipment,
            "number": req.number}


async def get_request_in_basket_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    req = basket_return_collection[int(dialog_manager.dialog_data.get("chosen_request_id"))]
    return {"equipment": req.equipment,
            "number": req.number}


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def to_local_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.start)


async def to_show_in_usage(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = IN_USAGE
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(IN_USAGE)) != 0:
        await manager.switch_to(Return_Request_SG.show_in_usage)
    else:
        await callback.answer(show_alert=True, text='Нет оборудования в пользовании')


async def to_return_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(manager.event.from_user.id)]
    if len(basket_return_collection) != 0:
        await manager.switch_to(Return_Request_SG.show_return_basket)
    else:
        await callback.answer(show_alert=True, text='Список возврата пуст!')


async def to_choose_postamat(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.choose_postamat)


async def get_basket_return_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      basket_return_collection.values()]
    return {"equipment": equipment_list}


async def get_in_usage_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ', ' + str(i.number) + 'шт'), i.id,) for i in
                      request_collection.get_requests_by_status(IN_USAGE)]
    return {"equipment": equipment_list}


async def get_deleted_return_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = int(dialog_manager.dialog_data.get("chosen_request_id"))
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["Успешно удален", "Не удалось удалить, попробуйте позже"]
    if basket_return_collection.get(curr_id) is not None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}


async def get_added_to_basket_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("chosen_request_id")
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["Успешно добавлен в список возврата", "Не удалось добавить, попробуйте позже"]
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


async def to_show_chosen_request(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_request_id"] = button_id
    await manager.switch_to(Return_Request_SG.show_chosen_request)


async def to_show_chosen_in_usage_request(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_request_id"] = int(button_id)
    await manager.switch_to(Return_Request_SG.show_chosen_in_usage)


async def to_del_from_return_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    curr_id = int(manager.dialog_data.get("chosen_request_id"))
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(manager.event.from_user.id)]
    basket_return_collection.delete_by_id_list([curr_id])
    await manager.switch_to(Return_Request_SG.delition_confirmation)


async def to_send_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.send_return_requests)


# дописать отправку запросы на возврат
async def send_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection_return: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback.from_user.id)]
    basket_collection_return.update_requests_parameters_by_id(list(basket_collection_return.keys()),
                                                              status=PROCEEDING_RETURN)
    await manager.switch_to(Return_Request_SG.sent_for_return_confirmed_message)


async def choose_postamat_return_dialog(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    basket_collection_return: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback.from_user.id)]
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get("chosen_request_id")]
    req.postamat_id = button_id
    basket_collection_return.add_existing_request(req)
    await manager.switch_to(Return_Request_SG.added_to_basket_message)


window_start = Window(
    Const("Для отправки запроса на возврат, перейдите в список возврата и отправьте запрос на возврат"),
    Button(Const("Оборудование в пользовании"), id="to_add_return_equipment", on_click=to_show_in_usage),
    Button(Const("Список возврата, отправка запроса"), id="to_basket", on_click=to_return_basket),
    Button(Const("Вернуться"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.start,
)

window_show_basket = Window(
    Const("Ваш cписок возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=to_show_chosen_request
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
    Const("Список оборудования в пользовании"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=to_show_chosen_in_usage_request
        ),
        id="equipments",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back_101", on_click=to_local_menu),
    state=Return_Request_SG.show_in_usage,
    getter=get_in_usage_req_info
)

window_show_chosen_in_usage = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Button(Const("Вернуть оборудование"), id="add_to_return_basket", on_click=to_choose_postamat),
    Button(Const("Вернуться"), id="to_show_return_reqs", on_click=to_return_basket),
    state=Return_Request_SG.show_chosen_in_usage,
    getter=get_request_in_usage_info
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
    Button(Const("Вернуться"), id="go_back100", on_click=to_show_chosen_in_usage_request),
    state=Return_Request_SG.choose_postamat,
    getter=get_numbers_of_postamats
)

window_show_chosen_request = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Button(Const("Удалить из списка возврата"), id="del_from_return_basket", on_click=to_del_from_return_basket),
    Button(Const("Вернуться"), id="go_back102", on_click=to_return_basket),
    state=Return_Request_SG.show_chosen_request,
    getter=get_request_in_basket_info
)

window_send_confirmation = Window(
    Const('Вы уверены что хотите отправить запрос на возврат используемого оборудования ?'),
    Button(Const("Отправить"), id="send_reqs", on_click=send_requests),
    Button(Const("Вернуться"), id="go_back11", on_click=to_return_basket),
    state=Return_Request_SG.send_return_requests,
)

window_requests_sent_message = Window(
    Format('{status}'),
    Button(Const("Перейти в меню возврата"), id="send_reqs", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="send_reqs", on_click=to_menu),
    state=Return_Request_SG.sent_for_return_confirmed_message,
    getter=get_return_sent_status
)
window_added_message = Window(
    Format('{status}'),
    Button(Const("Перейти в список возврата"), id="to_list_return", on_click=to_return_basket),
    Button(Const("Перейти в меню возврата"), id="to_menu_return", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.added_to_basket_message,
    getter=get_added_to_basket_status
)

window_deleted_message = Window(
    Format('{status}'),
    Button(Const("Перейти в список возврата"), id="to_list_return", on_click=to_return_basket),
    Button(Const("Перейти в меню возврата"), id="to_menu_return", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.delition_confirmation,
    getter=get_deleted_return_req_info
)

dialog_return_request = Dialog(window_added_message, window_requests_sent_message, window_send_confirmation,
                               window_show_chosen_request, window_choose_postamat, window_show_in_usage,
                               window_show_basket, window_start, window_show_chosen_in_usage, window_deleted_message)
