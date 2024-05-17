from fastapi import APIRouter, Depends

from apps.products.services import ProductService
from apps.reviews.schemas import ReviewOut, ReviewIn, ReviewUpdate
from apps.reviews.services import ReviewService

router = APIRouter(prefix='/reviews', tags=['Reviews'])


@router.get(
    path='/{id_review}',
    name='Get review product',
    description='Get review product',
    response_model=ReviewOut,
    tags=['Reviews'],
)
async def get_review(
        id_review: int,
        review_service: ReviewService = Depends(ReviewService.from_request_private),
) -> ReviewOut:
    return await review_service.get(id_instance=id_review)


@router.post(
    path='/{id_product}',
    name='Create review product',
    description='Create review product',
    response_model=ReviewOut,
    tags=['Reviews'],
)
async def create_review(
        id_product: int,
        data: ReviewIn,
        review_service: ReviewService = Depends(ReviewService.from_request_private),
        product_service: ProductService = Depends(ProductService.from_request_protected)
) -> ReviewOut:
    return await review_service.create(data=data, product_service=product_service, data_extra={"id_product": id_product})


@router.patch(
    path='/{id_review}',
    name='Update review product',
    description='Update review product',
    response_model=ReviewOut,
    tags=['Reviews'],
)
async def create_review(
        id_review: int,
        data: ReviewUpdate,
        review_service: ReviewService = Depends(ReviewService.from_request_private),
) -> ReviewOut:
    return await review_service.update(id_instance=id_review, data=data)
