import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recommendation
from ..schemas import (
    HomeRequest,
    PartyRequest
)

from ..dependencies import get_current_user

from ..services.gemini import GeminiService

from ..config import get_settings


router = APIRouter(
    prefix="/api",
    tags=["planners"]
)


def get_service():

    settings = get_settings()

    return GeminiService(
        settings.gemini_api_key,
        settings.gemini_model
    )


def save_recommendation(
    db,
    user,
    planner,
    budget,
    payload,
    result
):

    row = Recommendation(

        user_id=user.id,

        planner=planner,

        budget=budget,

        input_json=json.dumps(
            payload
        ),

        result_json=json.dumps(
            result
        )
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    return row


@router.post("/generate-home")
def generate_home(
    data: HomeRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    payload = data.model_dump()

    result = get_service().generate(
        "home",
        payload
    )

    row = save_recommendation(
        db,
        user,
        "home",
        data.budget,
        payload,
        result
    )

    return {
        "id": row.id,
        **result
    }


@router.post("/generate-party")
def generate_party(
    data: PartyRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    payload = data.model_dump()

    result = get_service().generate(
        "party",
        payload
    )

    row = save_recommendation(
        db,
        user,
        "party",
        data.budget,
        payload,
        result
    )

    return {
        "id": row.id,
        **result
    }


@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form("elegant"),

    outfit_color: str = Form(""),

    notes: str = Form(""),

    outfit_image: UploadFile | None = File(None),

    user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be positive"
        )

    image = None

    mime = None

    if outfit_image:

        allowed = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if outfit_image.content_type not in allowed:

            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG and WebP images are allowed"
            )

        image = await outfit_image.read()

        if len(image) > 5 * 1024 * 1024:

            raise HTTPException(
                status_code=413,
                detail="Image must be 5 MB or smaller"
            )

        mime = outfit_image.content_type

    payload = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "outfit_color": outfit_color,

        "notes": notes
    }

    result = get_service().generate(

        "jewelry",

        payload,

        image,

        mime
    )

    row = save_recommendation(

        db,

        user,

        "jewelry",

        budget,

        payload,

        result
    )

    return {
        "id": row.id,
        **result
    }