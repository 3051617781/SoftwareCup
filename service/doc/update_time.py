import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from model.DocModel import Doc
from crud.DocCrud import DocCrud
from schema.DocGetSchema import DocGetSchema
from util.auth_token import validate_token
from util.get_db import get_db
import time

update_time_router = APIRouter()

@update_time_router.post("/update_time")
async def _(body: DocGetSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    id = body.doc_id

    try:
        doc = DocCrud.get_by_id(db, id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Database Error: {e}"})

    if doc is None:
        return JSONResponse(status_code=404, content={"message": "Doc Not Found"})

    if doc.user_id != user_id:
        return JSONResponse(status_code=403, content={"message": "Permission Denied"})

    try:
        doc.updated = int(time.time())
        DocCrud.update_doc(doc)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Database Error: {e}"})

    return {
        "status": 0, 
        "message": "OK"
    }