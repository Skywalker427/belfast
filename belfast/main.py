from typing import Optional

from fastapi import Response, status
from pydantic import BaseModel

from .router import app
from .utils.utils import filter_none


class RequestBody(BaseModel):
    image: Optional[str] = None

class SuccessResponse(BaseModel):
    status: str = "success"
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str = "An error occurred"


@app.post("/upload")
def upload(body: RequestBody, response: Response):
    image = body.image

    if image is None:
        error_response = ErrorResponse(
            status="error",
            message="Image is required. Please provide an image in the request body.",
        )
        response.status_code = status.HTTP_400_BAD_REQUEST
        return filter_none(error_response.dict())

    # Do something with the image

    res = SuccessResponse(status="success")
    response.status_code = status.HTTP_201_CREATED
    return filter_none(res.dict())