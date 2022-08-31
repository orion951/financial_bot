from aiogram import types, Dispatcher

from loguru import logger
from aiogram.dispatcher import FSMContext

from common_obj import bot
from database.Postgres import Postgres
from database import db
from processes import client


async def cancel_process(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(f'Cancel from state "{current_state}"')
    with Postgres() as (con, cursor):
        query = """ SELECT * FROM users where user_id = %s ;"""
        values = [message.from_user.id]
        cursor.execute(query, values)
        result = cursor.fetchall()

    await bot.send_message(message.from_user.id, 'Отменил')
    if current_state == None:
        await client.start_fsm_action(message, result[0][2])

    await state.finish()
    await client.start_fsm_action(message, result[0][2])


async def to_start(message: types.Message, state: FSMContext):
    with Postgres() as (con, cursor):
        query = """ SELECT * FROM users where user_id = %s ;"""
        values = [message.from_user.id]
        cursor.execute(query, values)
        result = cursor.fetchall()
        
        logger.info(f'select from users: {result}')

    await state.finish()
    await client.start_fsm_action(message, result[0][2])