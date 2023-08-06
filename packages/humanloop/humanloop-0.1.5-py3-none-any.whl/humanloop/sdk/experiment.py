from humanloop.api.models.experiment import TrialResponse
from humanloop.sdk.init import _get_client


def trial(experiment_id: str) -> TrialResponse:
    """Generates a model config according to your experiment to use to execute
     your model.

    The returned TrialResponse contains a `.id` attribute that can be used in a
    subsequent log to such that the log contributes to the experiment.
    """
    client = _get_client()
    return client.trial(experiment_id)
