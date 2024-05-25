import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud
from util.auth_token import validate_token
from util.get_db import get_db

verify_router = APIRouter()


@verify_router.get("/verify")
async def _(token: str, db: Session = Depends(get_db)):
    payload = validate_token(token)

    email = payload.get("email")

    try:
        user = UserCrud.get_by_email(db, email)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"DataBase Error: {e}"})

    if user is None:
        return JSONResponse(status_code=400, content={"status": 1, "message": "No such user"})

    if user.verified == 1:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Email already verified"})

    try:
        user.verified = 1
        UserCrud.update(db, user)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"DataBase Error: {e}"})

    return "账号已激活"