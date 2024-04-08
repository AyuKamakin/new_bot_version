from aiogram.fsm.state import StatesGroup, State


class Create_Request_SG(StatesGroup):
    start = State()
    search_menu = State()
    choose_category = State()
    choose_equipment_by_category = State()
    choose_equipment_by_name = State()
    choose_number = State()
    successfully_added = State()
    show_basket = State()
    choose_postamat = State()
    send_basket_requests = State()
    show_chosen_request = State()
    change_number = State()
    change_postamat = State()
    baskets_requests_sent_message = State()
    delete_req_from_basket = State()
    confirm_deletion = State()
    deletion_confirmed_message = State()
    sent_confirmed_message = State()
    search_equipment_by_name = State()
