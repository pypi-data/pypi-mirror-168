from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status


def model_from_detailed(response: Response):
    """Deserialize a response into a model."""
    raise_for_status(response)
    return response.parsed
