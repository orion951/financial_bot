from aiogram import types, Dispatcher
from common_obj import bot
from keyboards import kb_close_question
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.Postgres import Postgres
from database import db

class FSMCreationBill(StatesGroup):
    bill_name = State()
    acc_balance = State()
    is_not_calc = State()

async def create_fsm_bill(message: types.Message):
    await FSMCreationBill.bill_name.set()
    await bot.send_message(message.from_user.id, 'Название счета')

async def write_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bill_name'] = message.text
    await FSMCreationBill.next()
    await bot.send_message(message.from_user.id, 'Сколько денег на счете?')


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

    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, str(data))

    with Postgres() as (con, cursor):
        query = """ SELECT * FROM bill where user_id = %s ;"""
        values = [message.from_user.id]
        cursor.execute(query, values)
        # result = db.fetchall("bill", ["*"])
        if cursor.rowcount == 0:
            query = """ INSERT INTO bill (bill_name, acc_balance, is_not_calc, bill_id, user_id) VALUES (%s, %s, %s, %s, %s)"""
            values = [x for x in data.values()]
            values.append(1)
            values.append(message.from_user.id)
            values_tuple = tuple(values)
            cursor.execute(query, values_tuple)
            await bot.send_message(message.from_user.id, f"Готово! Счёт '{data['bill_name']}' создан")
        else:
            result = cursor.fetchall
            print(result)

    await state.finish()
    

def reg_processes_bill(dp:Dispatcher):
    dp.register_message_handler(create_fsm_bill, state=None)
    dp.register_message_handler(write_name, state=FSMCreationBill.bill_name)
    dp.register_message_handler(write_accbalance, state=FSMCreationBill.acc_balance)
    dp.register_message_handler(write_isnotcalc, state=FSMCreationBill.is_not_calc)
