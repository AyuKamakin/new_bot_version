from aiogram.fsm.state import StatesGroup, State


class Create_Request_SG(StatesGroup):
    start = State()
    search_menu = State()
    choose_category = State()
    choose_equipment_by_category = State()
    choose_equipment_by_name = State()
    choose_number = State()
    add_to_basket_confirmation = State()
    successfully_added = State()
    show_basket = State()
    choose_postamat = State()
    send_basket_requests = State()
    baskets_requests_sent_message = State()
