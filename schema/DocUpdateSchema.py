from pydantic import BaseModel

class DocUpdateSchema(BaseModel):
    doc_id: int
    title: str
    permissions: int
    desc: str