from pydantic import BaseModel


class Text2ImgSearchInstanceReply(BaseModel):
    """
    A class to define the reply object of the API
    """
    captions: list[str]  # the captions of the image
    img_url: str  # the url of the image

    class Config:
        json_schema_extra = {
            "example": [{
                "captions": ["caption 1", "caption 2"],
                "img_url": "http://images.cocodataset.org/val2014/COCO_val2014_000000203564.jpg"
            }]
        }
