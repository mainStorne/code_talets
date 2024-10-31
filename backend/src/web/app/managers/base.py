from fastapi_sqlalchemy_toolkit import ModelManager
from ..utils.save_file import save_file_to_static
from ..db.adapters.base import BaseAdapter
from fastapi import UploadFile

class BaseManager(ModelManager):
    async def get_and_save_file(self, session, data: dict, model, file_field: str, file: UploadFile):
        file_path = save_file_to_static(file)
        data.update({file_field: file_path})
        adapter = BaseAdapter(session, model)
        return await adapter.create(data)


