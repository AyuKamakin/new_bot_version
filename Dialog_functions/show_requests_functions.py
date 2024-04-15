from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_collection import *
from SG.Show_requests_SG import Show_requests_SG
from SG.Start_SG import Start_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


# удаление запроса, дописать удаление из базы
async def deletion_confirmed(callback: CallbackQuery, button: Button, manager: DialogManager):
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[
        int(callback.from_user.id)]
    request_collection.delete_by_id_list([manager.dialog_data.get("current_request_id")])
    await manager.switch_to(Show_requests_SG.deletion_confirmed)


async def show_requests_by_condition(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    if manager.dialog_data.get("request_status") == APPROVED:
        await manager.switch_to(Show_requests_SG.show_approved)
    elif manager.dialog_data.get("request_status") == READY:
        await manager.switch_to(Show_requests_SG.show_awaiting)
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
    await manager.switch_to(Show_requests_SG.show_declined)


async def show_awaiting(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = READY
    await manager.switch_to(Show_requests_SG.show_awaiting)


async def show_approved(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = APPROVED
    await manager.switch_to(Show_requests_SG.show_approved)


async def show_in_usage(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = IN_USAGE
    await manager.switch_to(Show_requests_SG.show_in_usage)


async def show_ready_return(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = READY_RETURN
    await manager.switch_to(Show_requests_SG.show_ready_return)


async def show_proceeding_return(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = PROCEEDING_RETURN
    await manager.switch_to(Show_requests_SG.show_proceeding_return)


async def show_return_done(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["request_status"] = RETURN_DONE
    await manager.switch_to(Show_requests_SG.show_return_done)


async def to_show_reqs(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Show_requests_SG.start)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


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
