from aiogram import types

from loguru import logger

from database import Postgres
from processes.Bill import create_bill

class Bill():

    @staticmethod
    async def write_name(message: types.Message):

        with Postgres() as (con, cursor):
            query = f""" SELECT *
                         FROM bill
                         WHERE user_id = {message.from_user.id} ;"""
            cursor.execute(query)

            result = cursor.fetchall()

        cancel = False
        bill_id = 0

        for row in result:
            if bill_id < row['bill_id']:
                bill_id = row['bill_id']
            if row['bill_name'] == message.text:
                cancel = True

        return {'cancel': cancel, 'bill_id': bill_id}

    @staticmethod
    async def get_user_bills(message: types.Message):
        with Postgres() as (conn, cursor):
            cursor.execute(f""" SELECT *
                                FROM bill
                                WHERE bill_name = '{message.text}'
                                  AND user_id = {message.from_user.id};""")

            result = cursor.fetchall()[0]
            logger.info(f'select from user bill names: {result}')

        acc_balance = float(result['acc_balance'] / 100)
        logger.info(f'acc_balance: {acc_balance}')

        if result['is_not_calc']:
            is_calc = 'Не учитывается в общем балансе'
        else:
            is_calc = 'Учитывается в общем балансе'


        return {'bill_id': result['bill_id'],
                'bill_name': result['bill_name'],
                'acc_balance': acc_balance,
                'is_calc': is_calc}

    @staticmethod
    async def create_bill_from_oth_proc(bot, message):
        await bot.send_message(message.from_user.id,
                               ' '.join('''Пока нет доступных счетов(. 
                                           Давайте создадим, 
                                           а потом делайте с ним что хотите'''.split()))
        await create_bill.create_fsm_bill(message)
