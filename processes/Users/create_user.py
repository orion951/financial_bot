from aiogram import types, Dispatcher
from common_obj import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.Postgres import Postgres
from database import db

from processes import client

class FSMCreationUser(StatesGroup):
    user_name = State()


async def create_fsm_user(message: types.Message):
    with Postgres() as (con, cursor):
        query = """ SELECT * FROM users where user_id = %s ;"""
        values = [message.from_user.id]
        cursor.execute(query, values)
        result = cursor.fetchall()
        print(result)
    if cursor.rowcount == 0:
        await FSMCreationUser.user_name.set()
        await bot.send_message(message.from_user.id, 'Привет! Мы еще не знакомы. Как мне тебя называть?')
    else:
        await client.start_fsm_action(message, message.text)

async def set_name(message: types.Message, state: FSMContext):

    with Postgres() as (con, cursor):
        query = """ INSERT INTO users (user_id, telegram_name, user_name) VALUES (%s, %s, %s)"""
        values_tuple = (message.from_user.id, message.from_user.full_name, message.text)
        cursor.execute(query, values_tuple)

    await state.finish()
    await client.start_fsm_action(message, message.text)
    

def reg_processes_user(dp:Dispatcher):
    dp.register_message_handler(create_fsm_user, state=None)
    dp.register_message_handler(set_name, state=FSMCreationUser.user_name)