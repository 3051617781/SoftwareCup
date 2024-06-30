import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Type

from model.DocModel import Doc
from crud.DocCrud import DocCrud
from schema.DocUpdateSchema import DocUpdateSchema
from util.auth_token import validate_token
from util.get_db import get_db


update_doc_router = APIRouter()

@update_doc_router.post("/update")
async def _(body: DocUpdateSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    id = body.doc_id
    desc = body.desc
    title = body.title
    permissions = body.permissions

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
        doc.title = title
        doc.desc = desc
        doc.permissions = permissions
        DocCrud.update_doc(doc)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Database Error: {e}"})

    return {
        "status": 0, 
        "message": "OK"
    }