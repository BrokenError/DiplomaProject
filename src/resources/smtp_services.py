import aiosmtplib
from aiosmtplib import SMTPSenderRefused, SMTPServerDisconnected, SMTPConnectError, SMTPRecipientsRefused
from fastapi import HTTPException

from settings import logger, settings_app


class SMTPClient:
    def __init__(self):
        self.smtp_server = settings_app.SMTP_SERVER
        self.smtp_port = settings_app.SMTP_PORT
        self.username = settings_app.SMTP_USERNAME
        self.password = settings_app.SMTP_PASSWORD
        self.server = None

    async def connect(self):
        self.server = aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True)
        try:
            await self.server.connect()
            await self.server.login(self.username, self.password)
        except SMTPConnectError:
            logger.error("Timed out waiting for server ready message")
            raise HTTPException(status_code=504, detail="Время ожидания ответа истекло")

    async def send(self, msg):
        try:
            await self.server.send_message(msg)
            logger.info(f"Message sent to {self.username}")
        except (SMTPSenderRefused, SMTPServerDisconnected) as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail=f'Ошибка отправки сообщения')
        except SMTPRecipientsRefused as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail=f'Неверно указана почта')

    async def close(self):
        try:
            if self.server:
                self.server = None
        except SMTPServerDisconnected:
            logger.info('SMTP server disconnected')


smtp_client = SMTPClient()
