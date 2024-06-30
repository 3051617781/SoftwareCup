from pydantic import BaseModel

class DocCreateSchema(BaseModel):
    title: str
    permissions: int
    desc: str
    user_id: int
