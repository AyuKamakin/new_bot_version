import operator
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from Getters.create_request_getters import get_rating_stars
from SG.Return_request_SG import *
from Getters.return_request_getters import *
from Dialog_functions.return_request_functions import *


window_start = Window(
    Const("Для отправки запроса на возврат, перейдите в список возврата и отправьте запрос на возврат"),
    Button(Const("Оборудование в пользовании"), id="to_add_return_equipment", on_click=to_show_in_usage),
    Button(Const("Список возврата, отправка запроса"), id="to_basket", on_click=to_return_basket),
    Button(Const("Вернуться"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.start,
)

window_show_basket = Window(
    Const("Ваш cписок возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=to_show_chosen_request
        ),
        id="equipments",
        width=1,
        height=6,
    ),
    Button(Const("Отправить запрос"), id="to_send_return_request", on_click=to_send_request),
    Button(Const("Вернуться"), id="go_back_101", on_click=to_menu),
    state=Return_Request_SG.show_return_basket,
    getter=get_basket_return_requests_list
)

window_show_in_usage = Window(
    Const("Список оборудования в пользовании"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="equipment",
            id='first',
            on_click=to_show_chosen_in_usage_request
        ),
        id="equipments",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back_101", on_click=to_local_menu),
    state=Return_Request_SG.show_in_usage,
    getter=get_in_usage_req_info
)

window_show_chosen_in_usage = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Button(Const("Вернуть оборудование"), id="add_to_return_basket", on_click=to_choose_postamat),
    Button(Const("Вернуться"), id="to_show_return_reqs", on_click=to_return_basket),
    state=Return_Request_SG.show_chosen_in_usage,
    getter=get_request_in_usage_info
)

window_choose_postamat = Window(
    Const("Доступные постаматы для возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_postamat",
            on_click=choose_postamat_return_dialog
        ),
        id="choose_num",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back100", on_click=to_show_chosen_in_usage_request),
    state=Return_Request_SG.choose_postamat,
    getter=get_numbers_of_postamats
)

window_show_chosen_request = Window(
    Format('Оборудование: {equipment}'),
    Format('Количество: {number} шт'),
    Format('Постамат для возврата: {postamat}'),
    Format('Оценка системы: {rating}⭐'),
    Format('Комментарий: {comment}'),
    Button(Const("Изменить постамат"), id="update_postamat", on_click=to_update_postamat),
    Button(Const("Изменить оценку"), id="update_rating", on_click=to_update_rating),
    Button(Const("Изменить комментарий"), id="update_comment", on_click=to_update_comment),
    Button(Const("Удалить из списка возврата"), id="del_from_return_basket", on_click=to_del_from_return_basket),
    Button(Const("Вернуться"), id="go_back102", on_click=to_return_basket),
    state=Return_Request_SG.show_chosen_request,
    getter=get_request_in_basket_info
)

window_send_confirmation = Window(
    Const('Вы уверены что хотите отправить запрос на возврат используемого оборудования ?'),
    Button(Const("Отправить"), id="send_reqs", on_click=send_requests),
    Button(Const("Вернуться"), id="go_back11", on_click=to_return_basket),
    state=Return_Request_SG.send_return_requests,
)

window_requests_sent_message = Window(
    Format('{status}'),
    Button(Const("Перейти в меню возврата"), id="send_reqs", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="send_reqs", on_click=to_menu),
    state=Return_Request_SG.sent_for_return_confirmed_message,
    getter=get_return_sent_status
)
window_added_message = Window(
    Format('{status}'),
    Button(Const("Перейти в список возврата"), id="to_list_return", on_click=to_return_basket),
    Button(Const("Перейти в меню возврата"), id="to_menu_return", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.added_to_basket_message,
    getter=get_added_to_basket_status
)

window_deleted_message = Window(
    Format('{status}'),
    Button(Const("Перейти в список возврата"), id="to_list_return", on_click=to_return_basket),
    Button(Const("Перейти в меню возврата"), id="to_menu_return", on_click=to_local_menu),
    Button(Const("Перейти в меню"), id="to_menu", on_click=to_menu),
    state=Return_Request_SG.delition_confirmation,
    getter=get_deleted_return_req_info
)

window_choose_rating = Window(
    Const("Поставьте оценку системе"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_rating",
            on_click=set_rating
        ),
        id="choose_rate",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back114", on_click=to_choose_postamat),
    state=Return_Request_SG.choose_rating,
    getter=get_rating_stars
)

window_update_rating = Window(
    Const("Поставьте оценку системе"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_rating",
            on_click=update_rating
        ),
        id="choose_rate",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back115", on_click=to_show_chosen_request),
    state=Return_Request_SG.update_rating,
    getter=get_rating_stars
)

window_create_comment = Window(
    Const('Введите комментарий или нажмите "Продолжить"'),
    MessageInput(comment_created),
    Button(Const("Продолжить"), id="go_on_to_added", on_click=to_added),
    Button(Const("Вернуться"), id="go_back115", on_click=to_choose_rating),
    state=Return_Request_SG.create_comment,
)

window_update_comment = Window(
    Const('Введите комментарий'),
    MessageInput(comment_updated),
    Button(Const("Вернуться"), id="go_back118", on_click=to_show_chosen_request),
    state=Return_Request_SG.update_comment,
)

window_update_postamat = Window(
    Const("Доступные постаматы для возврата"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="numbers_list",
            id="choosing_postamat",
            on_click=update_postamat_return_dialog
        ),
        id="choose_num",
        width=1,
        height=6,
    ),
    Button(Const("Вернуться"), id="go_back100", on_click=to_show_chosen_request),
    state=Return_Request_SG.update_postamat,
    getter=get_numbers_of_postamats
)
dialog_return_request = Dialog(window_added_message, window_requests_sent_message, window_send_confirmation,
                               window_show_chosen_request, window_choose_postamat, window_show_in_usage,
                               window_show_basket, window_start, window_show_chosen_in_usage, window_deleted_message,
                               window_create_comment, window_choose_rating, window_update_comment, window_update_rating, window_update_postamat)
