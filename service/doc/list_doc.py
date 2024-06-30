import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Type

from model.DocModel import Doc
from crud.DocCrud import DocCrud
from schema.DocListSchema import DocListSchema
from util.auth_token import validate_token
from util.get_db import get_db


list_doc_router = APIRouter()

@list_doc_router.post("/list")
async def _(body: DocListSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    user_id = body.user_id
    permissions = body.permissions

    try:
        if permissions == -1:
            doc_list:list[Type[Doc]] = DocCrud.get_all_docs(db, user_id)
        else:
            doc_list:list[Type[Doc]] = DocCrud.get_docs_from_permissions(db, user_id, permissions)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    return {
        "status": 0, 
        "message": "OK",
        "docID": [_.doc_id for _ in doc_list]
    }
