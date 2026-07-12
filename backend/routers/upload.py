"""
Upload Router
POST /upload-dataset
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.upload_service import UploadService

router = APIRouter(
    prefix="/upload-dataset",
    tags=["Upload Dataset"]
)


@router.post("/")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        service = UploadService(db)

        result = service.upload_dataset(file)

        return {

            "success": True,

            "message": "Dataset uploaded successfully.",

            "data": result

        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )