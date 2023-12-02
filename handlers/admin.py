from aiogram import types, Dispatcher
from create_bot import dp, bot
from date_base import sqlite_db
from aiogram.dispatcher.filters import Text
from games import arithmetic


#*************Часть для администрации****************#
def check_user_on_bd(id):
    sqlite_db.cur.execute(f"SELECT id FROM players WHERE id={id}")
    if sqlite_db.cur.fetchone() is None:
        return 0
    return 1

async def check_admin(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Получаем информацию о пользователе в чате
    chat_member = await bot.get_chat_member(chat_id, user_id)

    # Проверяем, является ли пользователь администратором
    if chat_member.status in ['administrator', 'creator']:
        return 1
    else:
        await message.answer('Вы не администратор.')
        return 0

async def get_id(message: types.Message):
    # Проверяем, есть ли упоминание пользователя в сообщении
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        return user_id
    else:
        await message.answer("Пожалуйста, ответьте на сообщение пользователя, чтобы получить его ID.")
        return 0
    
async def transaction(message: types.Message):
    global text
    result = await check_admin(message)
    if result:
        id = await get_id(message)
        if id:
            check_result = check_user_on_bd(id)
            if check_result:
                sqlite_db.cur.execute(f"SELECT money FROM players WHERE id={message.from_user.id}")
                user_money = sqlite_db.cur.fetchone()[0]
                if user_money >= int(text[1]):
                    arithmetic.addition(sqlite_db, id, int(text[1]))
                    arithmetic.subtraction(sqlite_db, message.from_user.id, int(text[1]))
                    await message.answer("Транзакция успешно обработана")
                else:
                    await message.answer("У вас не хватает денег")
                    
            else:
                await message.answer("Этот пользователь не найден в моей базе данных")

async def announcement(message: types.Message):
    global text
    t = ""
    for el in text[1:]:
        t += el + " " 
    sent_message = await message.answer(t)

    # Закрепляем отправленное сообщение
    await bot.pin_chat_message(message.chat.id, sent_message.message_id)



async def split_text(message: types.Message):
    global text
    text = message.text.split()
    if text[0].lower() == "перевод":
        await message.answer("Команда должна выглядеть\nПеревод <кол-во денег>")
        if len(text) == 2:
            await transaction(message)
    if text[0].lower() == "объявление":
        await announcement(message)
        await delete_user_message(message)

async def delete_user_message(message: types.Message):
    # Удаляем сообщение пользователя
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

def register_hendlers_client(dp : Dispatcher):
    dp.register_message_handler(get_id, commands=['get_id'])
    dp.register_message_handler(split_text)
    #dp.register_message_handler(command_show_profile, Text(equals='Профиль', ignore_case=True), state="*")

