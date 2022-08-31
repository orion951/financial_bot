from aiogram import types, Dispatcher

from loguru import logger
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from common_obj import bot
from keyboards import kb_close_question
from database import Postgres, db
from processes import client, common_handlers
from keyboards import common_kb


class FSMCreationBill(StatesGroup):
    bill_name = State()
    acc_balance = State()
    is_not_calc = State()


async def create_fsm_bill(message: types.Message):
    await FSMCreationBill.bill_name.set()
    await bot.send_message(message.from_user.id, 'Название счета', reply_markup=common_kb.kb_cancel)


async def cancel_create(message: types.Message, state: FSMContext):
    await common_handlers.cancel_process(message=message, state=state)


async def write_name(message: types.Message, state: FSMContext):
    with Postgres() as (con, cursor):
        query = """ SELECT * FROM bill where user_id = %s ;"""
        values = [message.from_user.id]
        cursor.execute(query, values)
        result = cursor.fetchall()
    cancel = False
    bill_id = 0

    for row in result:
        if bill_id < row[0]:
            bill_id = row[0]
        if row[1] == message.text:
            cancel = True
            await bot.send_message(message.from_user.id, 'Счёт с таким именем уже существует')
            await state.finish()
            await create_fsm_bill(message)

    if cancel == False:
        async with state.proxy() as data:
            data['bill_name'] = message.text
            data['bill_id'] = bill_id + 1
        await FSMCreationBill.next()

        await bot.send_message(message.from_user.id, 'Сколько денег на счете?', reply_markup=common_kb.kb_cancel)


async def write_accbalance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['acc_balance'] = int(float(message.text) * 100)
    await FSMCreationBill.next()

    await bot.send_message(message.from_user.id, 'Учитывать этот счёт в общем бюджете?', reply_markup=kb_close_question)


async def write_isnotcalc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Да':
            data['is_not_calc'] = False
        else:
            data['is_not_calc'] = True

    with Postgres() as (conn, cursor):
        db.insert('bill', {'bill_name': data['bill_name'], 
                           'bill_id': data['bill_id'],
                           'acc_balance': data['acc_balance'],
                           'is_not_calc': data['is_not_calc'],
                           'user_id': message.from_user.id}, cursor=cursor, conn=conn)
        # query = """ INSERT INTO bill (bill_name, bill_id, acc_balance, is_not_calc, user_id) VALUES (%s, %s, %s, %s, %s)"""

        # values = [x for x in data.values()]
        # values.append(message.from_user.id)
        # values_tuple = tuple(values)

        # cursor.execute(query, values_tuple)

        await bot.send_message(message.from_user.id, f"Готово! Счёт '{data['bill_name']}' создан")

    await common_handlers.to_start(message=message, state=state)
    

def reg_processes_bill_create(dp:Dispatcher):
    dp.register_message_handler(create_fsm_bill, state=None)
    dp.register_message_handler(cancel_create, regexp='Отмена', state='*')
    dp.register_message_handler(write_name, state=FSMCreationBill.bill_name)
    dp.register_message_handler(write_accbalance, state=FSMCreationBill.acc_balance)
    dp.register_message_handler(write_isnotcalc, state=FSMCreationBill.is_not_calc)
