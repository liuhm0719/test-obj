from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class EC2Instance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    instance_id: str
    name: str
    instance_type: str
    state: str
    region: str
    availability_zone: str | None = None
    private_ip: str | None = None
    public_ip: str | None = None
    vpc_id: str | None = None
    key_name: str | None = None
    launch_time: str | None = None
    tags: dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


ec2_db: dict[str, EC2Instance] = {}


_UNSET = object()


def create_ec2(
    instance_id: str,
    name: str,
    instance_type: str,
    state: str,
    region: str,
    availability_zone: str | None = None,
    private_ip: str | None = None,
    public_ip: str | None = None,
    vpc_id: str | None = None,
    key_name: str | None = None,
    launch_time: str | None = None,
    tags: dict[str, str] | None = None,
) -> EC2Instance:
    instance = EC2Instance(
        instance_id=instance_id,
        name=name,
        instance_type=instance_type,
        state=state,
        region=region,
        availability_zone=availability_zone,
        private_ip=private_ip,
        public_ip=public_ip,
        vpc_id=vpc_id,
        key_name=key_name,
        launch_time=launch_time,
        tags=tags if tags is not None else {},
    )
    ec2_db[instance.id] = instance
    return instance


def get_ec2(ec2_id: str) -> EC2Instance | None:
    return ec2_db.get(ec2_id)


def get_ec2_instances() -> list[EC2Instance]:
    return list(ec2_db.values())


def update_ec2(
    ec2_id: str,
    instance_id: str | None = None,
    name: str | None = None,
    instance_type: str | None = None,
    state: str | None = None,
    region: str | None = None,
    availability_zone: object = _UNSET,
    private_ip: object = _UNSET,
    public_ip: object = _UNSET,
    vpc_id: object = _UNSET,
    key_name: object = _UNSET,
    launch_time: object = _UNSET,
    tags: dict[str, str] | None = None,
) -> EC2Instance | None:
    instance = ec2_db.get(ec2_id)
    if instance is None:
        return None
    if instance_id is not None:
        instance.instance_id = instance_id
    if name is not None:
        instance.name = name
    if instance_type is not None:
        instance.instance_type = instance_type
    if state is not None:
        instance.state = state
    if region is not None:
        instance.region = region
    if availability_zone is not _UNSET:
        instance.availability_zone = availability_zone  # type: ignore[assignment]
    if private_ip is not _UNSET:
        instance.private_ip = private_ip  # type: ignore[assignment]
    if public_ip is not _UNSET:
        instance.public_ip = public_ip  # type: ignore[assignment]
    if vpc_id is not _UNSET:
        instance.vpc_id = vpc_id  # type: ignore[assignment]
    if key_name is not _UNSET:
        instance.key_name = key_name  # type: ignore[assignment]
    if launch_time is not _UNSET:
        instance.launch_time = launch_time  # type: ignore[assignment]
    if tags is not None:
        instance.tags = tags
    instance.updated_at = datetime.now(timezone.utc).isoformat()
    return instance


def delete_ec2(ec2_id: str) -> EC2Instance | None:
    return ec2_db.pop(ec2_id, None)
