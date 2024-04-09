from fastapi import APIRouter, Depends

from apps.accessories.schemas import AccessoryList, AccessoryOut
from apps.accessories.services import AccessoryService
from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination

router = APIRouter(prefix='/accessories', tags=['Accessories'])


@router.get(
    path='',
    response_model=AccessoryList,
    name='Get accessories list',
    description='Get accessories list',
    tags=['Accessories']
)
async def get_list(
        accessory_service: AccessoryService = Depends(AccessoryService.from_request),
        pagination: Pagination = Depends(get_pagination),
) -> AccessoryList:
    return await accessory_service.list(
        pagination=pagination
    )


@router.get(
    path='/{id_accessory}',
    name='Get accessory',
    description='Get accessory',
    operation_id='Get accessory',
    tags=['Accessories'],
    response_model=AccessoryOut
)
async def get(
        id_accessory: int,
        accessory_service: AccessoryService = Depends(AccessoryService.from_request)
) -> AccessoryOut:
    return await accessory_service.get(id_instance=id_accessory)
