from entity.Entity import EntityProcess
from database.Postgres import Postgres
from common_obj import bot
from processes.Bill import create_fsm_bill, read_fsm_bill


class BillProcess(EntityProcess):

    async def create_process(self, message):

        await create_fsm_bill(message)

    async def read_process(self, message):
        
        await read_fsm_bill(message)

    async def update_process(self):
        pass

    async def delete_process(self):
        pass
