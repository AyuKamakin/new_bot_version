from aiogram.fsm.state import StatesGroup, State


class Create_Request_SG(StatesGroup):
    start = State()
    choose_category = State()
    choose_equipment = State()
    choose_number = State()
    add_to_basket_confirmation = State()
    successfully_added = State()
    show_basket = State()
    send_basket_requests = State()
    baskets_requests_sent_message = State()
