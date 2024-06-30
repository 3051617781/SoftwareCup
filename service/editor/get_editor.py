import time
import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud.DocCrud import DocCrud
from util.auth_token import validate_token
from util.get_db import get_db
from config import config
from schema.EditorGetSchema import EditorGetSchema
import os

get_editor_router = APIRouter()

@get_editor_router.post("/get")
async def get_document(body: EditorGetSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    doc_id = body.doc_id

    try:
        doc = DocCrud.get_by_id(db, doc_id)
        if doc:
            doc_path = f"{config.doc_file_path}/{doc_id}.html" 
            if os.path.exists(doc_path):
                with open(doc_path, 'r') as file:
                    content = file.read()
            else:
                with open(doc_path, 'w') as file:
                    file.write("")
                content = ""
            return {
                "status": 0,
                "message": "OK",
                "content": content
            }
        else:
            return JSONResponse(status_code=404, content={"status": 1, "message": "Document not found"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})
