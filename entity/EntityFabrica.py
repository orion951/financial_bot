from xml.dom.minidom import Entity
from entity.Bill import BillProcess
from entity.Acc_change import Acc_changeProcess
from entity.Category import CategoryProcess
from entity.Entity import EntityProcess

class EntityFabrica():

    object : EntityProcess

    @classmethod
    async def create_object(cls, entity) -> EntityProcess:
        if entity == 'Счета':
            cls.object = BillProcess()
        elif entity == 'Расходы' or entity == 'Доходы':
            cls.object = Acc_changeProcess()
        elif entity == 'Категории':
            cls.object = CategoryProcess()

    @classmethod
    async def execute_process(cls, message):
        if message.text in 'Создать':
            await cls.object.create_process(message)
        elif message.text in 'Посмотреть':
            await cls.object.read_process()
        elif message.text in 'Изменить':
            await cls.object.update_process()
        elif message.text in 'Удалить':
            await cls.object.delete_process()