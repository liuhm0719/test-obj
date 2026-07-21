import math

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.subnet import (
    create_subnet,
    delete_subnet,
    get_subnet,
    get_subnets,
    update_subnet,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.subnet import (
    SubnetCreate,
    SubnetListResponse,
    SubnetResponse,
    SubnetUpdate,
)

router = APIRouter(prefix="/subnets", tags=["Subnets"])


@router.get("", response_model=SubnetListResponse)
async def list_subnets(pagination: PaginationParams = Depends()):
    all_subnets = get_subnets()
    total = len(all_subnets)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_subnets[start:end]
    return SubnetListResponse(
        items=[SubnetResponse.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=SubnetResponse, status_code=status.HTTP_201_CREATED)
async def create_subnet_endpoint(body: SubnetCreate):
    subnet = create_subnet(
        subnet_id=body.subnet_id,
        name=body.name,
        vpc_id=body.vpc_id,
        cidr_block=body.cidr_block,
        availability_zone=body.availability_zone,
        state=body.state.value,
        region=body.region,
        map_public_ip_on_launch=body.map_public_ip_on_launch,
        available_ip_count=body.available_ip_count,
        tags=body.tags,
    )
    return SubnetResponse.model_validate(subnet)


@router.get(
    "/{subnet_id}",
    response_model=SubnetResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_subnet_endpoint(subnet_id: str):
    subnet = get_subnet(subnet_id)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return SubnetResponse.model_validate(subnet)


@router.put(
    "/{subnet_id}",
    response_model=SubnetResponse,
    responses={404: {"model": ErrorResponse}},
)
async def update_subnet_endpoint(subnet_id: str, body: SubnetUpdate):
    update_kwargs: dict = {}
    if body.subnet_id is not None:
        update_kwargs["subnet_id"] = body.subnet_id
    if body.name is not None:
        update_kwargs["name"] = body.name
    if body.vpc_id is not None:
        update_kwargs["vpc_id"] = body.vpc_id
    if body.cidr_block is not None:
        update_kwargs["cidr_block"] = body.cidr_block
    if body.availability_zone is not None:
        update_kwargs["availability_zone"] = body.availability_zone
    if body.state is not None:
        update_kwargs["state"] = body.state.value
    if body.region is not None:
        update_kwargs["region"] = body.region
    if body.map_public_ip_on_launch is not None:
        update_kwargs["map_public_ip_on_launch"] = body.map_public_ip_on_launch
    if body.available_ip_count is not None:
        update_kwargs["available_ip_count"] = body.available_ip_count
    if body.tags is not None:
        update_kwargs["tags"] = body.tags

    subnet = update_subnet(subnet_id, **update_kwargs)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return SubnetResponse.model_validate(subnet)


@router.delete(
    "/{subnet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_subnet_endpoint(subnet_id: str):
    subnet = delete_subnet(subnet_id)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return None
