from entity.Entity import EntityProcess
from processes.AccChange import create_fsm_acc_change


class AccChangeProcess(EntityProcess):

    async def create_process(self, message):
        await create_fsm_acc_change(message)

    async def read_process(self):
        pass

    async def update_process(self):
        pass

    async def delete_process(self):
        pass
