from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), index=True)
    hashed_password = Column(String(255))
    avatar_filename = Column(String(255))
    verified = Column(Integer)
    admin = Column(Integer)

    def __init__(self, email: str, username: str, hashed_password: str, avatar_filename: str, verified: int,
                 admin: int):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.avatar_filename = avatar_filename
        self.verified = verified
        self.admin = admin
