import asyncio
import logging
import os
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin.accessories import AccessoryAdmin
from admin.laptops import LaptopAdmin
from admin.likedproduct import LikedProductAdmin
from admin.orderitems import OrderItemAdmin
from admin.orders import OrderAdmin
from admin.products import ProductAdmin
from admin.providers import ProviderAdmin
from admin.reviews import ReviewAdmin
from admin.smartphones import SmartphoneAdmin
from admin.smartwatches import SmartwatchAdmin
from admin.tablets import TabletAdmin
from admin.television import TelevisionAdmin
from admin.user import UserAdmin
from api.router import router
from db.database import engine
from settings import settings_app

# from starlette.middleware.gzip import GZipMiddleware

logging.config.fileConfig(
    os.path.join(os.path.dirname(__file__), 'logging.conf'),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)

app = FastAPI(title='Магазин TechZone')
# app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(router, prefix='/api/v1')

admin = Admin(app, engine)

admin.add_view(ProductAdmin)
admin.add_view(AccessoryAdmin)
admin.add_view(LaptopAdmin)
admin.add_view(SmartphoneAdmin)
admin.add_view(SmartwatchAdmin)
admin.add_view(TelevisionAdmin)
admin.add_view(TabletAdmin)
admin.add_view(UserAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(LikedProductAdmin)
admin.add_view(ProviderAdmin)
admin.add_view(ReviewAdmin)


async def start_consuming():
    asyncio.get_event_loop()


if __name__ == '__main__':

    uvicorn.run('main:app', host=settings_app.SERVER_HOST, port=settings_app.SERVER_PORT, debug=True, reload=True)
    # process_app = mp.Process(
    #     target=uvicorn.run,
    #     args=('main:app',),
    #     kwargs={
    #         "host": settings_app.SERVER_HOST,
    #         "port": settings_app.SERVER_PORT,
    #         "debug": True,
    #         "reload": True,
    #     }
    # )
    # process_app.start()
