from fastapi import APIRouter

from .auth import auth_router
from .check import check_router
from .feedback import feedback_router
from .info import info_router
from .register import register_router
from .resend_email import resend_email_router
from .update_info import update_info_router
from .upload_avatar import upload_avatar_router
from .verify import verify_router

user_router = APIRouter()
user_router.include_router(auth_router)
user_router.include_router(register_router)
user_router.include_router(check_router)
user_router.include_router(info_router)
user_router.include_router(update_info_router)
user_router.include_router(upload_avatar_router)
user_router.include_router(resend_email_router)
user_router.include_router(verify_router)
user_router.include_router(feedback_router)
