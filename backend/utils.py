"""
Common Utility Functions
"""

import os
import shutil

from fastapi import HTTPException
from fastapi import UploadFile

from backend.config import settings


def validate_csv(file: UploadFile):

    extension = file.filename.split(".")[-1].lower()

    if extension not in settings.ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )


def save_uploaded_file(file: UploadFile):

    os.makedirs(
        settings.UPLOAD_FOLDER,
        exist_ok=True
    )

    destination = os.path.join(
        settings.UPLOAD_FOLDER,
        file.filename
    )

    with open(destination, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return destination


def file_size_ok(path):

    size = os.path.getsize(path)

    return size <= settings.MAX_UPLOAD_SIZE