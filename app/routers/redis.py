import math

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.redis import (
    create_redis,
    delete_redis,
    get_redis,
    get_redis_instances,
    update_redis,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.redis import RedisCreate, RedisListResponse, RedisResponse, RedisUpdate

router = APIRouter(prefix="/redis", tags=["redis"])


@router.get("", response_model=RedisListResponse)
async def list_redis(pagination: PaginationParams = Depends()):
    all_instances = get_redis_instances()
    total = len(all_instances)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_instances[start:end]
    return RedisListResponse(
        items=[RedisResponse.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=RedisResponse, status_code=status.HTTP_201_CREATED)
async def create_redis_instance(body: RedisCreate):
    try:
        instance = create_redis(
            cluster_id=body.cluster_id,
            node_type=body.node_type,
            engine_version=body.engine_version,
            status=body.status.value,
            endpoint=body.endpoint,
            port=body.port,
            num_shards=body.num_shards,
            replicas_per_shard=body.replicas_per_shard,
            region=body.region,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "DUPLICATE_IDENTIFIER",
                "message": str(e),
            },
        )
    return RedisResponse.model_validate(instance)


@router.get(
    "/{redis_id}",
    response_model=RedisResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_redis_instance(redis_id: int):
    instance = get_redis(redis_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Redis instance not found"},
        )
    return RedisResponse.model_validate(instance)


@router.put(
    "/{redis_id}",
    response_model=RedisResponse,
    responses={404: {"model": ErrorResponse}},
)
async def update_redis_instance(redis_id: int, body: RedisUpdate):
    update_kwargs: dict = {}
    if body.cluster_id is not None:
        update_kwargs["cluster_id"] = body.cluster_id
    if body.node_type is not None:
        update_kwargs["node_type"] = body.node_type
    if body.engine_version is not None:
        update_kwargs["engine_version"] = body.engine_version
    if body.status is not None:
        update_kwargs["status"] = body.status.value
    if body.endpoint is not None:
        update_kwargs["endpoint"] = body.endpoint
    if body.port is not None:
        update_kwargs["port"] = body.port
    if body.num_shards is not None:
        update_kwargs["num_shards"] = body.num_shards
    if body.replicas_per_shard is not None:
        update_kwargs["replicas_per_shard"] = body.replicas_per_shard
    if body.region is not None:
        update_kwargs["region"] = body.region

    try:
        instance = update_redis(redis_id, **update_kwargs)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "DUPLICATE_IDENTIFIER",
                "message": str(e),
            },
        )
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Redis instance not found"},
        )
    return RedisResponse.model_validate(instance)


@router.delete(
    "/{redis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_redis_instance(redis_id: int):
    instance = delete_redis(redis_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Redis instance not found"},
        )
    return None
