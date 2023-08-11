from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#Ставка на рулетку (послеовательность)
class FSMRoulettez(StatesGroup):
    bid_money = State()
    bid = State()
    win_money = State()


class FSMSlots(StatesGroup):
    bid_money = State()
    win_money = State()
    

