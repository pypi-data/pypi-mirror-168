from rgtracker.common import *
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from redisgears import executeCommand as execute


@dataclass
class Section:
    id: str
    name: str = None
    levels: dict = None
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
        self.dimension_key = f'{Type.JSON.value}::{Dimension.SECTION.value}:{self.id}::'
        self.dimension_ts_key = f'::{Dimension.SECTION.value}:{self.id}:{rounded_last_visited}:'
        self.metric_pageviews_key = f'{Type.CMS.value}::{Dimension.SECTION.value}::{rounded_last_visited}:{Metric.PAGEVIEWS.value}'
        self.metric_unique_device_key = f'{Type.HLL.value}::{Dimension.SECTION.value}:{self.id}:{rounded_last_visited}:{Metric.UNIQUE_DEVICES.value}'

    def create(self, website):
        execute('SADD', Dimension.SECTION.value, f'{self.id}:{self.name}')
        # log(f'SADD {Dimension.SECTION.value} {self.id}:{self.name}')
        l = []
        [l.extend([k, v]) for k, v in self.levels.items()]
        levels = convert_list_to_dict(l)
        execute('JSON.SET', self.dimension_key, '.', json.dumps({
            'id': self.id,
            'website': {
                'id': website.id,
                'name': website.name
            },
            'name': self.name,
            **levels,
            'pages': [],
            'last_visited': self.last_visited,
        }))
        # log(f'JSON.SET {self.dimension_key}')
        execute('JSON.ARRAPPEND', website.dimension_key, '$.sections', json.dumps({
            'id': self.id,
            'name': self.name,
            # **self.levels,
            'last_visited': int(self.last_visited)
        }))
        # log(f'JSON.ARRAPPEND {website.dimension_key} $.sections')

    def create_metrics(self):
        try:
            execute('CMS.INITBYDIM', self.metric_pageviews_key, self.cms_width, self.cms_depth)
            # log(f'CMS.INITBYDIM {self.metric_pageviews_key} {self.cms_width} {self.cms_depth}')
        except Exception:
            # tracker_log(f'{e} - {self.metric_pageviews_key}', 'Section - ')
            pass

        try:
            execute('PFADD', self.metric_unique_device_key)
        except Exception as e:
            # tracker_log(f'{e} - {self.metric_pageviews_key}', 'Section - ')
            pass

    def incr_metrics(self, device_id):
        execute('CMS.INCRBY', self.metric_pageviews_key, self.id, 1)
        # log(f'CMS.INCRBY {self.metric_pageviews_key} {self.id} {1}')
        execute('PFADD', self.metric_unique_device_key, device_id)
        # log(f'PFADD {self.metric_unique_device_key} {device_id}')

    def expire_new_metrics(self):
        ttl_pageviews = execute('TTL', self.metric_pageviews_key)
        # tracker_log(f'TTL {self.metric_pageviews_key} {ttl_pageviews}', 'Section - expire new - ')
        if ttl_pageviews == -1:
            expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
            # tracker_log(f'Expire key {self.metric_pageviews_key} = {expire_pg}', f'Section - expire_new_metrics - ')

        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Section - expire new ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Section - expire_new_metrics - ')

    # Todo: put expire in method params
    def expire_metrics(self):
        expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_pageviews_key} = {expire_pg}', f'Section - expire_metrics - ')
        expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_unique_device_key} = {expire_ud}', f'Section - expire_metrics - ')

    def expire_record_metrics(self):
        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Section - expire_record_metrics - ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Section - expire_record_metrics - ')

    def is_exists(self):
        x = execute('EXISTS', self.dimension_key)
        # log(f'EXISTS {self.dimension_key} => {x}')
        return x

    def has_metrics(self):
        x = execute('EXISTS', self.metric_pageviews_key)
        # log(f'EXISTS {self.metric_pageviews_key} => {x}')
        # z = execute('EXISTS', self.metric_unique_device_key)
        # log(f'EXISTS {self.metric_unique_device_key} => {z}')
        # return x + z
        return x

    def update_last_visited(self):
        execute('JSON.SET', self.dimension_key, '.last_visited', self.last_visited)
        # log(f'update_last_visited: JSON.SET {self.dimension_key} .last_visited {self.last_visited}')

    def notification_of_new_section(self, stream_names):
        # tracker_log(f'{self.last_visited_rounded} new section {self.id}', f'Section - notification_of_new_section - ')
        execute('XADD', stream_names.get('section_pageviews'), 'MAXLEN', '864000', '*',
                'ts', self.last_visited_rounded,
                'status', 'new',
                'ids', self.id)
        execute('XADD', stream_names.get('section_unique_devices'), 'MAXLEN', '864000', '*',
                'ts', self.last_visited_rounded,
                'status', 'new',
                'ids', self.id)

    def notification_of_active_sections(self, stream_names):
        prev_unix_ts = int(
            (datetime.fromtimestamp(int(self.last_visited_rounded) / 1000) - timedelta(minutes=1)).timestamp() * 1000)

        # Todo: create index_name with method instead of hard coding it
        ids_numbers = int(
            execute('FT.SEARCH', 'I::S:::', f'@last_visited:[{prev_unix_ts} {self.last_visited_rounded}]', 'LIMIT', 0,
                    0)[0])
        ids_raw = execute('FT.SEARCH', 'I::S:::', f'@last_visited:[{prev_unix_ts} {self.last_visited_rounded}]',
                          'LIMIT', 0, ids_numbers, 'RETURN', '1', 'id')
        ids = []
        for d in ids_raw:
            if type(d) is list:
                ids.append(d[-1])

        # FixMe: HOT FIX
        if len(ids) > 0:
            tracker_log(
                f'[{datetime.fromtimestamp(prev_unix_ts / 1000)} - {datetime.fromtimestamp(int(self.last_visited_rounded) / 1000)}] {len(ids)} active sections',
                f'Section - notification_of_active_sections - ')
            execute('XADD', stream_names.get('section_pageviews'), 'MAXLEN', '864000', '*',
                    'ts', self.last_visited_rounded,
                    'status', 'active',
                    'ids', json.dumps(ids))
            execute('XADD', stream_names.get('section_unique_devices'), 'MAXLEN', '864000', '*',
                    'ts', self.last_visited_rounded,
                    'status', 'active',
                    'ids', json.dumps(ids))
        else:
            tracker_log(
                f'[{datetime.fromtimestamp(prev_unix_ts / 1000)} - {datetime.fromtimestamp(int(self.last_visited_rounded) / 1000)}] {len(ids)} active sections',
                f'Section - notification_of_active_websites - warning - ')

    def send_to_enrich(self):
        execute('XADD', 'ST:ENRICH:S:::', 'MAXLEN', '600', '*', 'key', self.dimension_key)


def load_section(website, section, page, device, output_stream_names):
    if section.is_exists() != 1:
        section.create(website)
        section.create_metrics()
        section.incr_metrics(device.id)
        section.expire_new_metrics()
        section.notification_of_new_section(stream_names=output_stream_names)
        section.send_to_enrich()
    else:
        if section.has_metrics() < 1:
            section.create_metrics()
            section.incr_metrics(device.id)
            section.expire_metrics()
            section.update_last_visited()
            section.notification_of_active_sections(stream_names=output_stream_names)
        else:
            section.incr_metrics(device.id)
            section.expire_record_metrics()
            section.update_last_visited()
