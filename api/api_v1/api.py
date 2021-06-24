from fastapi import APIRouter

from api.api_v1.endpoints import user,rbac

api_router = APIRouter()
# user
api_router.include_router(user.router, prefix='/user', tags=['user'])
# rbac
api_router.include_router(rbac.router, prefix='/rbac', tags=['rbac'])

