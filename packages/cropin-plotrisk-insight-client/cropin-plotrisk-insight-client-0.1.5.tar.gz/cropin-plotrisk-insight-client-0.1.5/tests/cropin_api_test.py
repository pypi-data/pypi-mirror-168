import base64
import logging

from python_sdk_client.clients_enum import EnvType
from python_sdk_client.cropin_api import CropinAPI

"""Example on how to use CropAPI.  
"""
if __name__ == '__main__':
    logging.info(">>>>>>>>>>>> starting")

    # authenticate
    cropin_api = CropinAPI("test", "12345678", "admin", env=EnvType.DEV)

    # plot details without any filter
    plot_response = cropin_api.get_plot_details()
    print("plot details without any filters is : {}".format(plot_response))

    # satellite data without any filter
    satellite_response = cropin_api.get_satellite_details()
    print("satellite metrics with no filters :{}".format(satellite_response))

    # satellite data with boundary_id filter
    satellite_response = cropin_api.get_satellite_details(ca_ids='7101')
    print("satellite metrics when boundaryId is passed : {}".format(satellite_response))
    #
    # # # yield data without any filter
    # yield_response = cropin_api.get_yield_details()
    # print("yield data with no filter passed :{}".format(yield_response))
    # #
    # # # weather data without any filter
    # weather_response = cropin_api.get_weather_details(ca_ids='9301')
    # print("weather data with no filter passed :{}".format(weather_response))
    # #
    # # # plot image download
    # download_response = cropin_api.download_image(ca_id='6801', image_name='NDVI',
    #                                               image_type='PNG', date='2022-06-30')
    # print("download_response is: {}".format(download_response))
    #
    # # code to convert the bytes to image
    # imgdata = base64.b64decode(download_response['bytes'])
    # filename = 'image.jpg'
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)
