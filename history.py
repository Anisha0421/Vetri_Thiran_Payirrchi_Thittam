import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recommendation
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/api",
    tags=["history"]
)


@router.get("/history")
def history(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(Recommendation)
        .filter_by(user_id=user.id)
        .order_by(
            Recommendation.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [

        {

            "id": row.id,

            "planner": row.planner,

            "budget": row.budget,

            "created_at":
                row.created_at.isoformat(),

            "result":
                json.loads(
                    row.result_json
                )
        }

        for row in rows
    ]


@router.get(
    "/recommendations/{rid}"
)
def recommendation_detail(
    rid: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    row = db.get(
        Recommendation,
        rid
    )

    if (
        not row
        or row.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return {

        "id": row.id,

        "planner":
            row.planner,

        "budget":
            row.budget,

        "input":
            json.loads(
                row.input_json
            ),

        "result":
            json.loads(
                row.result_json
            )
    }