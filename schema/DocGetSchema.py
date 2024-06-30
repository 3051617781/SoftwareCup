from pydantic import BaseModel

class DocGetSchema(BaseModel):
    doc_id: int
