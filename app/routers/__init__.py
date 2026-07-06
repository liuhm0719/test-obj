from app.routers.ec2 import router as ec2_router
from app.routers.todos import router as todos_router
from app.routers.users import router as users_router

__all__ = [
    "ec2_router",
    "todos_router",
    "users_router",
]
