from typing import Type

from sqlalchemy.orm import Session

from model.UserModel import User


class UserCrud:
    @staticmethod
    def create(db: Session, email: str, username: str, password: str, avatar_filename: str = "",
               verified: int = 0, admin: bool = False) -> User:
        new_user = User(email, username, password, avatar_filename, verified, admin)
        db.add(new_user)
        db.commit()
        return new_user

    @staticmethod
    def get_by_user_id(db: Session, user_id) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_one_by_username(db: Session, username) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_all(db: Session) -> list[Type[User]]:
        return db.query(User).all()

    @staticmethod
    def update(db: Session, user) -> User:
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user) -> User:
        db.delete(user)
        db.commit()
        return user

    @staticmethod
    def delete_by_user_id(db: Session, user_id) -> User:
        user = UserCrud.get_by_user_id(db, user_id)
        db.delete(user)
        db.commit()
        return user
