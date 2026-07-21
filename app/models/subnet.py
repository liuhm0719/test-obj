from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Subnet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    subnet_id: str
    name: str
    vpc_id: str
    cidr_block: str
    availability_zone: str
    state: str
    region: str
    map_public_ip_on_launch: bool | None = None
    available_ip_count: int | None = None
    tags: dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


subnet_db: dict[str, Subnet] = {}


_UNSET = object()


def create_subnet(
    subnet_id: str,
    name: str,
    vpc_id: str,
    cidr_block: str,
    availability_zone: str,
    state: str,
    region: str,
    map_public_ip_on_launch: bool | None = None,
    available_ip_count: int | None = None,
    tags: dict[str, str] | None = None,
) -> Subnet:
    subnet = Subnet(
        subnet_id=subnet_id,
        name=name,
        vpc_id=vpc_id,
        cidr_block=cidr_block,
        availability_zone=availability_zone,
        state=state,
        region=region,
        map_public_ip_on_launch=map_public_ip_on_launch,
        available_ip_count=available_ip_count,
        tags=tags if tags is not None else {},
    )
    subnet_db[subnet.id] = subnet
    return subnet


def get_subnet(subnet_id: str) -> Subnet | None:
    return subnet_db.get(subnet_id)


def get_subnets() -> list[Subnet]:
    return list(subnet_db.values())


def update_subnet(
    subnet_id: str,
    name: str | None = None,
    vpc_id: str | None = None,
    cidr_block: str | None = None,
    availability_zone: str | None = None,
    state: str | None = None,
    region: str | None = None,
    map_public_ip_on_launch: object = _UNSET,
    available_ip_count: object = _UNSET,
    tags: dict[str, str] | None = None,
) -> Subnet | None:
    subnet = subnet_db.get(subnet_id)
    if subnet is None:
        return None
    if name is not None:
        subnet.name = name
    if vpc_id is not None:
        subnet.vpc_id = vpc_id
    if cidr_block is not None:
        subnet.cidr_block = cidr_block
    if availability_zone is not None:
        subnet.availability_zone = availability_zone
    if state is not None:
        subnet.state = state
    if region is not None:
        subnet.region = region
    if map_public_ip_on_launch is not _UNSET:
        subnet.map_public_ip_on_launch = map_public_ip_on_launch  # type: ignore[assignment]
    if available_ip_count is not _UNSET:
        subnet.available_ip_count = available_ip_count  # type: ignore[assignment]
    if tags is not None:
        subnet.tags = tags
    subnet.updated_at = datetime.now(timezone.utc).isoformat()
    return subnet


def delete_subnet(subnet_id: str) -> Subnet | None:
    return subnet_db.pop(subnet_id, None)
