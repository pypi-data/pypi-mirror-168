import logging

from python_sdk_client.clients_enum import EnvType
from python_sdk_client.libs.insight_service_client import InsightServiceClient


class CropinClient:

    def __init__(self, tenant: str, username: str, password: str, env: EnvType):
        logging.info("Initializing Cropin Client")
        self.insight_service_client = InsightServiceClient(tenant, username, password, env)
        logging.info("Initialized Cropin Client")

    def get_plot_details(self, plot_ids: str, **kwargs):
        return self.insight_service_client.get_plot_details(plot_ids, **kwargs)

    def get_satellite_details(self, plot_ids: str, **kwargs):
        return self.insight_service_client.get_satellite_details(plot_ids, **kwargs)

    def get_weather_details(self, plot_ids: str, **kwargs):
        return self.insight_service_client.get_weather_details(plot_ids, **kwargs)

    def get_yield_details(self, plot_ids: str, **kwargs):
        return self.insight_service_client.get_yield_details(plot_ids, **kwargs)

    def download_image(self, ca_id: str, image_name, image_type, date):
        return self.insight_service_client.download_image(ca_id, image_name, image_type, date)
