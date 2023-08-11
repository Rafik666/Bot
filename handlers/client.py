from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client_menu
from date_base import sqlite_db
from games import roulettez, slots

'''*************Клиентская часть****************'''
#приветствие
async def command_start(message: types.Message):
    await message.reply('Привет ' + message.from_user.first_name+"\n"+
                        """Добро пожаловать на MegaLot_Casino, это бесплатный телеграм-казино для развлечения с друзьями(если они есть).
Тут проводять розыгрыши раз в 3 дня. Есть рулетка, колесо фартуны и ...(на стадии разроботки).\n
В Начале ты получаешь 100§""", reply_markup=kb_client_menu)

    #проверка на наличие польщователя в бд    
    sqlite_db.cur.execute(f"SELECT id FROM players WHERE id={message.from_user.id}")
    if sqlite_db.cur.fetchone() is None:
        await sqlite_db.sql_add_command(state=(message.from_user.first_name, message.from_user.id, 100, 0))
    
async def command_show_profile(message: types.Message):
    sqlite_db.cur.execute((f"SELECT * FROM players WHERE id={message.from_user.id}"))
    name, id, money, win_money = sqlite_db.cur.fetchone()
    await message.reply(f"Имя - {name}\nКоличество денег - {money}§\nВыигранные деньги: +{win_money}§")

async def rating_users(message: types.Message):
    sqlite_db.cur.execute('SELECT users, money FROM players ORDER BY money DESC')
    result = sqlite_db.cur.fetchall()
    text = ''
    i = 0
    if i != 5:
        for row in result:
            text += row[0] +" - "+str(row[1])+'§\n'
            i += 1        
    await message.reply(text)  



slots.register_hendlers_slots(dp)
roulettez.register_hendlers_roulettez(dp)


def register_hendlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_show_profile, commands=['Профиль'])
    dp.register_message_handler(rating_users, commands=['Топ'])
    