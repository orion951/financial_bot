from entity.Entity import EntityProcess

class Acc_changeProcess(EntityProcess):

    async def create_process(self):
        print('Create bill')

    async def read_process(self):
        print('Show bill')

    async def update_process(self):
        pass

    async def delete_process(self):
        pass