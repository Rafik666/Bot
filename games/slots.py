from aiogram import Dispatcher, types
from create_bot import dp
from date_base import sqlite_db
from machine import machine_condition as machine
from games import arithmetic, cancel_bid
from keyboards import kb_client_menu, kb_client_cont
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
import random

elemets_slots = ['🍌', '7️⃣', '🍋', '🍒', '🍓']

async def slots_start(message: types.Message):
    
    await machine.FSMSlots.bid_money.set()
    await message.reply("Введите какую ставку хотите сделать", reply_markup=ReplyKeyboardRemove())

async def load_bid_money(message: types.Message, state: machine.FSMContext):
    async with state.proxy() as data:
        sqlite_db.cur.execute(f"SELECT money FROM players WHERE id={message.from_user.id}")
        user_money = sqlite_db.cur.fetchone()[0]
        
        if message.text.isdigit():    
            if user_money >= int(message.text):
                
                data['bid_money'] = int(message.text)
                await message.reply("Ставка принята!", reply_markup=kb_client_cont)
                await machine.FSMSlots.next()
            else:
                await message.reply("У вас не хватает денег, на вашем счету: "+ str(user_money))

        else:
            await message.reply("Введите число!")
        

async def send_result(message: types.Message, state: machine.FSMContext):
    v1 = random.choice(elemets_slots)
    v2 = random.choice(elemets_slots)
    v3 = random.choice(elemets_slots)
    async with state.proxy() as data:
        prize = 0
        if v1 == v2 or v1 == v3 or v2 == v3:
            if v1 == '7️⃣' and v2 == '7️⃣' and v3 == '7️⃣':
                coefficient = 5
            elif v1 == v2 == v3 != '7️⃣':
                coefficient = 3
            
            elif v1 == v2 or v1 == v3 or v2 == v3:
                coefficient = 2

            prize = int(data['bid_money'])*coefficient
            arithmetic.addition(sqlite_db, message.from_user.id, prize)
            await message.answer("Поздравляю! Ваш выигрышь "+ str(prize)+"\nВыпало: "+ v1+v2+v3 , reply_markup=kb_client_menu)  
        else:
            await message.answer("К сожалению, вы проиграли\n"+'Выпало: '+ v1+v2+v3, reply_markup=kb_client_menu)
        data['win_money'] = prize
        arithmetic.winnings_money(sqlite_db, message.from_user.id, data['win_money'])
    await state.finish()
    

cancel_bid.register_hendlers_cancel(dp)


def register_hendlers_slots(dp: Dispatcher):
    dp.register_message_handler(slots_start, Text(equals='Слоты', ignore_case=True), state="*")
    dp.register_message_handler(load_bid_money, content_types=['text'], state=machine.FSMSlots.bid_money)
    dp.register_message_handler(send_result, state=machine.FSMSlots.win_money)
    