from keyboards import kb_client_menu
from aiogram import types, Dispatcher
from machine import machine_condition as machine
from aiogram.dispatcher.filters import Text


#Отмена
async def cancel_handler(message: types.Message, state: machine.FSMContext):
    print("отмена")
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK',reply_markup=kb_client_menu)

def register_hendlers_cancel(dp : Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
   