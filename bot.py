from aiogram.utils import executor
from common_obj import dp


async def on_startup(_):
    print("Бот запущен")

from handlers import client, admin

client.reg_handlers_client(dp)
    
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)