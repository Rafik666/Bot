from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

#Кнопка
bits = InlineKeyboardMarkup(row_width=3)

bit1_3 = InlineKeyboardButton(text="1-3", callback_data="1 - 3")
bit4_6 = InlineKeyboardButton(text="4-6", callback_data="4 - 6")
bit7_9 = InlineKeyboardButton(text="7-9", callback_data="7 - 9")
bit10_12 = InlineKeyboardButton(text="10-12", callback_data="10 - 12")

bit_5_on_red = InlineKeyboardButton(text="5 на 🔴", callback_data="5 на 🔴")
bit_5_on_black = InlineKeyboardButton(text="5 на ⚫️" ,callback_data="5 на ⚫️")
bit_5_on_green = InlineKeyboardButton(text="5 на 💚" ,callback_data="5 на 💚")


but_double = InlineKeyboardButton(text="Удвоить", callback_data="Удвоить")
bur_rotate = InlineKeyboardButton(text="Крутить", callback_data="Крутить")


bits.row(bit1_3, bit4_6, bit7_9, bit10_12).row(bit_5_on_red, bit_5_on_black, bit_5_on_green).row(but_double, bur_rotate)

