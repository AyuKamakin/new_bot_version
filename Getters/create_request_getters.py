from aiogram import Dispatcher
from aiogram_dialog import DialogManager

from Request_classes import Request_collection
from encoding import get_num_from_name, get_num_from_cat, find_similar_strings, merge_lists_from_dict
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
    basket_collection: Request_collection = dialog_manager.middleware_data.get("basket_collection")[int(dialog_manager.event.from_user.id)]
    if basket_collection.get(
            dialog_manager.dialog_data.get('chosen_id')) is not None:
        eq = dialog_manager.dialog_data.get('chosen_equipment')
        num = dialog_manager.dialog_data.get('chosen_number')
        return {"status": f'{eq}, {num} шт успешно добавлено в корзину'}
    else:
        return {"status": 'Не удалось добавить в корзину, попробуйте позже'}


async def get_delition_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_collection: Request_collection = dialog_manager.middleware_data.get("basket_collection")[int(dialog_manager.event.from_user.id)]
    if basket_collection.get(int(
            dialog_manager.dialog_data.get('request_to_change_id'))) is None:
        return {"status": 'Успешно удалено из корзины'}
    else:
        return {"status": 'Удалить не удалось, попробуйте снова позже'}


async def get_sent_status(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_collection: Request_collection = dialog_manager.middleware_data.get("basket_collection")[int(dialog_manager.event.from_user.id)]
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[int(dialog_manager.event.from_user.id)]
    for i in list(basket_collection.keys()):
        if i not in list(request_collection.keys()):
            return {"status": 'Отправить не удалось, попробуйте позже'}
    basket_collection.clear()
    return {"status": 'Запрос успешно отправлен!'}


async def get_found_equipment(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    eq_list = [(name, get_num_from_name(name, devices_with_categories_info)) for name in \
               find_similar_strings(str(dialog_manager.dialog_data.get('equipment_to_search')),
                                    merge_lists_from_dict(devices_with_categories_info))]
    return {"found_eq_list": eq_list}


async def get_changable_request_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_collection: Request_collection = dialog_manager.middleware_data.get("basket_collection")[int(dialog_manager.event.from_user.id)]
    print(dialog_manager.dialog_data.get("request_to_change_id"))
    req = basket_collection[int(dialog_manager.dialog_data.get("request_to_change_id"))]
    return {"id": req.id,
            "equipment": req.equipment,
            "number": req.number,
            "postamat": req.postamat_id}


async def get_basket_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    basket_collection: Request_collection = dialog_manager.middleware_data.get("basket_collection")[int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      basket_collection.values()]
    return {"equipment": equipment_list}
