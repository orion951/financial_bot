from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loguru import logger

from common_obj import bot
from database import Postgres, db
from processes import common_handlers
from keyboards import common_kb, acc_change_kb
from entity.Bill.Bill import Bill
from entity.Category.Category import Category


class FSMCreationAccChange(StatesGroup):
    type = State()
    bill = State()
    category = State()
    amount = State()
    action = State()

async def create_fsm_acc_change(message: types.Message):
    await FSMCreationAccChange.type.set()

    await bot.send_message(message.from_user.id, 'Что будем вносить?', reply_markup=acc_change_kb.kb_acc_change)

async def cancel_create(message: types.Message, state: FSMContext):
    await common_handlers.cancel_process(message=message, state=state)


async def set_type(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        if message.text == 'Расход':
            data['type'] = 'e'
        else:
            data['type'] = 'i'

        data['type_name'] = message.text

    await Bill.get_all_user_bills(bot, message, FSMCreationAccChange.bill, 'Выбери счёт')


async def set_bill(message: types.Message, state: FSMContext):

    result = await Bill.get_bill(message)

    async with state.proxy() as data:
        data['bill_id'] = result["bill_id"]
        data['bill_name'] = message.text

    await Category.get_all_user_cats(bot, message, FSMCreationAccChange.category, 'Выбери категорию', True)


async def set_category(message: types.Message, state: FSMContext):

    with Postgres() as (conn, cursor):
        cursor.execute(f""" SELECT cat_id
                            FROM category
                            WHERE user_id = {message.from_user.id}
                              AND cat_name = '{message.text}';""")

        category = cursor.fetchall()[0]

    async with state.proxy() as data:
        data['cat_id'] = category[0]
        data['cat_name'] = message.text

    await FSMCreationAccChange.next()

    await bot.send_message(message.from_user.id,
                           'Введи сумму',
                           reply_markup=common_kb.kb_to_start)


async def set_amount(message: types.Message, state: FSMContext):
    with Postgres() as (conn, cursor):
        cursor.execute(f""" SELECT max(acc_change_id)
                            FROM acc_change
                            WHERE user_id = {message.from_user.id};""")

        acc_change_id = cursor.fetchall()[0]
        logger.info(f'acc_change_id = {acc_change_id}')
        if acc_change_id[0] == None:
            acc_change_id[0] = 0

    async with state.proxy() as data:
            data['acc_change'] = int(acc_change_id[0]) + 1

    with Postgres() as (conn, cursor):
        db.insert('acc_change', {'acc_change_id': data['acc_change'],
                                 'amount': int(float(message.text) * 100),
                                 'cat_id': data['cat_id'],
                                 'bill_id': data['bill_id'],
                                 'user_id': message.from_user.id,
                                 'type': data['type']},
                  cursor=cursor, conn=conn)

    await bot.send_message(message.from_user.id,
                           f"""Готово!\n{data['type_name']}:\n\n{int(float(message.text) * 100)} 
                           со счёта '{data['bill_name']}' 
                           в категории '{data['cat_name']}' """.replace("  ", ""))

    await bot.send_message(message.from_user.id, 'Что дальше?', reply_markup=acc_change_kb.kb_end_acc_change)


async def choose_action(message: types.Message, state: FSMContext):
    
    if message.text == 'Расход' or message.text == 'Доход':
        await FSMCreationAccChange.type.set()
        await set_type(message, state)
    elif message.text == 'В начало':
        await state.finish()
        await common_handlers.to_start(message, state)

def reg_processes_acc_change_create(dp: Dispatcher):
    dp.register_message_handler(create_fsm_acc_change, state=None)
    dp.register_message_handler(cancel_create, regexp='Отмена', state='*')
    dp.register_message_handler(set_type, state=FSMCreationAccChange.type)
    dp.register_message_handler(set_bill, state=FSMCreationAccChange.bill)
    dp.register_message_handler(set_category, state=FSMCreationAccChange.category)
    dp.register_message_handler(set_amount, state=FSMCreationAccChange.amount)
    dp.register_message_handler(choose_action, state=FSMCreationAccChange.action)
