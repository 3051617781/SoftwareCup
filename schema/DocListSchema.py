from pydantic import BaseModel


class DocListSchema(BaseModel):
    user_id: int
    permissions: int
