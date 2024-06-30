from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base

class Doc(Base):
    __tablename__ = "doc"

    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    created = Column(Integer)
    updated = Column(Integer)
    permissions = Column(Integer)
    desc = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    
    def __init__(self, title, created, updated, permissions, desc, user_id):
        self.title = title
        self.created = created
        self.updated = updated
        self.user_id = user_id
        self.desc = desc
        self.permissions = permissions
