from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.client_helpers import v2_alpha_client
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.v2.alpha.v2_alpha_app_service import V2AlphaAppService
from benchling_sdk.services.v2.base_service import BaseService


class V2AlphaService(BaseService):
    """
    V2-alpha.

    Alpha endpoints have different stability guidelines than other stable endpoints.

    See https://benchling.com/api/v2-alpha/reference
    """

    _app_service: V2AlphaAppService

    def __init__(self, client: Client, retry_strategy: RetryStrategy = RetryStrategy()):
        """
        Initialize a v2-alpha service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        super().__init__(client, retry_strategy)
        alpha_client = v2_alpha_client(self.client)
        self._app_service = V2AlphaAppService(alpha_client, retry_strategy)

    @property
    def apps(self) -> V2AlphaAppService:
        """
        V2-Alpha Apps.

        Create and manage Apps on your tenant.

        https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps
        """
        return self._app_service
