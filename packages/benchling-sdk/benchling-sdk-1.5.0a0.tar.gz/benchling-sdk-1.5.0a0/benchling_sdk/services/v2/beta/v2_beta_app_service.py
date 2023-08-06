from benchling_api_client.v2.beta.api.apps import get_app_configuration_by_app_id
from benchling_api_client.v2.beta.models.benchling_app_configuration import BenchlingAppConfiguration

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaAppService(BaseService):
    """
    V2-Beta Apps.

    Create and manage Apps on your tenant.

    https://benchling.com/api/v2-beta/reference?stability=not-available#/Apps
    """

    @api_method
    def get_configuration_by_app_id(self, app_id: str) -> BenchlingAppConfiguration:
        """
        Get an app's configuration by app id.

        See https://benchling.com/api/v2-beta/reference?stability=la#/Apps/getAppConfigurationByAppID
        """
        response = get_app_configuration_by_app_id.sync_detailed(client=self.client, app_id=app_id)
        return model_from_detailed(response)
