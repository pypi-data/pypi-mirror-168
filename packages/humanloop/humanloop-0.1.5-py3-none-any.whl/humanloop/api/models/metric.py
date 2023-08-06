import datetime
from typing import List, Optional, Callable, Union
from pydantic import BaseModel


class CreateMetricRequest(BaseModel):
    name: str
    project: str
    description: str
    code: Union[Callable, str]


class UpdateMetricRequest(BaseModel):
    id: str
    project: str
    name: Optional[str]
    description: Optional[str]
    code: Optional[Union[Callable, str]]
    active: Optional[bool]


class MetricExperimentResponse(BaseModel):
    id: str
    name: str


class BaseMetricResponse(BaseModel):
    id: str
    name: str
    description: str
    code: str
    default: bool
    active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class MetricResponse(BaseMetricResponse):
    experiments: List[MetricExperimentResponse]
    num_values: int


