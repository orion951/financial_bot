from entity.Users import UserProcess
from aiogram import types, Dispatcher

async def random_message(message: types.Message):
    user = UserProcess()
    await user.create_process(message)


def reg_handlers_client(dp:Dispatcher):
    dp.register_message_handler(random_message)