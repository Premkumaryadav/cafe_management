from cafes.endpoints import router as cafes_router
from fastapi import APIRouter


router = APIRouter()


router.include_router(cafes_router, prefix='/cafes', tags=['Cafes'])