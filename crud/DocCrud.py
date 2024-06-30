from typing import Type

from sqlalchemy.orm import Session

from model.DocModel import Doc


class DocCrud:
    @staticmethod
    def create_doc(db: Session, title: str, created: int, updated: int, permissions: int, desc: str, user_id: int) -> Doc:
        doc = Doc(title, created, updated, permissions, desc, user_id)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    
    @staticmethod
    def get_docs_from_permissions(db: Session, user_id: int, permissions: int) -> list[Type[Doc]]:
        return db.query(Doc).filter(Doc.user_id == user_id, Doc.permissions == permissions).all()
    
    @staticmethod
    def get_all_docs(db: Session, user_id: int) -> list[Type[Doc]]:
        return db.query(Doc).filter(Doc.user_id == user_id).all()
    
    @staticmethod
    def update_doc(db: Session, doc: Doc):
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def delete_doc_by_id(db: Session, doc_id:int) -> None:
        doc = db.query(Doc).filter(Doc.doc_id == doc_id).first()
        db.delete(doc)
        db.commit()

    @staticmethod
    def get_by_id(db: Session, id: int) -> Doc:
        return db.query(Doc).filter(Doc.doc_id == id).first()

