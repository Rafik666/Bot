from create_bot import dp
from aiogram.utils import executor
from date_base import sqlite_db

 

async def on_startup(_):
    print("Бот вышел в онлайн")
   
    sqlite_db.sql_start()

from handlers import client, admin


client.register_hendlers_client(dp)
#other.register_handler_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)