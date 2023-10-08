from aiogram import Dispatcher, types
from create_bot import dp, bot
from date_base import sqlite_db
from machine import machine_condition as machine
from games import arithmetic,cancel_bid
from keyboards import bits
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from games import num_let


import random

#список ставок
list_players = {}
numbers_player = 1


from_roulettez = ['Рулетка крутиться, бабосы мутятся', 'Вращайте барабан']
numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12]
colors = ["🔴", "💚", "⚫️"]

def bet_countin_number(win_number, bit_pl, user, win_list, range_number, id):
    try:
        if win_number in range(int(bit_pl[0]), int(bit_pl[-1])):
            win_money = 5*2
            arithmetic.winnings_money(sqlite_db, id, win_money)
            arithmetic.addition(sqlite_db, id, win_money)
            win_list += f"{user.first_name} выиграл {win_money}  на {range_number}\n"
        else:
            win_list += f"{user.first_name} на {range_number}\n"
        
    except:
        win_list = bet_countin_color(win_number, bit_pl, user, win_list, id)
    return win_list

def bet_countin_color(win_number, bit_pl, user, win_list, id):
    if num_let.num_let[win_number] == bit_pl[-1]:
        win_money = 5*2
        arithmetic.addition(sqlite_db, id, win_money)
        arithmetic.winnings_money(sqlite_db, id, win_money)
        win_list += f"{user.first_name} выиграл {win_money}  на {bit_pl[-1]}\n"
    else:
        win_list += f"{user.first_name} на {bit_pl[-1]}\n"
    return win_list

        
    

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
        id_player = callback.from_user.id
        list_players[numbers_player] = {id_player : callback.data}

        sqlite_db.cur.execute(f"SELECT money FROM players WHERE id={id_player}")
        user_money = sqlite_db.cur.fetchone()[0]
        
        #проверка на кол-во денег
        if user_money >= 5:   
            arithmetic.subtraction(sqlite_db, id_player, 5)
            await callback.message.answer(f"Ставка принята: {callback.from_user.first_name} 5 абобиков на {callback.data}")
            numbers_player += 1
        else:
            await callback.message.answer(f"Не хватает денег, у вас на счету: {user_money}")
    
    #вращать барабан
    if callback.data == "Крутить":
        if len(list_players) != 0: 
            win_number = random.choice(numbers)

            win_list = f"Рулетка {win_number} {num_let.num_let[win_number]}\n"

            for n in list_players:
                for id in list_players[n]:
                    range_number = list_players[n][id]
                    bit_pl = range_number.split(" ")
                    for id in list_players[n]:
                        user = await bot.get_chat(id)
                        win_list = bet_countin_number(win_number, bit_pl, user, win_list, range_number, id)
                    

            await callback.message.answer(text=win_list)
            list_players.clear()
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
   