from fastapi import Depends, Request, HTTPException

from sqlalchemy.orm import Session

from .database import get_db
from .config import get_settings
from .models import User
from .security import current_user_id


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    user_id = current_user_id(
        request,
        get_settings().secret_key
    )

    user = db.get(
        User,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user