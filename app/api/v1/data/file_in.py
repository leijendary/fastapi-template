from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from pydantic import BaseModel

from app.core.models import model


@model.as_form
class FileIn(BaseModel):
    file: UploadFile = File(...)
    bucket: str = Form(...)
    folder: str = Form(...)
