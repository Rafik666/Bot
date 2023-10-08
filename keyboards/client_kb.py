from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
b1 = KeyboardButton('Профиль')
b2 = KeyboardButton('Топ')
b3 = KeyboardButton('Рулетка')
b4 = KeyboardButton('Колесо_фартуны')
b5 = KeyboardButton('Слоты')

kb_client_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_menu.row(b1, b2).row(b3, b4, b5)


r1 = KeyboardButton('Черный')
r2 = KeyboardButton('Красный')
r3 = KeyboardButton('Зеленый')

kb_client_roulettez = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_roulettez.row(r1, r2, r3)

c1 = KeyboardButton('Результат')

kb_client_cont = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client_cont.add(c1)
