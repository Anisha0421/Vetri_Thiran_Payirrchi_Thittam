from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Request


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Hash a user's password.
    bcrypt supports passwords up to 72 bytes.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    # Check bcrypt's 72-byte limit
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password must be 72 bytes or fewer."
        )

    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed: str
) -> bool:
    """
    Check whether the entered password
    matches the stored password hash.
    """

    return pwd_context.verify(
        password,
        hashed
    )


def create_token(
    user_id,
    secret: str
) -> str:
    """
    Create a JWT login token.
    """

    payload = {
        "sub": str(user_id),
        "exp": (
            datetime.now(timezone.utc)
            + timedelta(hours=12)
        )
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256"
    )


def current_user_id(
    request: Request,
    secret: str
) -> int:
    """
    Get the logged-in user's ID
    from the access token cookie.
    """

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError(
                "User ID missing from token"
            )

        return int(user_id)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session"
        )