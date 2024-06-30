import time
import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud.DocCrud import DocCrud
from util.auth_token import validate_token
from util.get_db import get_db
from config import config
from schema.EditorSaveSchema import EditorSaveSchema

save_editor_router = APIRouter()

@save_editor_router.post("/save")
async def get_document(body: EditorSaveSchema, token_payload: dict = Depends(validate_token), db: Session = Depends(get_db)):
    user_id = token_payload.get("user_id")
    doc_id = body.doc_id

    try:
        doc = DocCrud.get_by_id(db, doc_id)
        if doc:
            doc_path = f"{config.doc_file_path}/{doc_id}.html" 
            with open(doc_path, 'w') as file:
                file.write(body.content)
            return {
                "status": 0,
                "message": "OK"
            }
        else:
            return JSONResponse(status_code=404, content={"status": 1, "message": "Document not found"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": 1, "message": f"Database error: {e}"})
