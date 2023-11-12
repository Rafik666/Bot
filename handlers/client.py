from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client_menu
from date_base import sqlite_db
from games import roulettez, slots
from aiogram.dispatcher.filters import Text

#*************Клиентская часть****************#

#приветствие
async def command_start(message: types.Message):
    await message.answer('Привет ' + message.from_user.first_name+"\n"+
                        """Добро пожаловать на MegaLot_Casino, это бесплатный телеграм-казино для развлечения с друзьями(если они есть).
Тут проводять розыгрыши раз в 3 дня. Есть рулетка, колесо фартуны и ...(на стадии разроботки).\n
В Начале ты получаешь 100§""", reply_markup=kb_client_menu)

    #проверка на наличие польщователя в бд    
    sqlite_db.cur.execute(f"SELECT id FROM players WHERE id={message.from_user.id}")
    if sqlite_db.cur.fetchone() is None:
        await sqlite_db.sql_add_command(state=(message.from_user.first_name, message.from_user.id, 100, 0, 0, 0, 0))
    
async def command_show_profile(message: types.Message):
    sqlite_db.cur.execute((f"SELECT * FROM players WHERE id={message.from_user.id}"))
    name, id, money, win_money, lost_money, max_win, max_bit = sqlite_db.cur.fetchone()
    await message.answer(f"{name}\nНалик в кармане: {money}§\nВыиграно: {win_money}§\nПроиграно: {lost_money}§\nМакс. выиграш: {max_win}§\nМакс. ставка: {max_bit}§")

async def rating_users(message: types.Message):
    sqlite_db.cur.execute('SELECT users, money FROM players ORDER BY money DESC')
    result = sqlite_db.cur.fetchall()
    text = ''
    i = 0
    if i != 5:
        for row in result:
            text += row[0] +" - "+str(row[1])+'§\n'
            i += 1        
    await message.answer(text)  



slots.register_hendlers_slots(dp)
roulettez.register_hendlers_roulettez(dp)


def register_hendlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_show_profile, Text(equals='Профиль', ignore_case=True), state="*")
    dp.register_message_handler(rating_users, Text(equals='Топ', ignore_case=True), state="*")
    