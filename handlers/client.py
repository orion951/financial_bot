from aiogram import types, Dispatcher
from common_obj import dp, bot
from keyboards import kb_client


# @dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.answer("Привет!")

async def random_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выбери команду', reply_markup=kb_client)


def reg_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start_command, commands=['start','help'])
    dp.register_message_handler(random_message)
