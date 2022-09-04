from aiogram import types, Dispatcher
from loguru import logger

from common_obj import bot
from keyboards import kb_action_bill
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.Postgres import Postgres
from processes import common_handlers
from processes.Bill import change_bill
from keyboards.bill_kb import generate_bill_btn
from entity.Bill.Bill import Bill


class FSMReadingBill(StatesGroup):
    bill_name = State()
    action = State()


async def read_fsm_bill(message: types.Message):
    with Postgres() as (conn, cursor):
        cursor.execute(f""" SELECT *
                            FROM bill
                            where user_id = {message.from_user.id};""")

        result = cursor.fetchall()

    logger.info(f'select from user bills: {result}')

    bills = [x['bill_name'] for x in result]

    if len(bills) > 0:
        kb_read_bill = generate_bill_btn(bills, 3)

        await FSMReadingBill.bill_name.set()
        await bot.send_message(message.from_user.id,
                            'Какой счёт посмотрим?',
                            reply_markup=kb_read_bill)
    else:
        await Bill.create_bill_from_oth_proc(bot=bot, message=message)

async def cancel_read_bill(message: types.Message, state: FSMContext):
    await common_handlers.cancel_process(message=message, state=state)


async def choose_bill(message: types.Message, state: FSMContext):

    result = await Bill.get_user_bills(message)

    async with state.proxy() as data:
        data['bill_id'] = result["bill_id"]
        data['bill_name'] = result["bill_name"]
        data['acc_balance'] = result["acc_balance"]
        data['is_calc'] = result["is_calc"]

    await FSMReadingBill.next()
    await bot.send_message(message.from_user.id,
                           (f"""Название: {result["bill_name"]}
                            Баланс: {result["acc_balance"]}
                            {result["is_calc"]}""".replace("  ", "")),
                           reply_markup=kb_action_bill)


async def choose_action(message: types.Message, state: FSMContext):
    
    if message.text == 'Изменить':
        async with state.proxy() as data:
            message.text = data["bill_name"]

        await change_bill.FSMChangingBill.bill_name.set()
        await change_bill.choose_bill(message, state)

    elif message.text == 'В начало':
        await state.finish()
        await common_handlers.to_start(message, state)


def reg_processes_bill_read(dp: Dispatcher):
    dp.register_message_handler(read_fsm_bill, state=None)
    dp.register_message_handler(cancel_read_bill, regexp='Отмена', state='*')
    dp.register_message_handler(choose_bill, state=FSMReadingBill.bill_name)
    dp.register_message_handler(choose_action, state=FSMReadingBill.action)
