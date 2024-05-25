import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.UserCrud import UserCrud
from schema.UserRegisterSchema import UserRegisterSchema
from util.get_db import get_db
from util.hash_string import hash_string

register_router = APIRouter()


@register_router.post("/register")
async def _(body: UserRegisterSchema, db: Session = Depends(get_db)):
    email = body.email
    username = body.username
    password = body.password

    if len(email) > config.user_email_max:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Email too long"})

    if not (config.user_name_min <= len(username) <= config.user_name_max):
        return JSONResponse(status_code=400, content={"status": 1, "message": "Username length invalid"})

    if not (config.user_password_min <= len(password) <= config.user_password_max):
        return JSONResponse(status_code=400, content={"status": 1, "message": "Password length invalid"})

    try:
        user = UserCrud.get_by_email(db, email)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    if user:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Email already exists"})

    try:
        user = UserCrud.create(db, email, username, hash_string(password))
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    return {
        "status": 0,
        "message": "OK",
        "email": user.email,
        "userID": user.user_id,
        "username": user.username,
        "avatar": user.avatar_filename
    }
