from typing import Optional
from pydantic import BaseModel


class Text2ImgSearchRequest(BaseModel):
    """
    A class to represent the request object for the txt 2 img search
    """
    text: str
    vector_to_search: str
    k: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "text": "a cat playing alone",
                "vector_to_search": "image",
                "k": 5
            }
        }
