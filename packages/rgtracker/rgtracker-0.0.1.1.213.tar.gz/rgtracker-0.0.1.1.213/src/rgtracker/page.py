from rgtracker.common import *
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import ClassVar
from redisgears import executeCommand as execute
from redisgears import log


@dataclass
class Page:
    id: str
    url: str = None
    article_id: str = None
    last_visited: str = None
    last_visited_rounded: field(init=False) = None
    dimension_key: field(init=False) = None
    dimension_ts_key: field(init=False) = None
    metric_pageviews_key: field(init=False) = None
    metric_unique_device_key: field(init=False) = None
    cms_width: ClassVar[int] = 2000
    cms_depth: ClassVar[int] = 5

    def __post_init__(self):
        dt = datetime.fromtimestamp(int(self.last_visited) / 1000) if self.last_visited is not None else None
        rounded_last_visited = int(round_time(dt).timestamp() * 1000)

        self.last_visited_rounded = rounded_last_visited
        self.dimension_key = f'{Type.JSON.value}::{Dimension.PAGE.value}:{self.id}::'
        self.dimension_ts_key = f'::{Dimension.PAGE.value}:{self.id}:{rounded_last_visited}:'
        self.metric_pageviews_key = f'{Type.CMS.value}::{Dimension.PAGE.value}::{rounded_last_visited}:{Metric.PAGEVIEWS.value}'
        self.metric_unique_device_key = f'{Type.HLL.value}::{Dimension.PAGE.value}:{self.id}:{rounded_last_visited}:{Metric.UNIQUE_DEVICES.value}'

    def create(self, website, section):
        execute('SADD', Dimension.PAGE.value, f'{self.id}:{self.url}')
        # tracker_log(f'SADD {Dimension.SECTION.value} {self.id}:{self.url}', f'Page - create - ')
        execute('JSON.SET', self.dimension_key, '.', json.dumps({
            'id': self.id,
            'url': self.url,
            'website': {
                'id': website.id,
                'name': website.name
            },
            'section': {
                'id': section.id,
                'name': section.name,
                'levels': section.levels
            },
            'article_id': self.article_id,
            'last_visited': self.last_visited
        }))
        # tracker_log(f'JSON.SET {self.dimension_key}', f'Page - create - ')
        execute('JSON.ARRAPPEND', section.dimension_key, '$.pages', json.dumps({
            'id': self.id,
            'url': self.url,
            'article_id': self.article_id,
            'last_visited': int(self.last_visited)
        }))
        # tracker_log(f'JSON.ARRAPPEND {section.dimension_key}', f'Page - create - ')
        execute('JSON.ARRAPPEND', website.dimension_key, '$.pages', json.dumps({
            'id': self.id,
            'url': self.url,
            'article_id': self.article_id,
            'last_visited': int(self.last_visited)
        }))
        # tracker_log(f'JSON.ARRAPPEND {website.dimension_key}', f'Page - create - ')

    def create_metrics(self):
        try:
            execute('CMS.INITBYDIM', self.metric_pageviews_key, self.cms_width, self.cms_depth)
            # log(f'CMS.INITBYDIM {self.metric_pageviews_key} {self.cms_width} {self.cms_depth}')
        except Exception:
            # log(f'S-create_metrics: key {self.metric_pageviews_key} already exists')
            pass

        try:
            execute('PFADD', self.metric_unique_device_key)
        except Exception as e:
            # tracker_log(f'{e} - {self.metric_pageviews_key}', 'Page - ')
            pass

    def incr_metrics(self, device_id):
        execute('CMS.INCRBY', self.metric_pageviews_key, self.id, 1)
        # log(f'CMS.INCRBY {self.metric_pageviews_key} {self.id} {1}')
        execute('PFADD', self.metric_unique_device_key, device_id)
        # log(f'PFADD {self.metric_unique_device_key} {device_id}')

    def expire_new_metrics(self):
        ttl_pageviews = execute('TTL', self.metric_pageviews_key)
        # tracker_log(f'TTL {self.metric_pageviews_key} {ttl_pageviews}', 'Page - expire new - ')
        if ttl_pageviews == -1:
            expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
            # tracker_log(f'Expire key {self.metric_pageviews_key} = {expire_pg}', f'Page - expire_new_metrics - ')

        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Page - expire new ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Page - expire_new_metrics - ')

    # Todo: put expire in method params
    def expire_metrics(self):
        expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_pageviews_key} = {expire_pg}', f'Page - expire_metrics - ')
        expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_unique_device_key} = {expire_ud}', f'Page - expire_metrics - ')

    def expire_record_metrics(self):
        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Page - expire_record_metrics - ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Page - expire_record_metrics - ')

    def is_exists(self):
        x = execute('EXISTS', self.dimension_key)
        # log(f'EXISTS {self.dimension_key} => {x}')
        return x

    def has_metrics(self):
        x = execute('EXISTS', self.metric_pageviews_key)
        # tracker_log(f'EXISTS {self.metric_pageviews_key} - {x}', 'Page - ')
        # z = execute('EXISTS', self.metric_unique_device_key)
        # log(f'EXISTS {self.metric_unique_device_key} => {z}')
        # return x + z
        return x

    def update_last_visited(self):
        execute('JSON.SET', self.dimension_key, '.last_visited', self.last_visited)
        # log(f'update_last_visited: JSON.SET {self.dimension_key} .last_visited {self.last_visited}')

    def notification_of_new_page(self, stream_names):
        # tracker_log(f'{self.last_visited_rounded} new page {self.id}', f'Page - notification_of_new_page - ')
        execute('XADD', stream_names.get('page_pageviews'), 'MAXLEN', '86400000', '*',
                'ts', self.last_visited_rounded,
                'status', 'new',
                'ids', self.id)
        execute('XADD', stream_names.get('page_unique_devices'), 'MAXLEN', '86400000', '*',
                'ts', self.last_visited_rounded,
                'status', 'new',
                'ids', self.id)

    def notification_of_active_pages(self, stream_names):
        prev_unix_ts = int(
            (datetime.fromtimestamp(int(self.last_visited_rounded) / 1000) - timedelta(minutes=1)).timestamp() * 1000)

        # Todo: create index_name with method instead of hard coding it
        ids_numbers = int(
            execute('FT.SEARCH', 'I::P:::', f'@last_visited:[{prev_unix_ts} {self.last_visited_rounded}]', 'LIMIT', 0,
                    0)[0])
        ids_raw = execute('FT.SEARCH', 'I::P:::', f'@last_visited:[{prev_unix_ts} {self.last_visited_rounded}]',
                          'LIMIT', 0, ids_numbers, 'RETURN', '1', 'id')
        ids = []
        for d in ids_raw:
            if type(d) is list:
                ids.append(d[-1])

        # FixMe: HOT FIX
        if len(ids) > 0:
            tracker_log(
                f'[{datetime.fromtimestamp(prev_unix_ts / 1000)} - {datetime.fromtimestamp(int(self.last_visited_rounded) / 1000)}] {len(ids)} active pages',
                f'Page - notification_of_active_pages - ')
            execute('XADD', stream_names.get('page_pageviews'), 'MAXLEN', '86400000', '*',
                    'ts', self.last_visited_rounded,
                    'status', 'active',
                    'ids', json.dumps(ids))
            execute('XADD', stream_names.get('page_unique_devices'), 'MAXLEN', '86400000', '*',
                    'ts', self.last_visited_rounded,
                    'status', 'active',
                    'ids', json.dumps(ids))
        else:
            tracker_log(
                f'[{datetime.fromtimestamp(prev_unix_ts / 1000)} - {datetime.fromtimestamp(int(self.last_visited_rounded) / 1000)}] {len(ids)} active pages',
                f'Page - notification_of_active_websites - warning - ')

    def send_to_enrich(self):
        execute('XADD', 'ST:ENRICH:P:::', 'MAXLEN', '86400000', '*', 'key', self.dimension_key, 'article_id',
                self.article_id)


def load_page(website, section, page, device, output_stream_names):
    if page.is_exists() != 1:
        page.create(website, section)
        page.create_metrics()
        page.incr_metrics(device.id)
        page.expire_new_metrics()
        page.notification_of_new_page(stream_names=output_stream_names)
        page.send_to_enrich()
    else:
        if page.has_metrics() < 1:
            page.create_metrics()
            page.incr_metrics(device.id)
            page.expire_metrics()
            page.update_last_visited()
            page.notification_of_active_pages(stream_names=output_stream_names)
        else:
            page.incr_metrics(device.id)
            page.expire_record_metrics()
            page.update_last_visited()
