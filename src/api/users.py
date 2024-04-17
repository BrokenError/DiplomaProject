from fastapi import APIRouter, Depends

from apps.commons.services.base import ServiceAuthenticate
from apps.users.schemas import UserOut, UserUpdate, UserIn, UserAuthenticate, TokenOut, TokenIn
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
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    return await user_service.get(id_instance=id_user)


@router.post(
    path='/send-authentication-code',
    name='send authentication code',
    description='send authentication code',
    tags=['Users'],
)
async def send_message(
        data: UserIn,
        user_service: UserService = Depends(UserService.from_request)
):
    if data.email:
        await user_service.send_message_email(email=data.email)
    else:
        await user_service.send_message_phone(phone=data.phone)
    return {"status": "success"}


@router.post(
    path='/authentication',
    name='Authentication user',
    description='Authentication user',
    response_model=TokenOut,
    tags=['Users'],
)
async def authenticate(
        data: UserAuthenticate,
        user_service: UserService = Depends(UserService.from_request)
):
    return await user_service.authenticate_user(user_auth=data)


@router.post(
    path='/valid-token',
    name='get valid token',
    description='get valid token',
    response_model=TokenOut,
    tags=['Users'],
)
async def get_valid_token(
        data: TokenIn,
        user_service: UserService = Depends(UserService.from_request)
) -> TokenOut:
    return await user_service.get_valid_token(data=data)


@router.patch(
    path='/{id_user}',
    response_model=UserOut,
    name='Update user',
    description='Update user',
    tags=['Users']
)
async def update(
        id_user: int,
        data: UserUpdate,
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    return await user_service.update(id_instance=id_user, data=data)


@router.delete(
    path='/{id_user}',
    response_model=UserOut,
    name='Delete user',
    description='Delete user',
    tags=['Users']
)
async def delete(
        id_user: int,
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    return await user_service.delete(id_instance=id_user)
