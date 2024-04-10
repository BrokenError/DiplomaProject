from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.smartphones.schemas import SmartphoneList, SmartphoneOut
from apps.smartphones.services import SmartphoneService

router = APIRouter(prefix='/smartphones', tags=['Smartphones'])


@router.get(
    path='',
    response_model=SmartphoneList,
    name='Get smartphones list',
    description='Get smartphones list',
    tags=['Smartphones']
)
async def get_list(
        smartphone_service: SmartphoneService = Depends(SmartphoneService.from_request),
        pagination: Pagination = Depends(get_pagination),
) -> SmartphoneList:
    return await smartphone_service.list(
        pagination=pagination
    )


@router.get(
    path='/{id_smartphone}',
    name='Get smartphone',
    description='Get smartphone',
    operation_id='Get smartphone',
    tags=['Smartphones'],
    response_model=SmartphoneOut
)
async def get(
        id_smartphone: int,
        smartphone_service: SmartphoneService = Depends(SmartphoneService.from_request)
) -> SmartphoneOut:
    return await smartphone_service.get(id_instance=id_smartphone)
