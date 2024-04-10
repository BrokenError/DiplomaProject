from typing import Optional

from apps.commons.services import ServiceBase
from apps.users.schemas import UserIn
from db.models import User


class UserService(ServiceBase):
    Model = User

    async def create(self, *, data: UserIn = None, data_extra: Optional[dict] = None) -> Model:
        tablet = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(tablet)
        return tablet
