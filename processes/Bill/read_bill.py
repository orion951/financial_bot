from os import access

from aiogram import types, Dispatcher
from loguru import logger

from common_obj import bot
from keyboards import kb_action_bill
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.Postgres import Postgres
from processes import client, common_handlers
from keyboards.bill_kb import generate_bill_btn
from database import db

class FSMReadingBill(StatesGroup):
    bill_name = State()
    action = State()

async def read_fsm_bill(message: types.Message):
    with Postgres() as (conn, cursor):
        query = """ SELECT * FROM bill where user_id = %s or user_id = %s;"""
        values = [message.from_user.id, 100000000]
        cursor.execute(query, values)
        result = cursor.fetchall()
        logger.info(f'select from user bills: {result}')

    bills = [x[1] for x in result]
    kb_read_bill = generate_bill_btn(bills, 3)
    await FSMReadingBill.bill_name.set()
    await bot.send_message(message.from_user.id, 'Какой счёт посмотрим?', reply_markup=kb_read_bill)


async def cancel_read_bill(message: types.Message, state: FSMContext):
    await common_handlers.cancel_process(message=message, state=state)


async def choose_bill(message: types.Message, state: FSMContext):
    print('hello')
    with Postgres() as (conn, cursor):
        query = """ SELECT * FROM bill where bill_name = %s and (user_id = %s or user_id = %s);"""
        values = [message.text, message.from_user.id, 100000000]
        cursor.execute(query, values)
        result = cursor.fetchall()
        logger.info(f'select from user bill names: {result}')

    acc_balance = float(result[0][2] / 100)
    logger.info(f'acc_balance: {acc_balance}')

    if result[0][3] == True:
        is_calc = 'Не учитывается в общем балансе'
    else:
        is_calc = 'Учитывается в общем балансе'

    await FSMReadingBill.next()
    await bot.send_message(message.from_user.id, f'Название: {result[0][1]}\nБаланс: {acc_balance}\n{is_calc}', reply_markup=kb_action_bill)


async def choose_action(message: types.Message, state: FSMContext): 
    await state.finish()
    if message.text == 'Изменить':
        pass
    elif message.text == 'В начало':
        await common_handlers.to_start(message=message, state=state)


def reg_processes_bill_read(dp:Dispatcher):
    dp.register_message_handler(read_fsm_bill, state=None)
    dp.register_message_handler(cancel_read_bill, regexp='Отмена', state='*')
    dp.register_message_handler(choose_bill, state=FSMReadingBill.bill_name)
    dp.register_message_handler(choose_action, state=FSMReadingBill.action)