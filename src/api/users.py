import json

from fastapi import APIRouter, Depends

from apps.users.schemas import UserOut
from apps.users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    path='/{id_user}',
    response_model=UserOut,
    name='Get user',
    description='Get user',
    operation_id='Get user',
    tags=['Users'],
)
async def get(
        id_user: int,
        user_service: UserService = Depends(UserService.from_request)
):
    return await user_service.get(id_instance=id_user)


@router.delete(
    path='/{id_user}',
    response_model=UserOut,
    name='Delete scheduler event',
    description='Delete scheduler event',
    operation_id='delete_event',
    tags=['Users']
)
async def delete(
        id_user: int,
        event_service: UserService = Depends(UserService.from_request)
) -> UserOut:
    return await event_service.delete(id_instance=id_user)
