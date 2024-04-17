import os

import aiosmtplib


class SMTPClient:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER')
        self.smtp_port = os.environ.get('SMTP_PORT')
        self.username = os.environ.get('SMTP_USERNAME')
        self.password = os.environ.get('SMTP_PASSWORD')
        self.server = None

    async def connect(self):
        self.server = aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True)
        await self.server.connect()
        await self.server.login(self.username, self.password)

    async def send(self, msg):
        return await self.server.send_message(self.username, msg)

    async def close(self):
        if self.server:
            await self.server.quit()
            self.server = None


smtp_client = SMTPClient()
