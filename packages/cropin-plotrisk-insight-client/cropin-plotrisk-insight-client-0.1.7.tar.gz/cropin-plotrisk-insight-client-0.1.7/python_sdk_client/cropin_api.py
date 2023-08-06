import logging

from python_sdk_client.clients_enum import EnvType
from python_sdk_client.libs.cropin_client import CropinClient


class CropinAPI:
    """Class to connect CropinAPI to do different operations.
    As part of initialization, it's first step is Authentication.

    Parameters
    ----------
    tenant : string
        tenant for Cropin
    username : string
        username for Cropin
    password : string
        password for Cropin

    """

    logger = logging.getLogger("insights-sdk.CropinAPI")

    def __init__(self, tenant: str, username: str, password: str, env: EnvType = EnvType.PROD):
        self.cropin_client = CropinClient(tenant, username, password, env)
        print("CropinAPI is ready !!!!")

    def get_plot_details(self, plot_ids: str = None, **kwargs) -> list:

        return self.cropin_client.get_plot_details(plot_ids, **kwargs)

    def get_satellite_details(self, ids: str = None, **kwargs) -> list:
        """ Fetch satellite details for the plot ids passed.

        Satellite details returns data for satellite indices and
        crop details for the models subscribed.

        :param Ref ca_ids: Unique identifiers for plot/CA, e.g. ids=1234,5678
        :param str captured_date_time: Indicates timestamp when satellite insights processed, e.g. date = 2021-12-23T00:00:00Z
        :param str category: Cloud mask parameter.
        :param str max_cloud_coverage: Cloud coverage refers the fraction of sky covered with clouds, filters record where cloudCoverge <= maxCloudCoverage
        :param str min_cloud_coverage: Cloud coverage refers the fraction of sky covered with clouds, filters record where cloudCoverge >= minCloudCoverage
        :param str order_by: Order the result in ascending or descending format. Default order is 'ASC'
        :param Ref page: Page represents page no. in a paginated response.Page starts from 0, valid page can be zero or a positive number.
        :param Ref select: Select specific field or fields to return as part of result, e.g select = fieldName
        :param Ref size: Size represents the number of records that are displayed when a page loads,it can be between 10 to 300. Default size is 50.
        :param list[str] sort: Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :param str sort_by: Sort the result based on given field/fields in natural sorting order (ASC). Maximum 2 fields are allowed.
        """
        return self.cropin_client.get_satellite_details(ids, **kwargs)

    def get_weather_details(self, ids: str = None, **kwargs) -> list:
        """
        Fetches weather details for the plot ids passed.

        :param int ca_id: Unique identifier for plot/CA , e.g. id= 1234
        :param str _date: Indicates timestamp when satellite insights processed, e.g. date = 2021-12-23T00:00:00Z
        :param str date_from: Filter records for specific date range e.g. dateFrom = 2021-12-23T00:00:00Z
        :param str date_to: Filter records for specific date range e.g. dateTo = 2021-12-23T00:00:00Z
        :param str order_by: Order the result in ascending or descending format. Default order is 'ASC'
        :param Ref page: Page represents page no. in a paginated response.Page starts from 0, valid page can be zero or a positive number.
        :param Ref size: Size represents the number of records that are displayed when a page loads,it can be between 10 to 300. Default size is 50.
        :param list[str] sort: Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :param str sort_by: Sort the result based on given field/fields in natural sorting order (ASC). Maximum 2 fields are allowed.
        """
        return self.cropin_client.get_weather_details(ids, **kwargs)

    def get_yield_details(self, ids: str = None, **kwargs) -> list:
        """
        Fetches yield details for the plot ids passed.

        :param int ca_id: Unique identifier for plot/CA , e.g. id= 1234
        :param str order_by: Order the result in ascending or descending format. Default order is 'ASC'
        :param Ref page: Page represents page no. in a paginated response.Page starts from 0, valid page can be zero or a positive number.
        :param Ref size: Size represents the number of records that are displayed when a page loads,it can be between 10 to 300. Default size is 50.
        :param list[str] sort: Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :param str sort_by: Sort the result based on given field/fields in natural sorting order (ASC). Maximum 2 fields are allowed.

        """
        return self.cropin_client.get_yield_details(ids, **kwargs)

    def download_image(self, ca_id: str, image_name, image_type, date) -> dict:
        """

        Returns plot image byte streams for a single plot id at a given date and image type and name.

        :param int ca_id: Unique identifier for plot/CA , e.g. id= 1234 (required)
        :param str _date: Indicates captured satellite date in yyyy-MM-dd format, e.g. date=2022-03-15 (required)
        :param str image_name: Plot image name, e.g imageName = NDRE . (required)
        :param str image_type: Plot image type, e.g imageType = TIFF

        """
        return self.cropin_client.download_image(ca_id, image_name, image_type, date)
