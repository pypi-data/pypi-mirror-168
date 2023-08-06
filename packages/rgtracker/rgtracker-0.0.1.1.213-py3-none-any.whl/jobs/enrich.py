from rgtracker.common import *
from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from redisgears import executeCommand as execute
import json
import sys
import datetime

import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504, 404),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def enrich_page(record):
    key = record['value']['key']
    article_id = record['value']['article_id']
    api_url = f"http://rtl-curator.back.k8s.rtl/items/urn:newstool:article:{article_id}"
    try:
        response_json = requests_retry_session().get(api_url).json()
        element = datetime.datetime.strptime(response_json.get('display_date'), "%Y-%m-%dT%H:%M:%S%z")
        timestamp = round(datetime.datetime.timestamp(element) * 1000)
        result = {
            'kicker': response_json.get('kicker'),
            'title': response_json.get('title'),
            'display_date': timestamp
        }
        execute('JSON.SET', key, '$.metadata', json.dumps(result))
        # tracker_log(f'{key} - {result} - OK', prefix='Enrich - ')
    except requests.exceptions.RequestException as e:
        # tracker_log(f'{e} for {key}', prefix='Enrich - ', log_level='warning')
        pass


tracker_log(f'Register EnrichPage ...')

desc_json = {
    "name": 'Enrich',
    "version": '99.99.99',
    "desc": f"Enrich Website, Section and Page"
}
# unregister_old_versions(desc_json.get('name'), desc_json.get('version'))
GB("StreamReader", desc=json.dumps(desc_json)). \
    foreach(enrich_page). \
    register(
    prefix='ST:ENRICH:P:::',
    convertToStr=True,
    collect=True,
    onFailedPolicy='abort',
    onFailedRetryInterval=1,
    batch=1,
    duration=0,
    trimStream=False)

tracker_log(f'Register EnrichPage OK')
