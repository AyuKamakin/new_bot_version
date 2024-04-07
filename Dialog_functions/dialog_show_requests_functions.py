from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_collection import APPROVED, READY, PROCEEDING, DECLINED
from SG.Show_requests_SG import Show_requests_SG
from SG.Start_SG import Start_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


# удаление запроса, дописать удаление из базы
async def deletion_confirmed(callback: CallbackQuery, button: Button, manager: DialogManager):
    print(len(manager.middleware_data.get("request_collection")))
    manager.middleware_data.get("request_collection").delete_by_id_list([manager.dialog_data.get("current_request_id")])
    print(len(manager.middleware_data.get("request_collection")))
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

