from pydantic import BaseModel, AnyUrl
from typing import Optional


class LivePredictEventData(BaseModel):
    request_id: str
    endpoint_id: str
    model_type: str
    location: str
    image_url: AnyUrl
    image_id: str
    webhooks: str
