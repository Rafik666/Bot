from pathlib import Path
import asyncio
from aiogram import Dispatcher, types
from create_bot import dp, bot
from date_base import sqlite_db
from machine import machine_condition as machine
from games import arithmetic,cancel_bid
from keyboards import bits
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from games import num_let



import random


import tracemalloc

# Включаем tracemalloc
tracemalloc.start()

# Получаем текущую директорию, где находится ваш скрипт
current_directory = Path(__file__).resolve().parent.parent

# Собираем путь к гифке, предполагая, что она находится в двух папках выше
GIF_PATH1 = (current_directory / 'material/rlt1.mp4').resolve()
GIF_PATH2 = (current_directory / 'material/rlt2.mp4').resolve()
gif = [GIF_PATH1, GIF_PATH2]
#список ставок
list_players = {}
numbers_player = 1


from_roulettez = ['Рулетка крутиться, бабосы мутятся', 'Вращайте барабан']
numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12]
colors = ["🔴", "💚", "⚫️"]

id_bot_mess = []
async def send_message(callback, text):
    sent_message = await bot.send_message(chat_id=callback.message.chat.id, text=text)

    id_bot_mess.append(sent_message)

async def delete_message(callback):
    try:
        for sent_message in id_bot_mess:
            await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

async def send_and_delete_gif(callback):
    sent_message = await bot.send_animation(chat_id=callback.message.chat.id, animation=InputFile(random.choice(gif)))
    
    # Ждем 3 секунды
    await asyncio.sleep(3)
    
    # Пытаемся удалить сообщение с гифкой
    try:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=sent_message.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

def bet_countin_number(win_number, bit_pl, user, win_list, range_number, id):
    user_money = 5
    try:
        if win_number in range(int(bit_pl[0]), int(bit_pl[-1])):
            
            win_money = user_money*2
            arithmetic.winnings_money(sqlite_db, id, win_money)
            arithmetic.addition(sqlite_db, id, win_money)
            win_list += f"{user.first_name} выиграл {win_money}  на {range_number}\n"
        else:
            
            arithmetic.losting_money(sqlite_db, id, user_money)
            win_list += f"{user.first_name} на {range_number}\n"
        
    except:
        win_list = bet_countin_color(win_number, bit_pl, user, win_list, id)
    return win_list

def bet_countin_color(win_number, bit_pl, user, win_list, id):
    user_money = 5
    if num_let.num_let[win_number] == bit_pl[-1]:
        win_money = user_money*2
        arithmetic.addition(sqlite_db, id, win_money)
        arithmetic.winnings_money(sqlite_db, id, win_money)
        win_list += f"{user.first_name} выиграл {win_money}  на {bit_pl[-1]}\n"
    else:
        arithmetic.losting_money(sqlite_db, id, user_money)
        win_list += f"{user.first_name} на {bit_pl[-1]}\n"
    return win_list

def add_list_player(id_player, data):
    global numbers_player
    global numbers
    #добавления в список ставок (игроков)
    
    list_players[numbers_player] = {id_player : data}

    sqlite_db.cur.execute(f"SELECT money FROM players WHERE id={id_player}")
    user_money = sqlite_db.cur.fetchone()[0]
    return user_money

async def check_money(user_money, id_player, callback):
   
    #проверка на кол-во денег
    global numbers_player
    global numbers
    if user_money >= 5:   
        arithmetic.subtraction(sqlite_db, id_player, 5)
        if callback.data != "Удвоить" and callback.data != 'Повторить':
            await send_message(callback, text = f"Ставка принята: {callback.from_user.first_name} {callback.data}")

        numbers_player += 1

    else:
        await callback.message.answer(f"Не хватает денег, у вас на счету: {user_money}")

#принятия ставок/работа кнопок от бота
@dp.callback_query_handler()
async def command(callback: types.CallbackQuery):
    #начальная ставка
    

    global numbers_player
    global numbers
    
    #проверка нажатия на ставки
    if (callback.data == "1 - 3" or callback.data == "4 - 6" or 
        callback.data == "7 - 9" or callback.data=="10 - 12"
        or callback.data == "5 на 🔴" or callback.data == "5 на ⚫️"
        or callback.data == "5 на 💚"):

        #добавления в список ставок (игроков)
        user_money = add_list_player(callback.from_user.id, callback.data)

        #проверка на кол-во денег
        await check_money(user_money, callback.from_user.id, callback)

    #Удвоить
    if callback.data == "Удвоить":
        id_player = callback.from_user.id
        double_list = {key: value for key, value in list_players.items()}
        for i in double_list:
            
            for id_for_list in double_list[i].keys(): 
                if id_for_list == id_player:
                    #добавления в список ставок (игроков)
                    user_money = add_list_player(id_player, double_list[i][id_player])
                    #проверка на кол-во денег
                    await check_money(user_money, id_player, callback)

        await send_message(callback, text = f"Все ставки {callback.from_user.first_name} удвоены")
        
                    
    #вращать барабан
    if callback.data == "Крутить":
        if len(list_players) != 0: 
            win_number = random.choice(numbers)

            win_list = f"Рулетка {win_number} {num_let.num_let[win_number]}\n"

            await send_message(callback, f"{callback.from_user.first_name} крутит рулетку")
            asyncio.ensure_future(send_and_delete_gif(callback))
            await asyncio.sleep(3)

            for n in list_players:
                for id in list_players[n]:
                    range_number = list_players[n][id]
                    bit_pl = range_number.split(" ")
                    for id in list_players[n]:
                        user = await bot.get_chat(id)
                        win_list = bet_countin_number(win_number, bit_pl, user, win_list, range_number, id)
                    

            await callback.message.answer(text=win_list)
            list_players.clear()
            await delete_message(callback)
            id_bot_mess.clear()
        elif len(list_players) == 0:
            await callback.message.answer("Ставки еще не делались. Сперва сделайте ставку")
            
#запуск коммандлы рулетки
async def roulettez_start(message: types.Message):
    await message.answer(text="""Минирулетка
Угадайте число из:
0💚
1🔴 2⚫️ 3🔴 4⚫️ 5🔴 6⚫️
7🔴 8⚫️ 9🔴10⚫️11🔴12⚫️
Ставки можно текстом:
10 на красное | 5 на 12""", reply_markup=bits)
    



cancel_bid.register_hendlers_cancel(dp)

def register_hendlers_roulettez(dp : Dispatcher):
    dp.register_message_handler(roulettez_start, Text(equals='Рулетка', ignore_case=True), state="*")
   