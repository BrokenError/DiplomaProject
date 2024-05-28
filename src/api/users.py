from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile, Form

from apps.users.schemas import UserOut, UserIn, UserAuthenticate, TokenOut, TokenIn, UserUpdate
from apps.users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    path='',
    response_model=UserOut,
    name='Get user',
    description='Get user',
    operation_id='Get user',
    tags=['Users'],
)
async def get(
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    return await user_service.get()


@router.post(
    path='/send-authentication-code',
    name='send authentication code',
    description='send authentication code',
    tags=['Users'],
)
async def send_message(
        data: UserIn,
        user_service: UserService = Depends(UserService.from_request_protected)
):
    await user_service.send_message_email(email=data.email)
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
        user_service: UserService = Depends(UserService.from_request_protected)
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
        user_service: UserService = Depends(UserService.from_request_protected)
) -> TokenOut:
    return await user_service.get_valid_token(data=data)


@router.put(
    path='',
    response_model=UserOut,
    name='Update user',
    description='Update user',
    tags=['Users']
)
async def update(
        photo: Optional[UploadFile] = File(None),
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        phone_number: Optional[str] = Form(None),
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    data = UserUpdate(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )
    return await user_service.update(data=data, photo=photo)


@router.delete(
    path='',
    response_model=UserOut,
    name='Delete user',
    description='Delete user',
    tags=['Users']
)
async def delete(
        user_service: UserService = Depends(UserService.from_request_private)
) -> UserOut:
    return await user_service.delete(id_instance=None)


@router.delete(
    path='/photo',
    name='Delete photo user',
    description='Delete photo user',
    tags=['Users']
)
async def delete(
        user_service: UserService = Depends(UserService.from_request_private)
):
    return await user_service.delete_photo()