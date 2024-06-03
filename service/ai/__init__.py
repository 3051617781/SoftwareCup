from fastapi import APIRouter

from .continuation import continuation_router
from .styling import styling_router
from .translate import trans_router
ai_router = APIRouter()
ai_router.include_router(continuation_router)
ai_router.include_router(styling_router)
ai_router.include_router(trans_router)