from pydantic import BaseModel


class UserUpdateInfoSchema(BaseModel):
    username: str
    password: str
