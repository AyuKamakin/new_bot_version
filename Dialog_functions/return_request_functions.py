from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import StartMode, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_additional_info import Request_additional_info
from Request_classes.Request_additional_info_collection import Request_additional_info_collection
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

    info_coll: Request_additional_info_collection = dialog_manager.middleware_data.get("additional_info_collection")[
        int(dialog_manager.event.from_user.id)]
    req = basket_return_collection[int(dialog_manager.dialog_data.get("chosen_request_id"))]
    inf: Request_additional_info = info_coll[int(dialog_manager.dialog_data.get("chosen_request_id"))]
    return {"equipment": req.equipment,
            "number": req.number,
            "postamat": req.postamat_id,
            "rating": inf.rating,
            "comment": inf.comment,
            }


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
    inf_collection: Request_additional_info_collection = manager.middleware_data.get("additional_info_collection")[
        int(callback.from_user.id)]
    basket_return_collection.delete_by_id_list([curr_id])
    inf_collection.delete_info_by_id(curr_id)
    await manager.switch_to(Return_Request_SG.delition_confirmation)


async def to_send_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.send_return_requests)


async def to_choose_rating(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.choose_rating)


# дописать отправку запросы на возврат и дописать отправку доп инфы
async def send_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection_return: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback.from_user.id)]
    reqs_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback.from_user.id)]
    inf_collection: Request_additional_info_collection = manager.middleware_data.get("additional_info_collection")[
        int(callback.from_user.id)]
    manager.dialog_data['deleted_keys'] = list(basket_collection_return.keys())
    reqs_collection.update_requests_parameters_by_id(keys_list=list(basket_collection_return.keys()),
                                                     status=PROCEEDING_RETURN)
    basket_collection_return.clear()
    inf_collection.clear()
    await manager.switch_to(Return_Request_SG.sent_for_return_confirmed_message)


async def choose_postamat_return_dialog(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_postamat"] = int(button_id)
    await manager.switch_to(Return_Request_SG.choose_rating)


async def set_rating(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_rating"] = int(button_id)
    await manager.switch_to(Return_Request_SG.create_comment)


async def update_postamat_return_dialog(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    basket_collection_return: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback.from_user.id)]
    curr_id = int(manager.dialog_data.get("chosen_request_id"))
    basket_collection_return[curr_id].postamat_id = int(button_id)
    await manager.switch_to(Return_Request_SG.show_chosen_request)


async def update_rating(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    inf_coll: Request_additional_info_collection = manager.middleware_data.get("additional_info_collection")[
        int(callback_query.from_user.id)]
    curr_id = int(manager.dialog_data.get("chosen_request_id"))
    inf_coll[curr_id].rating = int(button_id)
    await manager.switch_to(Return_Request_SG.show_chosen_request)


async def comment_updated(msg: Message, inp: MessageInput, manager: DialogManager):
    added_info: Request_additional_info_collection = manager.middleware_data.get('additional_info_collection')[
        int(msg.from_user.id)]
    added_info[int(manager.dialog_data.get('chosen_request_id'))].comment = msg.text
    await manager.switch_to(Return_Request_SG.show_chosen_request)


async def to_update_postamat(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.update_postamat)


async def to_update_rating(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.update_rating)


async def to_update_comment(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_Request_SG.update_comment)


async def comment_created(msg: Message, inp: MessageInput, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(msg.from_user.id)]
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(msg.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get('chosen_request_id')]
    req.postamat_id = int(manager.dialog_data.get('chosen_postamat'))
    basket_return_collection.add_existing_request(req)
    added_info: Request_additional_info_collection = manager.middleware_data.get('additional_info_collection')[
        int(msg.from_user.id)]
    added_info.create_and_add_info(new_id=req.id, new_comment=msg.text,
                                   new_rating=manager.dialog_data.get('chosen_rating'))
    print(added_info[manager.dialog_data.get('chosen_request_id')])
    await manager.switch_to(Return_Request_SG.added_to_basket_message)


async def to_added(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback_query.from_user.id)]
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback_query.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get('chosen_request_id')]
    req.postamat_id = int(manager.dialog_data.get('chosen_postamat'))
    basket_return_collection.add_existing_request(req)
    added_info: Request_additional_info_collection = manager.middleware_data.get('additional_info_collection')[
        int(callback_query.from_user.id)]
    added_info.create_and_add_info(new_id=req.id, new_comment='', new_rating=manager.dialog_data.get('chosen_rating'))
    print(added_info[manager.dialog_data.get('chosen_request_id')])
    await manager.switch_to(Return_Request_SG.added_to_basket_message)
