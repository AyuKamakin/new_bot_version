from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from SG.Create_Request_SG import Create_Request_SG
from SG.Start_SG import Start_SG


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def go_to_add_equipment(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.search_menu)


async def go_to_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.show_basket)


async def go_to_send_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.send_basket_requests)


async def go_to_search_by_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.choose_category)


async def go_to_search_by_name(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.choose_equipment_by_name)
