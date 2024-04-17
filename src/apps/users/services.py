import os
import random
import re
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

from fastapi import HTTPException
from jose import jwt

from apps.commons.services import ServiceBase
from apps.users.schemas import UserIn, UserAuthenticate, TokenIn
from db.models import User
from resources.redis_services import redis


class UserService(ServiceBase):
    Model = User

    async def get_instance_by_data(self, **conditions: dict) -> Model:
        return (await self.manager.execute(
            self.select_visible(**conditions)
        )).scalars().first()

    async def create(self, *, data: Union[UserIn, dict] = None, data_extra: Optional[dict] = None) -> Model:
        user = await super().create(data=data, data_extra=data_extra)
        await self.manager.session.refresh(user)
        return user

    def authorize(self, id_user: int):
        token_access = self.create_token(
            data={"sub": f"{id_user}"}, term=timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        )
        token_refresh = self.create_token(
            data={"sub": f"{id_user}"}, term=timedelta(days=float(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
        )
        return {"token_access": token_access, "token_refresh": token_refresh}

    @staticmethod
    def check_datain(data: str):
        if re.match(rf'{os.getenv("EMAIL_REGEX")}', data):
            return {"email": data}
        elif re.match(rf'{os.getenv("PHONE_REGEX")}', data):
            return {"phone": data}
        raise HTTPException(status_code=400, detail="Неверные данные")

    @staticmethod
    def generate_confirmation_code():
        return random.randint(100000, 999999)

    async def save_confirmation_code(self, data: str):
        code = self.generate_confirmation_code()
        await redis.set(data, code, expire=600)
        print(f"Confirmation code: {code}")
        return code

    async def send_message_phone(self, phone: str):
        code = await self.save_confirmation_code(phone)
        ...
        return code

    async def send_message_email(self, email: str):
        code = await self.save_confirmation_code(email)

        msg = MIMEMultipart()
        msg['From'] = 'vvglvv1@gmail.com'
        msg['To'] = email
        msg['Subject'] = 'Подтверждение регистрации'

        body = (f'Здравствуйте!\nВы получили это письмо, потому что кто-то пытался войти в ваш аккаунт на нашем сайте.'
                f' Если это были вы, пожалуйста, подтвердите вход.'
                f'\nЕсли это были не вы и вы не пытались войти в аккаунт, проигнорируйте это письмо.\n '
                f'Код для подтверждения входа: {code}.\nС уважением,\nКоманда {os.getenv("COMPANY_NAME")}')
        msg.attach(MIMEText(body, 'plain'))

        # smtp_client.send(msg)
        return code

    async def authenticate_user(self, user_auth: UserAuthenticate):
        code = await redis.get(f'{user_auth.identifier}')
        if str(user_auth.code) != code:
            raise HTTPException(status_code=401, detail='Неверный код')
        data = self.check_datain(user_auth.identifier)
        if not await self.check_exists(**data):
            id_user = (await self.create(data_extra=data)).id
        else:
            id_user = (await self.get_instance_by_data(**data)).id
        return self.authorize(id_user)

    @staticmethod
    def create_token(data: dict, term: Optional[timedelta]):
        to_encode = data.copy()
        expire = datetime.utcnow() + term
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
        return encoded_jwt

    async def get_valid_token(self, data: TokenIn):
        if not data.token_refresh:
            raise HTTPException(status_code=401, detail='Ваша сессия истекла. Пожалуйста, выполните вход снова.')
        if not data.token_access:
            decoded_data = jwt.decode(
                data.token_refresh,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")],
            )
            data = self.authorize(id_user=decoded_data['sub'])
        return data
