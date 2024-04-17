from aiogram import Dispatcher
from aiogram_dialog import DialogManager

from Request_classes import Request_collection
from Request_classes.Request_collection import *


async def get_requests_counts(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwargs):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    return {
        'APPROVED': len(request_collection.get_requests_id_by_status(APPROVED)),
        'DECLINED': len(request_collection.get_requests_id_by_status(DECLINED)),
        'PROCEEDING': len(request_collection.get_requests_id_by_status(PROCEEDING)),
        'READY': len(request_collection.get_requests_id_by_status(READY)),
        'IN_USAGE': len(request_collection.get_requests_id_by_status(IN_USAGE)),
        'READY_RETURN': len(request_collection.get_requests_id_by_status(READY_RETURN)),
        'RETURN_DONE': len(request_collection.get_requests_id_by_status(RETURN_DONE)),
        'PROCEEDING_RETURN': len(request_collection.get_requests_id_by_status(PROCEEDING_RETURN)),
    }


async def get_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт, постамат ' + str(i.postamat_id)), i.id,) for i in
                      request_collection.get_requests_by_status(dialog_manager.dialog_data.get("request_status"))]
    return {"equipment": equipment_list}


async def get_in_usage_requests_list(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    equipment_list = [(str(i.equipment + ' ' + str(i.number) + ' шт'), i.id) for i in
                      request_collection.get_requests_by_status(dialog_manager.dialog_data.get("request_status"))]
    return {"equipment": equipment_list}


async def get_request_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    req = request_collection[dialog_manager.dialog_data.get("current_request_id")]
    status = ''
    if req.status == APPROVED:
        status = 'Одобрен'
    elif req.status == READY:
        status = 'Ожидает получения'
    elif req.status == DECLINED:
        status = 'Отклонен'
    elif req.status == PROCEEDING:
        status = 'В обработке'
    elif req.status == IN_USAGE:
        status = 'Оборудование в пользовании'
    elif req.status == PROCEEDING_RETURN:
        status = 'В обработке на возврат'
    elif req.status == READY_RETURN:
        status = 'Возможно вернуть в указанный постамат'
    elif req.status == RETURN_DONE:
        status = 'Оборудование успешно возвращено'
    return {"id": req.id,
            "equipment": req.equipment,
            "number": req.number,
            "status": status,
            "postamat": req.postamat_id}


# сделать еще одну проверку
async def get_deleted_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("current_request_id")
    request_collection: Request_collection = dialog_manager.middleware_data.get("request_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["успешно удален", "не удалось удалить, попробуйте позже"]
    #if request_collection.get(curr_id) is not None:
        #return {'status': phrases[1], 'id': curr_id}
    #else:
    return {'status': phrases[0], 'id': curr_id}


async def get_added_req_info(dialog_manager: DialogManager, dispatcher: Dispatcher, **kwarg):
    curr_id = dialog_manager.dialog_data.get("current_request_id")
    basket_return_collection: Request_collection = dialog_manager.middleware_data.get("basket_return_collection")[
        int(dialog_manager.event.from_user.id)]
    phrases = ["успешно добавлен в список возврата", "не удалось добавить в список возврата, попробуйте позже"]
    if basket_return_collection.get(curr_id) is None:
        return {'status': phrases[1], 'id': curr_id}
    else:
        return {'status': phrases[0], 'id': curr_id}
