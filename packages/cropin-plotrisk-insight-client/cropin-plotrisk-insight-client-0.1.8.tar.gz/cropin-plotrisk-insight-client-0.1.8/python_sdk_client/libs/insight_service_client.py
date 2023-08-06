import plotrisk_python_client
from plotrisk_python_client import Configuration

from python_sdk_client.libs.abstract_client import AbstractClient
from python_sdk_client.libs.batch_processor import handle, handleplotdetails
from python_sdk_client.libs.client_cfg import InsightServiceCfg
from python_sdk_client.clients_enum import EnvType

"""
Insights Service Client
-----------------------

class to validate the inputs and set the env, endpoint and other env specific details.
"""


class InsightServiceClient(AbstractClient):
    """
    Initialising the env and base url
    """

    def __init__(self, tenant: str, username: str, password: str, env: EnvType) -> None:
        super(InsightServiceClient, self).__init__(tenant, username, password, env)

        self.tenant_type = 'SMARTFARM_PLUS'

        if env.value == EnvType.PROD.value:
            self.base_url = InsightServiceCfg.PROD_BASE_URL
        elif env.value == EnvType.QA.value:
            self.base_url = InsightServiceCfg.QA_BASE_URL
        elif env.value == EnvType.DEV.value:
            self.base_url = InsightServiceCfg.DEV_BASE_URL
        elif env.value == EnvType.PROD2.value:
            self.base_url = InsightServiceCfg.PROD2_BASE_URL
        else:
            self.base_url = InsightServiceCfg.PROD_BASE_URL

        self.configuration = Configuration()
        # set base url
        self.configuration.host = self.base_url
        # set auth token
        self.configuration.api_key['Authorization'] = self.token

    """
    Validate input for fetching plot details
    """

    def get_plot_details(self, plot_ids: str, **kwargs):

        boundary_api = plotrisk_python_client.PlotRiskResourceApi(plotrisk_python_client.ApiClient(self.configuration))
        plot_ids_resp = handleplotdetails(boundary_api.get_plots_using_get,
                                          batch_size=InsightServiceCfg.BATCH_SIZE, **kwargs)
        return plot_ids_resp

    """
    Validate inputs for satellite delist_all3tails
    """

    def get_satellite_details(self, plot_ids: str, **kwargs):

        metrics_api = plotrisk_python_client.PlotRiskResourceApi(plotrisk_python_client.ApiClient(self.configuration))
        plot_ids_resp = handle(metrics_api.get_satellite_using_get, plot_ids,
                               batch_size=InsightServiceCfg.BATCH_SIZE, **kwargs)
        return plot_ids_resp

    """
    Validate inputs for weather details
    """

    def get_weather_details(self, plot_ids: str, **kwargs):

        weather_api = plotrisk_python_client.PlotRiskResourceApi(plotrisk_python_client.ApiClient(self.configuration))
        weather_api_resp = handle(weather_api.get_weather_using_get, plot_ids,
                                  batch_size=InsightServiceCfg.BATCH_SIZE, **kwargs)
        return weather_api_resp

    """ 
    Validate inputs for yield details
    """

    def get_yield_details(self, plot_ids: str, **kwargs):
        yield_api = plotrisk_python_client.PlotRiskResourceApi(plotrisk_python_client.ApiClient(self.configuration))
        yield_api_resp = handle(yield_api.get_yield_using_get, plot_ids,
                                batch_size=InsightServiceCfg.BATCH_SIZE, **kwargs)
        return yield_api_resp

    """
    Validate inputs for download plot image
    """

    def download_image(self, ca_id: str, image_name, image_type, date):
        download_api = plotrisk_python_client.PlotRiskResourceApi(plotrisk_python_client.ApiClient(self.configuration))
        file_response = download_api.download_image_using_get(image_type=image_type,
                                                              image_name=image_name, _date=date,
                                                              ca_id=ca_id)
        return file_response
