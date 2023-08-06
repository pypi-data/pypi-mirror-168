import numbers
from pprint import pprint

import plotrisk_python_client

from python_sdk_client.libs.client_cfg import InsightServiceCfg


def handle(anotherfunc, input_str, batch_size: numbers = 300, **kwargs):
    response = []
    if input_str is None:
        temp_resp = anotherfunc(**kwargs)
        if temp_resp is None or 'records' not in temp_resp or temp_resp['records'] is None:
            return response

        response = response + temp_resp['records']
        if temp_resp['totalPages'] is not None:
            total_pages = int(temp_resp['totalPages'])
            if temp_resp['currentPageItems'] > 0:
                total_pages = int(min(total_pages, InsightServiceCfg.MAX_SIZE / temp_resp['currentPageItems']))
            for i in range(1, total_pages, 1):
                temp_resp = anotherfunc(page=i, **kwargs)
                response = response + temp_resp['records']
        return response

    if input_str is not None:
        input_list = input_str.split(", ")
        for i in range(0, len(input_list), batch_size):
            current_batch = input_list[i:i + batch_size]
            current_batch_str = ','.join(current_batch)
            temp_resp = anotherfunc(ids=current_batch_str, **kwargs)
            if temp_resp is not None and 'records' in temp_resp and temp_resp['records'] is not None:
                response = response + temp_resp['records']
        return response


def handleplotdetails(anotherfunc, batch_size: numbers = 300, **kwargs):
    response = []
    temp_resp = anotherfunc(size=batch_size)

    if temp_resp is None:
        return response[0]

    response = response + temp_resp[0]
    if temp_resp[2] is not None and int(temp_resp[2].get('X-Total-Count')) > 0:
        total_pages = int(temp_resp[2].get('X-Total-Count'))
        for i in range(1, total_pages, 1):
            temp_resp = anotherfunc(page=i, **kwargs)
            response = response + temp_resp[0]
    return response



