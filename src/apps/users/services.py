import logging
import os
import random
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

from fastapi import HTTPException, UploadFile
from jose import jwt

from apps.commons.basics.exceptions import ExceptionValidation
from apps.commons.services import ServiceBase
from apps.orders.schemas import OrderStatus
from apps.users.schemas import UserIn, UserAuthenticate, TokenIn, UserUpdate
from db.models import User, Order
from resources.redis_services import redis
from resources.smtp_services import smtp_client
from settings import settings_app

logger = logging.getLogger('users')


class UserService(ServiceBase):
    Model = User

    async def get_instance_by_data(self, **conditions: dict) -> Model:
        return (await self.manager.execute(
            self.select_visible(**conditions)
        )).scalars().first()

    async def create(self, *, data: Union[UserIn, dict] = None, data_extra: Optional[dict] = None) -> Model:
        if not data and not data_extra:
            raise ExceptionValidation("'data' and 'data_extra' params are None. Can not create empty instance.")

        if data_extra is None:
            data_extra = dict()

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        user = await self.manager.create(
            self.Model,
            data | data_extra
        )
        await self.manager.session.refresh(user)
        return user

    async def get(self, id_instance: Optional[int] = None) -> Model:
        instance = await self.get_instance(id_instance or self.id_user)
        if not instance:
            raise HTTPException(status_code=404, detail="Такого пользователя не существует")
        instance.photo_url = settings_app.BASE_URL + instance.photo_url
        return instance

    async def update(
        self,
        id_instance: Optional[int] = None,
        *,
        data: Optional[UserUpdate] = None,
        data_extra: Optional[dict] = None,
        photo: Optional[UploadFile] = None
    ) -> Model:
        if photo:
            try:
                file_path = f"{settings_app.PATH_STORAGE_USER._path}/{photo.filename}"
                data.photo_url = photo
                async with open(file_path, "wb") as buffer:
                    buffer.write(await photo.read())
            except Exception:
                logger.error(f'Не удалось загрузить фото пользователя с id = {self.id_user}')

        data = (await self.validate_data(None, data)).dict(exclude_unset=True) if data else dict()

        return await self.manager.update(
            await self.get(id_instance),
            data
        )

    def authorize(self, id_user: int):
        token_access = self.create_token(
            data={"sub": f"{id_user}"}, term=timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        )
        token_refresh = self.create_token(
            data={"sub": f"{id_user}"}, term=timedelta(days=float(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
        )
        return {"token_access": token_access, "token_refresh": token_refresh}

    @staticmethod
    def generate_confirmation_code():
        return random.randint(100000, 999999)

    async def save_confirmation_code(self, data: str):
        code = self.generate_confirmation_code()
        await redis.set(data, code, expire=600)
        return code

    async def send_message_email(self, email: str):
        code = await self.save_confirmation_code(email)

        msg = MIMEMultipart()
        msg['From'] = 'Techzone@wis-techzone.ru'
        msg['To'] = email
        msg['Subject'] = 'Подтверждение регистрации'

        body = (f'Здравствуйте!\n'
                f'Вы получили это письмо, потому что кто-то пытался войти в ваш аккаунт на нашем сайте.'
                f' Если это были вы, пожалуйста, подтвердите вход.\n'
                f'Если это были не вы и вы не пытались войти в аккаунт, проигнорируйте это письмо.\n'
                f'Код для подтверждения входа: {code}.\n\n'
                f'С уважением,'
                f'\nКоманда {settings_app.COMPANY_NAME.capitalize()}')
        msg.attach(MIMEText(body, 'plain'))

        # with open('notification.html', 'r') as file:
        #     template_content = file.read()

        # template_content = template_content.replace('$ACCOUNT', f'{email}')
        # template_content = template_content.replace('$CODE', f'{code}')
        # template_content = template_content.replace('$COMPANY_NAME', f'{settings_app.COMPANY_NAME.capitalize()}')

        # msg.attach(MIMEText(template_content, 'html'))
        await smtp_client.connect()
        await smtp_client.send(msg)
        await smtp_client.close()
        return code

    async def authenticate_user(self, user_auth: UserAuthenticate):
        code = await redis.get(f'{user_auth.email}')
        if str(user_auth.code) != code:
            raise HTTPException(status_code=401, detail='Неверный код')
        data = {"email": f"{user_auth.email}"}
        if not await self.check_exists(**data):
            id_user = (await self.create(data=data)).id
            order = await self.manager.create(
                Order,
                {"status": OrderStatus.CART, "id_user": id_user, "payment_method": "Отсутствует"}
            )
            await self.manager.session.refresh(order)
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
        try:
            decoded_data = jwt.decode(
                data.token_refresh,
                settings_app.SECRET_KEY,
                algorithms=settings_app.ALGORITHM,
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Ваша сессия истекла. Пожалуйста, выполните вход снова.')
        except jwt.JWTError:
            raise HTTPException(status_code=400, detail='Неверный токен')
        data = self.authorize(id_user=decoded_data['sub'])
        return data

    async def delete(self, id_instance: Optional[int] = None) -> Model:
        return await self.manager.update(
            await self.get(self.id_user),
            {
                'is_deleted': True,
            }
        )
