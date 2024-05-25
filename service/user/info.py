import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud
from util.auth_token import validate_token
from util.get_db import get_db

info_router = APIRouter()


@info_router.get("/info")
async def _(token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")

    try:
        user = UserCrud.get_by_user_id(db, user_id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if user is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "User Not Found"})

    return {
        "status": 0,
        "message": "OK",
        "data": {
            "userID": user.user_id,
            "email": user.email,
            "username": user.username,
            "avatar": user.avatar_filename,
            "admin": user.admin,
        }
    }
