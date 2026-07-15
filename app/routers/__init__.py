from app.routers.ec2 import router as ec2_router
from app.routers.projects import router as projects_router
from app.routers.rds import router as rds_router
from app.routers.redis import router as redis_router
from app.routers.todos import router as todos_router
from app.routers.users import router as users_router

__all__ = [
    "ec2_router",
    "projects_router",
    "rds_router",
    "redis_router",
    "todos_router",
    "users_router",
]
