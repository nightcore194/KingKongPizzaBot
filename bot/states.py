from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    register = State()


class StatesAdmin(StatesGroup):
    inputFood = State()
    inputClient = State()
    inputEmployee = State()
    inputPrice = State()
    inputName = State()
    inputPhone = State()
    inputAddress = State()
    inputEnd = State()
    input_info = State()

class StatesCooking(StatesGroup):
    pass


class StatesInfo(StatesGroup):
    inputPrice = State()
    inputRecipe = State()

class StatesReport(StatesGroup):
    inputEndDate = State()
    result = State()
