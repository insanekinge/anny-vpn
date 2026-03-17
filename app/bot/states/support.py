from aiogram.fsm.state import State, StatesGroup


class SupportRequestState(StatesGroup):
    awaiting_message = State()
