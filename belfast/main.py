from typing import Optional

from pydantic import BaseModel

from .router import app


class RequestBody(BaseModel):
    image: Optional[str] = None


@app.post("/upload")
def upload(body: RequestBody):
    image = body.image

    if image is None:
        return {
            "status": "error",
            "message": "No image provided",
        }

    # Do something with the image

    return {
        "status": "success",
    }
