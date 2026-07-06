import math

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.rds import (
    create_rds,
    delete_rds,
    get_rds,
    get_rds_instances,
    update_rds,
)
from app.schemas.common import ErrorResponse, PaginationParams
from app.schemas.rds import RDSCreate, RDSListResponse, RDSResponse, RDSUpdate

router = APIRouter(prefix="/rds", tags=["RDS"])


@router.get("", response_model=RDSListResponse)
async def list_rds(pagination: PaginationParams = Depends()):
    all_instances = get_rds_instances()
    total = len(all_instances)
    pages = math.ceil(total / pagination.size) if total > 0 else 0
    start = pagination.offset
    end = start + pagination.size
    items = all_instances[start:end]
    return RDSListResponse(
        items=[RDSResponse.model_validate(i) for i in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=pages,
    )


@router.post("", response_model=RDSResponse, status_code=status.HTTP_201_CREATED)
async def create_rds_instance(body: RDSCreate):
    try:
        instance = create_rds(
            db_instance_identifier=body.db_instance_identifier,
            engine=body.engine.value,
            engine_version=body.engine_version,
            db_instance_class=body.db_instance_class,
            allocated_storage=body.allocated_storage,
            master_username=body.master_username,
            status=body.status.value,
            endpoint=body.endpoint,
            port=body.port,
            multi_az=body.multi_az,
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
    return RDSResponse.model_validate(instance)


@router.get(
    "/{rds_id}",
    response_model=RDSResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_rds_instance(rds_id: int):
    instance = get_rds(rds_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "RDS instance not found"},
        )
    return RDSResponse.model_validate(instance)


@router.put(
    "/{rds_id}",
    response_model=RDSResponse,
    responses={404: {"model": ErrorResponse}},
)
async def update_rds_instance(rds_id: int, body: RDSUpdate):
    update_kwargs: dict = {}
    if body.db_instance_identifier is not None:
        update_kwargs["db_instance_identifier"] = body.db_instance_identifier
    if body.engine is not None:
        update_kwargs["engine"] = body.engine.value
    if body.engine_version is not None:
        update_kwargs["engine_version"] = body.engine_version
    if body.db_instance_class is not None:
        update_kwargs["db_instance_class"] = body.db_instance_class
    if body.allocated_storage is not None:
        update_kwargs["allocated_storage"] = body.allocated_storage
    if body.status is not None:
        update_kwargs["status"] = body.status.value
    if body.endpoint is not None:
        update_kwargs["endpoint"] = body.endpoint
    if body.port is not None:
        update_kwargs["port"] = body.port
    if body.master_username is not None:
        update_kwargs["master_username"] = body.master_username
    if body.multi_az is not None:
        update_kwargs["multi_az"] = body.multi_az
    if body.region is not None:
        update_kwargs["region"] = body.region

    try:
        instance = update_rds(rds_id, **update_kwargs)
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
            detail={"code": "NOT_FOUND", "message": "RDS instance not found"},
        )
    return RDSResponse.model_validate(instance)


@router.delete(
    "/{rds_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_rds_instance(rds_id: int):
    instance = delete_rds(rds_id)
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "RDS instance not found"},
        )
    return None
