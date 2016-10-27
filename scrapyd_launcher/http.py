# -*- coding: utf-8 -*-

import os
import json
import time
import logging
import requests
from requests import exceptions


logger = logging.getLogger(__name__)


def _get_requests_json(response):
    try:
        return response.json()
    except ValueError:
        return {}


def _request(url, data, method, headers={}):
    max_retries = 5
    retries = 0
    method_call = getattr(requests, method.lower())
    while True:
        try:
            logger.info(
                'Calling [{}] "{}" with data: "{}"'.format(method, url, data))
            return method_call(url, data=json.dumps(data), headers=headers)
        except (exceptions.ConnectionError, exceptions.HTTPError) as e:
            retries += 1
            if retries >= max_retries:
                raise e
            time.sleep(2 * retries)


def report_webshooter(**kwargs):
    task_id = os.environ.get('SCRAPY_JOB', None)
    webshooter_api = os.environ.get('WEBSHOOTER_API', None)
    if webshooter_api:
        data = kwargs.copy()
        data['task_id'] = task_id
        response = _request(webshooter_api, data, 'POST', headers={
            'Content-type': 'application/json'
        })
        data = _get_requests_json(response)
        response.raise_for_status()
        return data
    else:
        logger.warning('Task not sent to webshooter.')
