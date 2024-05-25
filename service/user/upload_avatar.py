import traceback
import uuid

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud
from util.auth_token import validate_token
from util.get_db import get_db

upload_avatar_router = APIRouter()


@upload_avatar_router.post("/uploadAvatar")
async def _(file: UploadFile, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")

    file_ext = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4().hex}.{file_ext}"

    image = await file.read()
    if len(image) > 1024 * 1024:
        return JSONResponse(status_code=400, content={"status": 1, "message": "File Size Limit Exceeded"})

    try:
        with open(f"./avatar/{new_filename}", "wb") as f:
            f.write(image)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Write File Error: {e}"})

    try:
        user = UserCrud.get_by_user_id(db, user_id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    if user is None:
        return JSONResponse(status_code=404, content={"status": 1, "message": "User Not Found"})

    try:
        user.avatar_filename = new_filename
        UserCrud.update(db, user)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database Error: {e}"})

    return {
        "status": 0,
        "message": "OK",
        "avatar": new_filename
    }
