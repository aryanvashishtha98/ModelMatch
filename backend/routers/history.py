"""
History Router
GET /get-history
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.history_service import HistoryService

router = APIRouter(

    prefix="/get-history",

    tags=["History"]

)


@router.get("/")

def history(

    db: Session = Depends(get_db)

):

    try:

        service = HistoryService(db)

        return {

            "success": True,

            "history": service.get_history()

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@router.get("/{dataset_id}")

def dataset_history(

    dataset_id: int,

    db: Session = Depends(get_db)

):

    try:

        service = HistoryService(db)

        return {

            "success": True,

            "history": service.get_dataset_history(dataset_id)

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )