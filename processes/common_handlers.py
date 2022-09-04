from aiogram import types

from loguru import logger
from aiogram.dispatcher import FSMContext

from common_obj import bot
from database.Postgres import Postgres
from processes import client


async def cancel_process(message: types.Message, state: FSMContext):
    """Cancel any process and go to the start
       PARAMETERS:  message - last message from user
                    state - state of the process that we are canceling """

    current_state = await state.get_state()
    logger.info(f'Cancel from state "{current_state}"')
    with Postgres() as (con, cursor):
        cursor.execute(f""" SELECT *
                            FROM users
                            WHERE user_id = {message.from_user.id} ;""")

        result = cursor.fetchall()[0]

    await bot.send_message(message.from_user.id, 'Отменил')
    if current_state is None:
        await client.start_fsm_action(message, result['user_name'])

    await state.finish()
    await client.start_fsm_action(message, result['user_name'])


async def to_start(message: types.Message, state: FSMContext):
    """End of process with help command 'To Start'
       and go to choosing enttity
       PARAMETERS:  message - last message from user
                    state - the state of the process that we are canceling """

    with Postgres() as (con, cursor):
        cursor.execute(f""" SELECT *
                            FROM users
                            WHERE user_id = {message.from_user.id};""")

        result = cursor.fetchall()[0]

    logger.info(f'select from users: {result}')

    await state.finish()
    await client.start_fsm_action(message, result['user_name'])
