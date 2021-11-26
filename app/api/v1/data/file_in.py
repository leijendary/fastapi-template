from app.core.models import model
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from pydantic import BaseModel


@model.as_form
class FileIn(BaseModel):
    file: UploadFile = File(...)
    bucket: str = Form(...)
    folder: str = Form(...)
