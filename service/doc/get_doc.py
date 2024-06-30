import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.DocCrud import DocCrud
from crud.UserCrud import UserCrud
from schema.DocGetSchema import DocGetSchema
from util.auth_token import validate_token
from util.get_db import get_db
import datetime

get_doc_router = APIRouter()

@get_doc_router.post("/get")
async def _(body: DocGetSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    doc_id = body.doc_id

    try:
        doc = DocCrud.get_by_id(db, doc_id)
        user = UserCrud.get_by_user_id(db, doc.user_id)
        datetime_obj = datetime.datetime.fromtimestamp(doc.updated)
        time_str = datetime_obj.strftime('%Y-%m-%d')

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    return {
        "status": 0, 
        "message": "OK",
        "username": user.username,
        "title": doc.title,
        "updated": time_str,
        "desc": doc.desc,
        "permissions": doc.permissions,
        "id": doc.doc_id
    }
