import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud
from schema.UserAuthSchema import UserAuthSchema
from util.auth_token import create_token
from util.get_db import get_db
from util.hash_string import hash_string

auth_router = APIRouter()


@auth_router.post("/auth")
async def _(body: UserAuthSchema, db: Session = Depends(get_db)):
    email = body.email
    password = body.password

    try:
        user = UserCrud.get_by_email(db, email)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"DataBase Error: {e}"})

    hashed_password = hash_string(password)

    if user is None or user.hashed_password != hashed_password:
        return JSONResponse(status_code=401, content={"status": 1, "message": f"Wrong email or password"})

    token = None

    if user.verified == 1:
        payload = {
            "user_id": user.user_id,
            "email": user.email,
            "username": user.username
        }
        token = create_token(payload)

    return {
        "status": 0,
        "message": "OK",
        "token": token,
        "userID": user.user_id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar_filename,
        "admin": user.admin,
    }
