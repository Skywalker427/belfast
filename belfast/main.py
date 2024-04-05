import json
from enum import Enum
from typing import Optional

from fastapi import Response, status
from pydantic import BaseModel

from .router import app
from .utils.utils import filter_none
from .prompts.v5c_extract import prompt as v5c_extract_prompt
from .prompts.dl_extract import prompt as dl_extract_prompt
from .prompts.matches import prompt as matches_prompt


class ImageType(str, Enum):
    v5c = "v5c"
    id = "id"


class RequestBody(BaseModel):
    image: Optional[str] = None
    image_type: Optional[ImageType] = None


class ComparisonBody(BaseModel):
    v5c: dict
    id: dict


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str = "An error occurred"


class Enquiry(BaseModel):
    enquiry_id: str
    v5c_ocr: Optional[dict] = None
    id_ocr: Optional[dict] = None


@app.post("/upload")
def upload(body: RequestBody, response: Response):
    image = body.image
    image_type = body.image_type

    if image is None:
        error_response = ErrorResponse(
            status="error",
            message="Image is required. Please provide an image in the request body.",
        )
        response.status_code = status.HTTP_400_BAD_REQUEST
        return filter_none(error_response.dict())

    if image_type == 'v5c':
        llm_response = v5c_extract_prompt.call(image)
    elif image_type == 'id':
        llm_response = dl_extract_prompt.call(image)
    else:
        error_response = ErrorResponse(
            status="error",
            message="Invalid image type. Please provide a valid image type in the request body.",
        )
        response.status_code = status.HTTP_400_BAD_REQUEST
        return filter_none(error_response.dict())

    res = SuccessResponse(status="success", data=llm_response)
    response.status_code = status.HTTP_200_OK
    return filter_none(res.dict())


@app.post("/compare")
def compare(body: ComparisonBody):
    matches_prompt.set_variables(
        context=json.dumps({
            "set1": {
                "name": body.v5c.get("name"),
                "address": body.v5c.get("address"),
            },
            "set2": {
                "name": f"{body.id.get('2.')} {body.id.get('1.')}",
                "address": body.id.get("8."),
            },
        }, indent=4),
    )

    response = matches_prompt.call()

    res = SuccessResponse(status="success", data=response)
    return filter_none(res.dict())
