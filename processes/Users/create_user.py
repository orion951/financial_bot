from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from common_obj import bot
from database import Postgres, db
from processes import client


class FSMCreationUser(StatesGroup):
    user_name = State()


async def create_fsm_user(message: types.Message):
    with Postgres() as (con, cursor):
        cursor.execute(f""" SELECT *
                            FROM users
                            where user_id = {message.from_user.id} ;""")

        result = cursor.fetchall()[0]

    if cursor.rowcount == 0:
        await FSMCreationUser.user_name.set()
        await bot.send_message(message.from_user.id,
                               'Привет! Мы еще не знакомы.\
                               Как мне тебя называть?')
    else:
        await client.start_fsm_action(message, result['user_name'])


async def set_name(message: types.Message, state: FSMContext):

    with Postgres() as (conn, cursor):
        db.insert('bill', {'user_id': message.from_user.id,
                           'telegram_name': message.from_user.full_name,
                           'user_name': message.text},
                  cursor=cursor, conn=conn)

    await state.finish()
    await client.start_fsm_action(message, message.text)


def reg_processes_user(dp: Dispatcher):
    dp.register_message_handler(create_fsm_user, state=None)
    dp.register_message_handler(set_name, state=FSMCreationUser.user_name)
