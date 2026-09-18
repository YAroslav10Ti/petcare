from fastapi import APIRouter

from app.api.v1.auth.router import auth_router
from app.api.v1.pets.router import pets_router
from app.api.v1.medical_record.router import medical_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(pets_router)
api_router.include_router(medical_router)