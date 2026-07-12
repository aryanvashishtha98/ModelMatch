"""
Recommendation Router
GET /get-recommendation/{dataset_id}
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/get-recommendation",
    tags=["Recommendation"]
)


@router.get("/{dataset_id}")

def recommend(

    dataset_id: int,

    db: Session = Depends(get_db)

):

    try:

        service = RecommendationService(db)

        result = service.recommend(dataset_id)

        return {

            "success": True,

            "data": result

        }

    except Exception as e:
    import traceback
    traceback.print_exc()
    raise HTTPException(
        status_code=500,
        detail=str(e)
    )