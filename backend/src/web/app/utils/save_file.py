import shutil
from fastapi import HTTPException

from fastapi import UploadFile
from ..conf import BASE_PATH
from uuid import uuid4


def save_file_to_static(file: UploadFile):
    url = uuid4()
    filename = BASE_PATH / 'static' / url
    try:
        with open(filename, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return f'staticfiles/{url}'

