from datetime import datetime, timezone

from pydantic import BaseModel, Field


class RDSInstance(BaseModel):
    id: int = 0
    db_instance_identifier: str
    engine: str
    engine_version: str
    db_instance_class: str
    allocated_storage: int
    status: str = "creating"
    endpoint: str | None = None
    port: int = 3306
    master_username: str
    multi_az: bool = False
    region: str = "us-east-1"
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


rds_db: list[RDSInstance] = []

_next_id: int = 1


def _get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def create_rds(
    db_instance_identifier: str,
    engine: str,
    engine_version: str,
    db_instance_class: str,
    allocated_storage: int,
    master_username: str,
    status: str = "creating",
    endpoint: str | None = None,
    port: int = 3306,
    multi_az: bool = False,
    region: str = "us-east-1",
) -> RDSInstance:
    for inst in rds_db:
        if inst.db_instance_identifier == db_instance_identifier:
            raise ValueError(
                f"db_instance_identifier '{db_instance_identifier}' already exists"
            )
    instance = RDSInstance(
        id=_get_next_id(),
        db_instance_identifier=db_instance_identifier,
        engine=engine,
        engine_version=engine_version,
        db_instance_class=db_instance_class,
        allocated_storage=allocated_storage,
        master_username=master_username,
        status=status,
        endpoint=endpoint,
        port=port,
        multi_az=multi_az,
        region=region,
    )
    rds_db.append(instance)
    return instance


def get_rds(rds_id: int) -> RDSInstance | None:
    for inst in rds_db:
        if inst.id == rds_id:
            return inst
    return None


def get_rds_instances() -> list[RDSInstance]:
    return list(rds_db)


_UNSET = object()


def update_rds(
    rds_id: int,
    db_instance_identifier: str | None = None,
    engine: str | None = None,
    engine_version: str | None = None,
    db_instance_class: str | None = None,
    allocated_storage: int | None = None,
    status: str | None = None,
    endpoint: object = _UNSET,
    port: int | None = None,
    master_username: str | None = None,
    multi_az: bool | None = None,
    region: str | None = None,
) -> RDSInstance | None:
    instance = get_rds(rds_id)
    if instance is None:
        return None
    if db_instance_identifier is not None:
        for inst in rds_db:
            if (
                inst.id != rds_id
                and inst.db_instance_identifier == db_instance_identifier
            ):
                raise ValueError(
                    f"db_instance_identifier '{db_instance_identifier}' already exists"
                )
        instance.db_instance_identifier = db_instance_identifier
    if engine is not None:
        instance.engine = engine
    if engine_version is not None:
        instance.engine_version = engine_version
    if db_instance_class is not None:
        instance.db_instance_class = db_instance_class
    if allocated_storage is not None:
        instance.allocated_storage = allocated_storage
    if status is not None:
        instance.status = status
    if endpoint is not _UNSET:
        instance.endpoint = endpoint  # type: ignore[assignment]
    if port is not None:
        instance.port = port
    if master_username is not None:
        instance.master_username = master_username
    if multi_az is not None:
        instance.multi_az = multi_az
    if region is not None:
        instance.region = region
    instance.updated_at = datetime.now(timezone.utc).isoformat()
    return instance


def delete_rds(rds_id: int) -> RDSInstance | None:
    for i, inst in enumerate(rds_db):
        if inst.id == rds_id:
            return rds_db.pop(i)
    return None
