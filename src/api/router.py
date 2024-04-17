from fastapi import APIRouter

from api.accessories import router as accessory_router
from api.favourites import router as favourite_router
from api.laptops import router as laptop_router
from api.order import router as order_router
from api.products import router as product_router
from api.smartphones import router as smartphone_router
from api.smartwatches import router as smartwatch_router
from api.tablets import router as tablet_router
from api.televisions import router as television_router
from api.users import router as user_router

router = APIRouter(prefix='')

router.include_router(product_router)
router.include_router(tablet_router)
router.include_router(accessory_router)
router.include_router(laptop_router)
router.include_router(smartphone_router)
router.include_router(smartwatch_router)
router.include_router(television_router)
router.include_router(user_router)
router.include_router(favourite_router)
router.include_router(order_router)
