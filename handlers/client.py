from aiogram import types, Dispatcher
from common_obj import dp, bot
from keyboards import kb_client, kb_action
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from entity import Bill,Expenses
 

class FSMAction(StatesGroup):
    entity = State()
    actions = State()


async def start_fsm_action(message: types.Message):
    await FSMAction.entity.set()
    await bot.send_message(message.from_user.id, 'С чем будем работать?', reply_markup=kb_client)


async def choose_entity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['entity'] = message.text
    await FSMAction.next()
    await bot.send_message(message.from_user.id, 'Что будем делать?', reply_markup=kb_action)


async def choose_action(message: types.Message, state: FSMAction):
    async with state.proxy() as data:
        if data['entity'] == 'Счета':
            entity = Bill()
        elif data['entity'] == 'Расходы':
            entity = Expenses()

    if message.text in 'Создать':
        entity.create()

    await state.finish()


def reg_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start_fsm_action, state=None)
    dp.register_message_handler(choose_entity, state=FSMAction.entity)
    dp.register_message_handler(choose_action, state=FSMAction.actions)

