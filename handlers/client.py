from entity.Users import UserProcess
from aiogram import types, Dispatcher
from common_obj import bot
from keyboards.client_kb import kb_start


async def start(message: types.Message):
    user = UserProcess()
    await user.create_process(message)


async def random_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'Для работы с ботом нажми Старт', reply_markup=kb_start)


def reg_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start, regexp='Старт')
    dp.register_message_handler(random_message)