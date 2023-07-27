from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
b1 = KeyboardButton('/Профиль')
b2 = KeyboardButton('/Рулетка')
b3 = KeyboardButton('/Колесо_фартуны')

kb_client_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_menu.add(b1).row(b2,b3)


r1 = KeyboardButton('Черный')
r2 = KeyboardButton('Красный')
r3 = KeyboardButton('Зеленый')

kb_client_roulettez = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_roulettez.row(r1, r2, r3)

c1 = KeyboardButton('Результат')

kb_client_cont = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_cont.add(c1)
