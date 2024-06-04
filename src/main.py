import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqladmin import Admin

from admin.accessories import AccessoryAdmin
from admin.authenticate import authentication_backend
from admin.favourite import FavouriteAdmin
from admin.laptops import LaptopAdmin
from admin.orderitems import OrderItemAdmin
from admin.orders import OrderAdmin
from admin.products import ProductAdmin, PhotosAdmin
from admin.providers import ProviderAdmin
from admin.reviews import ReviewAdmin
from admin.smartphones import SmartphoneAdmin
from admin.smartwatches import SmartwatchAdmin
from admin.tablets import TabletAdmin
from admin.television import TelevisionAdmin
from admin.user import UserAdmin
from api.router import router
from db.database import engine
from resources.redis_services import redis
from settings import settings_app


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis.up()
    yield
    await redis.down()


app = FastAPI(
    title='Магазин TechZone',
    lifespan=lifespan,
    docs_url='/api/v1/docs',
    openapi_url='/api/v1/openapi',
    redoc_url='/api/v1/redoc'
)

app.include_router(router, prefix='/api/v1')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication")

origins = [
    "http://127.0.0.1:5174",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(
    app,
    engine,
    base_url=f"/{settings_app.URL_ADMIN}",
    title=settings_app.COMPANY_NAME,
    authentication_backend=authentication_backend
)

admin.add_view(PhotosAdmin)
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
admin.add_view(FavouriteAdmin)
admin.add_view(ProviderAdmin)
admin.add_view(ReviewAdmin)


async def start_consuming():
    asyncio.get_event_loop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings_app.SERVER_HOST,
        port=settings_app.SERVER_PORT,
        debug=True,
        reload=True,
        lifespan="on",
        forwarded_allow_ips='*',
        proxy_headers=True,
        # ssl_keyfile='/techzone/letsencrypt/live/wis-techzone.ru/privkey.pem',
        # ssl_certfile='/techzone/letsencrypt/live/wis-techzone.ru/fullchain.pem'
    )
