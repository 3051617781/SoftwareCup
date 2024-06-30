from fastapi import APIRouter
from .get_editor import get_editor_router
from .save_editor import save_editor_router
editor_router = APIRouter()
editor_router.include_router(get_editor_router)
editor_router.include_router(save_editor_router)