import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import config
from crud.UserCrud import UserCrud
from schema.UserUpdateInfoSchema import UserUpdateInfoSchema
from util.auth_token import validate_token
from util.get_db import get_db
from util.hash_string import hash_string

update_info_router = APIRouter()


@update_info_router.post("/updateInfo")
async def _(body: UserUpdateInfoSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    username = body.username
    password = body.password

    if not (config.user_name_min <= len(username) <= config.user_name_max):
        return JSONResponse(status_code=400, content={"status": 1, "message": "Username length invalid"})

    if password != "" and not (config.user_password_min <= len(password) <= config.user_password_max):
        return JSONResponse(status_code=400, content={"status": 1, "message": "Password length invalid"})

    try:
        user = UserCrud.get_by_user_id(db, user_id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if user is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "User Not Found"})

    try:
        user.username = username
        if password != "":
            user.hashed_password = hash_string(password)
        UserCrud.update(db, user)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    return {
        "status": 0,
        "message": "OK"
    }
