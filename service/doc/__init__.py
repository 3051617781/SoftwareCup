from fastapi import APIRouter
from .create_doc import create_doc_router
from .delete_doc import delete_doc_router
from .list_doc import list_doc_router
from .update_doc import update_doc_router
from .update_time import update_time_router
from .get_doc import get_doc_router

doc_router = APIRouter()
doc_router.include_router(create_doc_router)
doc_router.include_router(delete_doc_router)
doc_router.include_router(list_doc_router)
doc_router.include_router(update_doc_router)
doc_router.include_router(update_time_router)
doc_router.include_router(get_doc_router)