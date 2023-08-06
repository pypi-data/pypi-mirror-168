import inspect
from typing import Callable, Union
from humanloop.api.models.metric import UpdateMetricRequest, CreateMetricRequest, MetricResponse

from humanloop.sdk.init import _get_client

# TODO given Metric.id is globally unique, should remove the need for specifying
# project_id as part of update and delete

# TODO pull out the *args, **kwargs validation logic into a separate function to remove duplication


def create_metric(*args, **kwargs) -> MetricResponse:
    """Create a metric with name, description and code."""

    if len(args) > 0:
        if len(args) != 1:
            raise ValueError(
                "When passing arguments, only a single argument is accepted. "
                "This should be a single `CreateMetricRequest` object."
            )
        if len(kwargs) != 0:
            raise ValueError(
                "Either pass arguments of type `CreateMetricRequest` or the keyword arguments required, not both."
            )
        return _create_metric(args[0])
    elif len(kwargs) > 0:
        return _create_metric(CreateMetricRequest(**kwargs))
    else:
        raise ValueError(
            "Provide a CreateMetricRequest or the keyword arguments to create a CreateMetricRequest object."
        )


def _create_metric(metric: CreateMetricRequest) -> MetricResponse:
    client = _get_client()
    project_id = client.get_project(metric.project).internal_id
    if metric.code is not None:
        metric.code = _process_metric_code(metric.code)
    return client.create_metric(project_id=project_id, metric=metric)


def update_metric(*args, **kwargs) -> MetricResponse:
    """Update metric definition."""
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError(
                "When passing arguments, only a single argument is accepted. "
                "This should be a single `UpdateMetricRequest` object."
            )
        if len(kwargs) != 0:
            raise ValueError(
                "Either pass arguments of type `UpdateMetricRequest` or the keyword arguments required, not both."
            )
        return _update_metric(args[0])
    elif len(kwargs) > 0:
        return _update_metric(UpdateMetricRequest(**kwargs))
    else:
        raise ValueError(
            "Provide a UpdateMetricRequest or the keyword arguments to create an UpdateMetricRequest object. "
        )


def _update_metric(metric: UpdateMetricRequest) -> MetricResponse:
    client = _get_client()
    project_id = client.get_project(metric.project).internal_id
    if metric.code is not None:
        metric.code = _process_metric_code(metric.code)
    return client.update_metric(
        project_id=project_id, metric_id=metric.id, request=metric
    )


def get_metrics(project: str) -> MetricResponse:
    """Get metrics for a given project."""
    client = _get_client()
    project_id = client.get_project(project).intenral_id
    return client.get_metrics(project_id)


def delete_metric(project: str, metric_id: str) -> MetricResponse:
    """Delete metric definition."""
    client = _get_client()
    project_id = client.get_project(project).internal_id
    return client.delete_metric(project_id, metric_id)


def _process_metric_code(code: Union[str, Callable]) -> str:
    """
    Validates that metric is valid for sending to client.
    The client expects a string, so if a function object is provided, it is converted to
    a string.
    TODO add compile and run checks (currently happen server side)
    """
    if isinstance(code, str):
        return code

    if callable(code):
        return inspect.getsource(code)
    else:
        raise ValueError("code is not a callable or a string")

