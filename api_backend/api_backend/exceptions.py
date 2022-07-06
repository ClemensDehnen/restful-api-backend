"""Project specific exceptions"""
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """Model for FastAPI ErrorMessages compatible with response_models"""

    message: str
