from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str
