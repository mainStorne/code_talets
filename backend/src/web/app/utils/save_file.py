import shutil
from fastapi import HTTPException

from fastapi import UploadFile
from ..conf import BASE_PATH
from uuid import uuid4


def save_file_to_static(file: UploadFile):
    url = f'{uuid4()}{file.filename}'
    filename = BASE_PATH / 'static' / url
    try:
        with open(f'{filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return f'/staticfiles/{url}'

