import math

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.ec2 import (
    create_ec2,
    delete_ec2,
    get_ec2,
    get_ec2_instances,
    update_ec2,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.ec2 import EC2Create, EC2ListResponse, EC2Response, EC2Update

router = APIRouter(prefix="/ec2", tags=["EC2"])


@router.get("", response_model=EC2ListResponse)
async def list_ec2(pagination: PaginationParams = Depends()):
    all_instances = get_ec2_instances()
    total = len(all_instances)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_instances[start:end]
    return EC2ListResponse(
        items=[EC2Response.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=EC2Response, status_code=status.HTTP_201_CREATED)
async def create_ec2_instance(body: EC2Create):
    instance = create_ec2(
        instance_id=body.instance_id,
        name=body.name,
        instance_type=body.instance_type,
        state=body.state.value,
        region=body.region,
        availability_zone=body.availability_zone,
        private_ip=body.private_ip,
        public_ip=body.public_ip,
        vpc_id=body.vpc_id,
        key_name=body.key_name,
        launch_time=body.launch_time,
        tags=body.tags,
    )
    return EC2Response.model_validate(instance)


@router.get(
    "/{ec2_id}",
    response_model=EC2Response,
    responses={404: {"model": ErrorResponse}},
)
async def get_ec2_instance(ec2_id: str):
    instance = get_ec2(ec2_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "EC2 instance not found"},
        )
    return EC2Response.model_validate(instance)


@router.put(
    "/{ec2_id}",
    response_model=EC2Response,
    responses={404: {"model": ErrorResponse}},
)
async def update_ec2_instance(ec2_id: str, body: EC2Update):
    update_kwargs: dict = {}
    if body.instance_id is not None:
        update_kwargs["instance_id"] = body.instance_id
    if body.name is not None:
        update_kwargs["name"] = body.name
    if body.instance_type is not None:
        update_kwargs["instance_type"] = body.instance_type
    if body.state is not None:
        update_kwargs["state"] = body.state.value
    if body.region is not None:
        update_kwargs["region"] = body.region
    if body.availability_zone is not None:
        update_kwargs["availability_zone"] = body.availability_zone
    if body.private_ip is not None:
        update_kwargs["private_ip"] = body.private_ip
    if body.public_ip is not None:
        update_kwargs["public_ip"] = body.public_ip
    if body.vpc_id is not None:
        update_kwargs["vpc_id"] = body.vpc_id
    if body.key_name is not None:
        update_kwargs["key_name"] = body.key_name
    if body.launch_time is not None:
        update_kwargs["launch_time"] = body.launch_time
    if body.tags is not None:
        update_kwargs["tags"] = body.tags

    instance = update_ec2(ec2_id, **update_kwargs)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "EC2 instance not found"},
        )
    return EC2Response.model_validate(instance)


@router.delete(
    "/{ec2_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_ec2_instance(ec2_id: str):
    instance = delete_ec2(ec2_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "EC2 instance not found"},
        )
    return None
