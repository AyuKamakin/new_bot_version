from aiogram.fsm.state import StatesGroup, State


class Return_Request_SG(StatesGroup):
    start = State()
    show_return_basket = State()
    sent_for_return_confirmed_message = State()
    send_return_requests = State()
    show_chosen_request = State()
    show_in_usage = State()
    choose_postamat = State()
    delition_confirmation = State()
    added_to_basket_message = State()
    show_chosen_in_usage = State()
    create_comment = State()
    choose_rating = State()
    update_rating = State()
    update_postamat = State()
    update_comment = State()