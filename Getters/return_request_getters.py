from aiogram import Dispatcher
from aiogram_dialog import DialogManager
from Request_classes.Request_collection import *


async def get_basket_return_requests_list(dialog_manager: DialogManager, **kwarg):
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      basket_return_collection.values()]
    return {"equipment": equipment_list}


async def get_in_usage_req_info(dialog_manager: DialogManager, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ', ' + str(i.number) + 'шт'), i.id,) for i in
                      request_collection.get_requests_by_status(IN_USAGE)]
    return {"equipment": equipment_list}


async def get_deleted_return_req_info(dialog_manager: DialogManager, **kwarg):
    curr_id = int(dialog_manager.dialog_data.get("chosen_request_id"))
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["Успешно удален", "Не удалось удалить, попробуйте позже"]
    if basket_return_collection.get(curr_id) is not None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}


async def get_added_to_basket_status(dialog_manager: DialogManager, **kwarg):
    curr_id = dialog_manager.dialog_data.get("chosen_request_id")
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["Успешно добавлен в список возврата", "Не удалось добавить, попробуйте позже"]
    if basket_return_collection.get(curr_id) is None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}


async def get_return_sent_status(dialog_manager: DialogManager, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    for i in list(dialog_manager.dialog_data.get('deleted_keys')):
        if request_collection[i].status != PROCEEDING_RETURN:
            return {"status": 'Не удалось отправить запросы на возврат, попробуйте позже'}
    return {"status": 'Запросы на возврат отправлены!'}
