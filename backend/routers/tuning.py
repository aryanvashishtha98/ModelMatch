"""
Tuning Router
POST /run-tuning/{dataset_id}
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.tuning_service import TuningService

router = APIRouter(

    prefix="/run-tuning",

    tags=["Model Tuning"]

)


@router.post("/{dataset_id}")

def tune(

    dataset_id: int,

    db: Session = Depends(get_db)

):

    try:

        service = TuningService(db)

        results = service.run(dataset_id)

        return {

            "success": True,

            "verified_results": results

        }

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )