import traceback

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud.UserCrud import UserCrud


def check_admin(db: Session, user_id: int) -> JSONResponse | None:
    try:
        user = UserCrud.get_by_user_id(db, user_id)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": f"Database Error {e}"})

    if not user or not user.admin:
        return JSONResponse(status_code=403, content={"message": "Forbidden"})

    return None
