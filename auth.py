from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Recommendation
from ..schemas import (
    RegisterRequest,
    LoginRequest
)

from ..security import (
    hash_password,
    verify_password,
    create_token
)

from ..config import get_settings
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    email = data.email.lower()

    existing_user = (
        db.query(User)
        .filter_by(email=email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(
            data.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(
        user.id,
        get_settings().secret_key
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        max_age=43200
    )

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter_by(
            email=data.email.lower()
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(
        user.id,
        get_settings().secret_key
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        max_age=43200
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out"
    }


@router.get("/session-info")
def session_info(
    user=Depends(get_current_user)
):

    return {
        "logged_in": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


@router.get("/session-data")
def session_data(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    count = (
        db.query(Recommendation)
        .filter_by(user_id=user.id)
        .count()
    )

    return {
        "user_id": user.id,
        "recommendation_count": count
    }