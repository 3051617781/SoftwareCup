import time
import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.DocCrud import DocCrud
from schema.DocCreateSchema import DocCreateSchema
from util.auth_token import validate_token
from util.get_db import get_db


create_doc_router = APIRouter()

@create_doc_router.post("/create")
async def _(body: DocCreateSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    title = body.title
    permissions = body.permissions
    desc = body.desc
    user_id = body.user_id

    if not 0 < len(title) <= 255 or not 0 < len(desc) <= 255:
        return JSONResponse(status_code=400, content={"status": 1, "message": "Title or Desc too long"})
    try:
        doc = DocCrud.create_doc(db, title, int(time.time()), int(time.time()), permissions, desc, user_id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    return {
        "status": 0, 
        "message": "OK",
        "docID": doc.doc_id 
    }
