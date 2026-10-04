from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10000000
    )

    room_type: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="modern",
        max_length=80
    )

    items: dict[str, int] = Field(
        default_factory=dict
    )

    city: str = Field(
        default="Chennai",
        max_length=100
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10000000
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="Home",
        max_length=120
    )

    city: str = Field(
        default="Chennai",
        max_length=100
    )