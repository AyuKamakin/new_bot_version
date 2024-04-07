from aiogram import Dispatcher
from aiogram_dialog import DialogManager

from encoding import get_num_from_name, get_num_from_cat
from inventory_information import devices_with_categories_info


async def get_caterories(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    category_list = [(i, get_num_from_cat(i, devices_with_categories_info)) for i in
                     list(devices_with_categories_info.keys())]
    return {"category_list": category_list}


async def get_equipment_from_cat(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    equipment_list = [(i, get_num_from_name(i, devices_with_categories_info)) for i in
                      devices_with_categories_info[dialog_manager.dialog_data.get('current_category')]]
    return {"equipment_list": equipment_list}


async def get_numbers_of_eq(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    numbers_list = [(str(i), i) for i in range(101)]
    return {"numbers_list": numbers_list}


async def get_numbers_of_postamats(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    numbers_list = [(str(i), i) for i in range(6)]
    return {"numbers_list": numbers_list}


async def get_adding_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    if dialog_manager.middleware_data.get("basket_collection").get(dialog_manager.dialog_data.get('chosen_id')) is not None:
        eq = dialog_manager.dialog_data.get('chosen_equipment')
        num = dialog_manager.dialog_data.get('chosen_number')
        return {"status": f'{eq}, {num} шт успешно добавлено в корзину'}
    else:
        return {"status": 'Не удалось добавить в корзину, попробуйте позже'}

