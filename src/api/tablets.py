from fastapi import APIRouter, Depends

from apps.commons.pagination.schemas import Pagination
from apps.commons.pagination.utils import get_pagination
from apps.tablets.schemas import TabletList, TabletOut
from apps.tablets.services import TabletService

router = APIRouter(prefix='/tablets', tags=['Tablets'])


@router.get(
    path='',
    response_model=TabletList,
    name='Get tablets list',
    description='Get tablets list',
    operation_id='get_tablets_list',
    tags=['Tablets']
)
async def get_list(
        tablets_service: TabletService = Depends(TabletService.from_request),
        pagination: Pagination = Depends(get_pagination),
) -> TabletList:
    return await tablets_service.list(
        pagination=pagination
    )


@router.get(
    path='/{id_tablet}',
    name='Get tablet',
    description='Get tablet',
    operation_id='Get tablet',
    tags=['Tablets'],
    response_model=TabletOut
)
async def get(
        id_tablet: int,
        tablet_service: TabletService = Depends(TabletService.from_request)
) -> TabletOut:
    return await tablet_service.get(id_instance=id_tablet)
