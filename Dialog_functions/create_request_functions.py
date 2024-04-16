import random

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from Request_classes.Request_collection import PROCEEDING, Request_collection
from SG.Create_Request_SG import Create_Request_SG
from SG.Start_SG import Start_SG
from encoding import get_cat_from_num, get_name_from_num, find_similar_strings, merge_lists_from_dict
from inventory_information import devices_with_categories_info


async def to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Start_SG.menu, mode=StartMode.RESET_STACK)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def go_to_add_equipment(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.search_menu)


async def go_to_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    if len(basket_collection) != 0:
        await manager.switch_to(Create_Request_SG.show_basket)
    else:
        await callback.answer(show_alert=True, text='Корзина пуста!')


async def go_to_send_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.send_basket_requests)


async def go_to_search_by_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.choose_category)


async def go_to_search_by_name(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.search_equipment_by_name)


async def go_to_search_for_equipment(msg: Message, inp: MessageInput, manager: DialogManager):
    manager.dialog_data['equipment_to_search'] = msg.text
    print(msg.text)
    print(find_similar_strings(str(msg.text), merge_lists_from_dict(devices_with_categories_info)))
    if len(find_similar_strings(str(msg.text), merge_lists_from_dict(devices_with_categories_info))) != 0:
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
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[int(callback.from_user.id)]
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    i = random.randint(10000000, 11000000)
    while i in list(request_collection.keys()) or i in list(
            basket_collection.keys()):
        i = random.randint(10000000, 11000000)
    manager.dialog_data['chosen_id'] = i
    basket_collection.create_and_add_request(i,
                                                                            manager.dialog_data.get('chosen_equipment'),
                                                                            PROCEEDING,
                                                                            manager.dialog_data.get('chosen_number'),
                                                                            manager.dialog_data.get('chosen_postamat'),
                                                                            int(callback.from_user.id))
    await manager.switch_to(Create_Request_SG.successfully_added)


async def update_basket_request(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    manager.dialog_data["request_to_change_id"] = button_id
    await manager.switch_to(Create_Request_SG.show_chosen_request)


async def update_num(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    basket_collection[int(manager.dialog_data.get("request_to_change_id"))].number = button_id
    await manager.switch_to(Create_Request_SG.show_chosen_request)


async def update_postamat(callback: CallbackQuery, button: Button, manager: DialogManager, button_id):
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    basket_collection[int(manager.dialog_data.get("request_to_change_id"))].postamat_id = button_id
    await manager.switch_to(Create_Request_SG.show_chosen_request)


async def go_to_update_postamat(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.change_postamat)


async def go_to_local_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.start)


async def go_to_del_from_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.delete_req_from_basket)

#Дописать отправку хапросов
async def send_requests(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    request_collection: Request_collection = manager.middleware_data.get("request_collection")[int(callback.from_user.id)]
    request_collection.copy_all_from_old(basket_collection)
    await manager.switch_to(Create_Request_SG.sent_confirmed_message)


async def delete_chosen_from_basket(callback: CallbackQuery, button: Button, manager: DialogManager):
    basket_collection: Request_collection = manager.middleware_data.get("basket_collection")[int(callback.from_user.id)]
    basket_collection.delete_by_id_list([int(manager.dialog_data.get("request_to_change_id"))])
    await manager.switch_to(Create_Request_SG.deletion_confirmed_message)


async def go_to_show_chosen_request(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.show_chosen_request)


async def go_to_update_num(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Create_Request_SG.change_number)
