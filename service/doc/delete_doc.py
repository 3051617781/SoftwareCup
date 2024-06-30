import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.DocCrud import DocCrud
from schema.DocDeleteSchema import DocDeleteSchema
from util.auth_token import validate_token
from util.get_db import get_db
import os
from config import config

delete_doc_router = APIRouter()

@delete_doc_router.delete("/delete")
async def _(body: DocDeleteSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    doc_id = body.doc_id

    try:
        DocCrud.delete_doc_by_id(db, doc_id)
        file_path = f"{config.doc_file_path}/{doc_id}.html" 
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})

    return {
        "status": 0, 
        "message": "OK"
    }
