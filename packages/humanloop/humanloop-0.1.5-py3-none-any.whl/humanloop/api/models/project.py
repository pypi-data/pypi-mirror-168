import datetime
from typing import List, Literal, Union

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: str
    # TODO remove with cleanup of metric routers
    internal_id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CategoricalFeedbackGroup(BaseModel):
    name: str
    labels: List[str]
    type: Literal["categorical"]


class TextFeedbackGroup(BaseModel):
    name: str
    type: Literal["text"]


class FeedbackSchema(BaseModel):
    groups: List[Union[TextFeedbackGroup, CategoricalFeedbackGroup]]
