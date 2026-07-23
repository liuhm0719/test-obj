import csv
import io
import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.models.subnet import (
    create_subnet,
    delete_subnet,
    delete_subnet_tag,
    get_subnet,
    get_subnet_tags,
    get_subnets,
    merge_subnet_tags,
    replace_subnet_tags,
    update_subnet,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.subnet import (
    SubnetCreate,
    SubnetListResponse,
    SubnetResponse,
    SubnetUpdate,
    TagsPatchRequest,
    TagsPutRequest,
    TagsResponse,
)

router = APIRouter(prefix="/subnets", tags=["Subnets"])


@router.get("/export", response_class=StreamingResponse)
async def export_subnets_csv(
    tag_key: str | None = Query(None, description="按 tag key 过滤"),
    tag_value: str | None = Query(None, description="按 tag value 过滤，需与 tag_key 一起使用"),
):
    subnets = get_subnets(tag_key=tag_key, tag_value=tag_value)
    buf = io.StringIO()
    writer = csv.writer(buf)
    columns = [
        "id", "subnet_id", "name", "vpc_id", "cidr_block",
        "availability_zone", "state", "region", "map_public_ip_on_launch",
        "available_ip_count", "tags", "created_at", "updated_at",
    ]
    writer.writerow(columns)
    for subnet in subnets:
        tags_str = ";".join(
            f"{k}={v}" for k, v in sorted(subnet.tags.items())
        )
        writer.writerow([
            subnet.id,
            subnet.subnet_id,
            subnet.name,
            subnet.vpc_id,
            subnet.cidr_block,
            subnet.availability_zone,
            subnet.state,
            subnet.region,
            subnet.map_public_ip_on_launch,
            subnet.available_ip_count,
            tags_str,
            subnet.created_at,
            subnet.updated_at,
        ])
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="subnets.csv"'},
    )


@router.get("", response_model=SubnetListResponse)
async def list_subnets(
    pagination: PaginationParams = Depends(),
    tag_key: str | None = Query(None, description="按 tag key 过滤"),
    tag_value: str | None = Query(None, description="按 tag value 过滤，需与 tag_key 一起使用"),
):
    all_subnets = get_subnets(tag_key=tag_key, tag_value=tag_value)
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


@router.get(
    "/{subnet_id}/tags",
    response_model=TagsResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_tags_endpoint(subnet_id: str):
    tags = get_subnet_tags(subnet_id)
    if tags is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return TagsResponse(tags=tags)


@router.put(
    "/{subnet_id}/tags",
    response_model=TagsResponse,
    responses={404: {"model": ErrorResponse}},
)
async def replace_tags_endpoint(subnet_id: str, body: TagsPutRequest):
    subnet = replace_subnet_tags(subnet_id, body.tags)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return TagsResponse(tags=subnet.tags)


@router.patch(
    "/{subnet_id}/tags",
    response_model=TagsResponse,
    responses={404: {"model": ErrorResponse}},
)
async def merge_tags_endpoint(subnet_id: str, body: TagsPatchRequest):
    subnet = merge_subnet_tags(subnet_id, body.tags)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return TagsResponse(tags=subnet.tags)


@router.delete(
    "/{subnet_id}/tags/{tag_key}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_tag_endpoint(subnet_id: str, tag_key: str):
    subnet = delete_subnet_tag(subnet_id, tag_key)
    if subnet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Subnet not found"},
        )
    return None
