from pydantic import BaseModel

class DocDeleteSchema(BaseModel):
    doc_id: int
