import random

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_collection import PROCEEDING
from SG.Create_Request_SG import Create_Request_SG
from SG.Start_SG import Start_SG
from encoding import get_cat_from_num, get_name_from_num
from inventory_information import devices_with_categories_info


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

async def choose_category(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['current_category'] = get_cat_from_num(button_id, devices_with_categories_info)
    await manager.switch_to(Create_Request_SG.choose_equipment_by_category)


async def choose_equipment(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['chosen_equipment'] = get_name_from_num(button_id, devices_with_categories_info)
    await manager.switch_to(Create_Request_SG.choose_number)


async def choose_number(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['chosen_number'] = button_id
    await manager.switch_to(Create_Request_SG.choose_postamat)


async def choose_postamat(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data['chosen_postamat'] = button_id
    i = random.randint(10000000, 11000000)
    while i in list(manager.middleware_data.get("request_collection").keys()) or i in list(
            manager.middleware_data.get("basket_collection").keys()):
        i = random.randint(10000000, 11000000)
    manager.dialog_data['chosen_id'] = i
    manager.middleware_data.get("basket_collection").create_and_add_request(i,
                                                                            manager.dialog_data.get('chosen_equipment'),
                                                                            PROCEEDING,
                                                                            manager.dialog_data.get('chosen_number'),
                                                                            manager.dialog_data.get('chosen_postamat'),
                                                                            random.randint(1, 100))
    print(manager.middleware_data.get("basket_collection")[i])
    await manager.switch_to(Create_Request_SG.successfully_added)
