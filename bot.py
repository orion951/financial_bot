from aiogram.utils import executor

from common_obj import dp
from processes.client import reg_processes_client 
from processes.Bill.create_bill import reg_processes_bill
from processes.Users.create_user import reg_processes_user
from handlers.client import reg_handlers_client


async def on_startup(_):
    print("Бот запущен")

reg_handlers_client(dp)
reg_processes_bill(dp)
reg_processes_client(dp)
reg_processes_user(dp)

    
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)