from abc import abstractmethod

from sqlalchemy.sql import Executable, Select


class InterfaceService:
    Model = None

    @abstractmethod
    def select_visible(self, *fields, **conditions) -> Select:
        ...

    @abstractmethod
    async def execute(self, query: Executable):
        ...
