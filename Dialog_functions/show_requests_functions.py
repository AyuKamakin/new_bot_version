from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_additional_info_collection import Request_additional_info_collection
from Request_classes.Request_collection import *
from SG import Return_request_SG
from SG.Create_Request_SG import Create_Request_SG
from SG.Show_requests_SG import Show_requests_SG
from SG.Start_SG import Start_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


# удаление запроса, дописать удаление из базы
async def deletion_confirmed(callback: CallbackQuery, button: Button, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get("current_request_id")]
    if req.status in [PROCEEDING, READY, APPROVED]:
        request_collection.update_requests_parameters_by_id(keys_list=list([req.id]), status=DECLINED)
    elif req.status in [PROCEEDING_RETURN, READY_RETURN]:
        request_collection.update_requests_parameters_by_id(keys_list=list([req.id]), status=IN_USAGE)
    elif req.status in [RETURN_DONE, IN_USAGE, DECLINED]:
        await callback.answer(show_alert=True, text='Удалить невозможно')
    await manager.switch_to(Show_requests_SG.deletion_confirmed)


async def show_requests_by_condition(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    if manager.dialog_data.get("request_status") == APPROVED:
        await manager.switch_to(Show_requests_SG.show_approved)
    elif manager.dialog_data.get("request_status") == READY:
        await manager.switch_to(Show_requests_SG.show_ready)
    elif manager.dialog_data.get("request_status") == PROCEEDING:
        await manager.switch_to(Show_requests_SG.show_proceeding)
    elif manager.dialog_data.get("request_status") == DECLINED:
        await manager.switch_to(Show_requests_SG.show_declined)
    elif manager.dialog_data.get("request_status") == PROCEEDING_RETURN:
        await manager.switch_to(Show_requests_SG.show_proceeding_return)
    elif manager.dialog_data.get("request_status") == READY_RETURN:
        await manager.switch_to(Show_requests_SG.show_ready_return)
    elif manager.dialog_data.get("request_status") == RETURN_DONE:
        await manager.switch_to(Show_requests_SG.show_return_done)
    elif manager.dialog_data.get("request_status") == IN_USAGE:
        await manager.switch_to(Show_requests_SG.show_in_usage)


async def show_declined(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = DECLINED
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(DECLINED)) != 0:
        await manager.switch_to(Show_requests_SG.show_declined)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_awaiting(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = READY
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(READY)) != 0:
        await manager.switch_to(Show_requests_SG.show_ready)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_approved(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = APPROVED
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(APPROVED)) != 0:
        await manager.switch_to(Show_requests_SG.show_approved)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_in_usage(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["request_status"] = IN_USAGE
    manager.dialog_data["current_request_id"] = int(button_id)
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(IN_USAGE)) != 0:
        await manager.switch_to(Show_requests_SG.show_chosen_in_usage)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def to_show_in_usage(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = IN_USAGE
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(IN_USAGE)) != 0:
        await manager.switch_to(Show_requests_SG.show_in_usage)
    else:
        await callback.answer(show_alert=True, text='Нет оборудования в пользовании')


async def to_show_chosen_in_usage(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = IN_USAGE
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(IN_USAGE)) != 0:
        await manager.switch_to(Show_requests_SG.show_in_usage)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_ready_return(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = READY_RETURN
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(READY_RETURN)) != 0:
        await manager.switch_to(Show_requests_SG.show_ready_return)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_proceeding_return(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = PROCEEDING_RETURN
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(PROCEEDING_RETURN)) != 0:
        await manager.switch_to(Show_requests_SG.show_proceeding_return)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def show_return_done(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = RETURN_DONE
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(RETURN_DONE)) != 0:
        await manager.switch_to(Show_requests_SG.show_return_done)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def to_show_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Show_requests_SG.start)


async def to_choose_postamat(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(manager.event.from_user.id)]
    if int(manager.dialog_data.get('current_request_id')) in list(basket_return_collection.keys()):
        await callback.answer(show_alert=True, text='Уже в списке возврата')
    else:
        await manager.switch_to(Show_requests_SG.choose_postamat)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def show_chosen_request(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, button_id):
    dialog_manager.dialog_data["current_request_id"] = int(button_id)
    await dialog_manager.switch_to(Show_requests_SG.show_chosen_request)


async def show_or_delete_chosen_request(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                        button_id):
    dialog_manager.dialog_data["current_request_id"] = int(button_id)
    await dialog_manager.switch_to(Show_requests_SG.show_or_delete_chosen_request)


async def show_chosen_in_usage(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                               button_id):
    dialog_manager.dialog_data["current_request_id"] = int(button_id)
    print(f'id = {button_id}')
    print(f'dialog_manager.dialog_data["current_request_id"] = {dialog_manager.dialog_data.get("current_request_id")}')
    await dialog_manager.switch_to(Show_requests_SG.show_chosen_in_usage)


async def show_proceeding(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = PROCEEDING
    req_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(manager.event.from_user.id)]
    if len(req_collection.get_requests_by_status(PROCEEDING)) != 0:
        await manager.switch_to(Show_requests_SG.show_proceeding)
    else:
        await callback_query.answer(show_alert=True, text='Такие запросы отсутствуют')


async def confirm_deletion(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Show_requests_SG.confirm_deletion)


async def add_to_return_basket(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback_query.from_user.id)]
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback_query.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get('current_request_id')]
    # req.postamat_id = button_id
    basket_return_collection.add_existing_request(req)
    await manager.switch_to(Show_requests_SG.adding_confirmed)


async def set_postamat_num(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_postamat"] = int(button_id)
    await manager.switch_to(Show_requests_SG.choose_rating)


async def comment_created(msg: Message, inp: MessageInput, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(msg.from_user.id)]
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(msg.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get('current_request_id')]
    req.postamat_id = int(manager.dialog_data.get('chosen_postamat'))
    basket_return_collection.add_existing_request(req)
    added_info: Request_additional_info_collection = manager.middleware_data.get('additional_info_collection')[int(msg.from_user.id)]
    added_info.create_and_add_info(new_id=req.id, new_comment=msg.text, new_rating=manager.dialog_data.get('chosen_rating'))
    print(added_info[manager.dialog_data.get('current_request_id')])
    await manager.switch_to(Show_requests_SG.adding_confirmed)


async def to_added(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback_query.from_user.id)]
    basket_return_collection: Request_collection = manager.middleware_data.get("basket_return_collection")[
        int(callback_query.from_user.id)]
    req: Request = request_collection[manager.dialog_data.get('current_request_id')]
    req.postamat_id = int(manager.dialog_data.get('chosen_postamat'))
    basket_return_collection.add_existing_request(req)
    added_info: Request_additional_info_collection = manager.middleware_data.get('additional_info_collection')[int(callback_query.from_user.id)]
    added_info.create_and_add_info(new_id=req.id, new_comment='', new_rating=manager.dialog_data.get('chosen_rating'))
    print(added_info[manager.dialog_data.get('current_request_id')])
    await manager.switch_to(Show_requests_SG.adding_confirmed)


async def to_return_basket(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Return_request_SG.Return_Request_SG.show_return_basket)


async def set_rating(callback_query: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["chosen_rating"] = int(button_id)
    await manager.switch_to(Show_requests_SG.create_comment)
