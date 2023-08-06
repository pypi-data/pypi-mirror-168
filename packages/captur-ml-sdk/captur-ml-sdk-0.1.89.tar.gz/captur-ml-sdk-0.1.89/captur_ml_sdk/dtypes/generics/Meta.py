from pydantic import (
    BaseModel, HttpUrl
)
from typing import Optional, List


class Meta(BaseModel):
    webhooks: Optional[HttpUrl]


class PredictMeta(BaseModel):
    webhooks: Optional[HttpUrl]
    transfer_bucket: Optional[str] = "captur-ml-test"
    pipeline_location: Optional[str] = "us-central1"


class TrainingMeta(BaseModel):
    location: Optional[str] = "europe-west4"
    webhooks: Optional[HttpUrl]
    budget_milli_node_hours: Optional[int] = 8000


class EvaluationMeta(BaseModel):
    webhooks: Optional[HttpUrl]
    write_to_file: Optional[bool]
    last_file: Optional[bool]
    request_id: Optional[str]
    prediction_model_name: Optional[str]
    label_model_name: Optional[str]
    metrics: Optional[List]
