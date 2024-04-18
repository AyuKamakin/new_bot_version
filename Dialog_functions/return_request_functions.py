from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Button
from Request_classes.Request_collection import *
from SG.Return_request_SG import Return_Request_SG
from SG.Start_SG import Start_SG


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
    reqs_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback.from_user.id)]
    manager.dialog_data['deleted_keys'] = list(basket_collection_return.keys())
    reqs_collection.update_requests_parameters_by_id(keys_list=list(basket_collection_return.keys()),
                                                     status=PROCEEDING_RETURN)
    basket_collection_return.clear()
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
