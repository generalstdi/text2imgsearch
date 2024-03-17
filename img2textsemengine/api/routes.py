import asyncio
from functools import partial
import requests
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, FileResponse
from PIL import Image
from img2textsemengine.api import searchers
from img2textsemengine.api.response import Text2ImgSearchInstanceReply
from img2textsemengine.api.request import Text2ImgSearchRequest

router = APIRouter()


@router.get(
    "/health",
    response_class=PlainTextResponse,
    response_description="Returns 'OK' if service is up"
)
def get_health():
    return "OK"


@router.post(
    "/query",
    response_model=list[Text2ImgSearchInstanceReply],
    response_description="Return the metadata of the top-k most similar images against the user query"
)
async def query(request_body: Text2ImgSearchRequest) -> list[Text2ImgSearchInstanceReply]:
    """
    Implement the query POST request which retrieve the top-k most similar image against the user's text query
    :param request_body: the request body
    :return: The img url and the captions/answers of the most relevant image
    """
    text = request_body.text
    vector_to_search = request_body.vector_to_search
    k = request_body.k
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(executor=None, func=partial(searchers["base_searcher"].query,
                                                                      text=text,
                                                                      vector_to_search=vector_to_search,
                                                                      top_k=k))
    search_results = []
    for retrieved_img in response:
        search_results.append(Text2ImgSearchInstanceReply(captions=retrieved_img[1],
                                                          img_url=retrieved_img[0]))
    return search_results


@router.get(
    "/get_image",
    response_class=FileResponse,
    response_description="Returns an image based on its url"
)
def get_image(img_url: str) -> FileResponse:
    """
    Given an img url, save it locally and then display it
    :param img_url: the img url
    :return: the image itself
    """
    image = Image.open(requests.get(img_url, stream=True).raw)
    image.save("tmp.jpeg")
    return FileResponse(path="tmp.jpeg")
