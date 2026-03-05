from aiogram.fsm.state import StatesGroup, State


class CustomPlan(StatesGroup):
    choosing_nt = State()
    choosing_ot = State()