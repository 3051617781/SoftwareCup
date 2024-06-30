from pydantic import BaseModel

class EditorSaveSchema(BaseModel):
    doc_id: int
    content: str
    