from aiogram import Dispatcher, types
from create_bot import dp, bot
from date_base import sqlite_db
from machine import machine_condition as machine
from games import arithmetic
from keyboards import kb_client_roulettez, kb_client_menu, kb_client_cont
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

import random

from_roulettez = ['Рулетка крутиться, бабосы мутятся', 'Вращайте барабан']
numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,
           18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]

async def roulettez_start(message: types.Message):
    await message.reply(random.choice(from_roulettez))
    await machine.FSMRoulettez.bid_money.set()
    await message.reply("Введите какую ставку хотите сделать", reply_markup=ReplyKeyboardRemove())

#Начало диалога
#@dp.message_handler(content_types=['text'], state=machine.FSMRoulettez.bid_money)
async def load_bid_money(message: types.Message, state: machine.FSMContext):
    async with state.proxy() as data:
        try:
            data['bid_money'] = int(message.text)
            await machine.FSMRoulettez.next()
            await message.reply("""Теперь введите на что будете делать ставку:
цвет(красный, черный, зеленый)/номер(0-36)""", reply_markup=kb_client_roulettez)
        except:
            await message.reply("Введите число!")

    

#Ловим ответ
#@dp.message_handler(state=machine.FSMRoulettez.bid)
async def load_bid(message: types.Message, state: machine.FSMContext):
    async with state.proxy() as data:
        
        #проверка на текст(ставку)
        if message.text.lower() == "черный" or message.text.lower() =="красный" or message.text.lower() == 'зеленый':
            data['bid'] = message.text    
    
            await machine.FSMRoulettez.next()
            await message.reply('Ставка сделана', reply_markup=kb_client_cont)
            arithmetic.subtraction(sqlite_db, message.from_user.id, int(data['bid_money']))
        
        #проверка на номер(ставку)
        elif message.text.isdigit():
            if int(message.text) >=0 and int(message.text) <=36: 
                data['bid'] = message.text    
        
                await machine.FSMRoulettez.next()
                await message.reply('Ставка сделана', reply_markup=kb_client_cont)
                arithmetic.subtraction(sqlite_db, message.from_user.id, int(data['bid_money']))
            else:
                await message.answer("Число должен быть в промежутке 0~36")
        

        else:
            await message.answer("Выбрали неверный цвет *пишите 'ё' как букву'е'*")
        
        
        
        
#Расчет
#@dp.message_handler(state=machine.FSMRoulettez.win_money)   
async def send_result(message: types.Message, state: machine.FSMContext):

    v_int = int(random.choice(numbers))
    v_color = random.choice(['черный', 'красный','зеленый'])
        
    
    async with state.proxy() as data:
        prize = 0
        if data['bid'].isdigit():
            if int(data['bid']) == v_int:
                if v_int == 0:
                    coefficient = 5
                else:
                    coefficient = 2
                prize = int(data['bid_money'])*coefficient
                arithmetic.addition(sqlite_db, message.from_user.id, prize)
                await message.answer("Поздравляю! Ваш выигрышь "+prize, reply_markup=kb_client_menu)  
                
        if data['bid'].lower() == v_color:
            if v_color == 'зеленый':
                coefficient = 3
            else:
                coefficient = 2
            prize = int(data['bid_money'])*coefficient

            arithmetic.addition(sqlite_db, message.from_user.id, prize)
            await message.answer("Поздравляю! Ваш выигрышь: "+str(prize), reply_markup=kb_client_menu)
        else:
            if data['bid'].isdigit():
                result = v_int
            else:
                result = v_color
            await message.answer("К сожалению, вы проиграли\n"+'Выпало: '+ str(result), reply_markup=kb_client_menu)
        
        data['win_money'] = prize
        arithmetic.winnings_money(sqlite_db, message.from_user.id, data['win_money'])
    await state.finish()

#Отмена
#@dp.message_handler(state='*', commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: machine.FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

    

def register_hendlers_roulettez(dp : Dispatcher):
    dp.register_message_handler(roulettez_start, commands=['рулетка', 'roulettez'])
    dp.register_message_handler(load_bid_money, content_types=['text'], state=machine.FSMRoulettez.bid_money)
    dp.register_message_handler(load_bid, state=machine.FSMRoulettez.bid)
    dp.register_message_handler(send_result, state=machine.FSMRoulettez.win_money)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')