import traceback

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud
from schema.UserResendEmailSchema import UserResendEmailSchema
from util.get_db import get_db
from util.hash_string import hash_string
from util.send_verify_email import send_verify_email

resend_email_router = APIRouter()


@resend_email_router.post("/resendEmail")
async def _(body: UserResendEmailSchema, db: Session = Depends(get_db)):
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

    if user.verified == 1:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Email already verified"})

    await send_verify_email(email)

    return {
        "status": 0,
        "message": "OK",
    }
