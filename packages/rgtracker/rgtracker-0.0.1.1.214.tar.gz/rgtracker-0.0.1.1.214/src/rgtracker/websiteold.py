from rgtracker.common import *
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import ClassVar
from redisgears import executeCommand as execute
from redisgears import log


@dataclass
class Website:
    id: str
    name: str = None
    last_visited: str = None
    dimension_key: field(init=False) = None
    dimension_ts_key: field(init=False) = None
    metric_pageviews_key: field(init=False) = None
    metric_unique_device_key: field(init=False) = None
    cms_width: ClassVar[int] = 2000
    cms_depth: ClassVar[int] = 5

    def __post_init__(self):
        if len(self.last_visited.split('_')) > 1:
            self.dimension_key = f'{Type.JSON.value}::{Dimension.WEBSITE.value}:{self.id}::'
            self.dimension_ts_key = f'::{Dimension.WEBSITE.value}:{self.id}:{self.last_visited}:'
            self.metric_pageviews_key = f'{Type.CMS.value}::{Dimension.WEBSITE.value}::{self.last_visited}:{Metric.PAGEVIEWS.value}'
            self.metric_unique_device_key = f'{Type.HLL.value}::{Dimension.WEBSITE.value}:{self.id}:{self.last_visited}:{Metric.UNIQUE_DEVICES.value}'
            # log(f'__post_init__ len(last_visited) > 1  \n{self.dimension_key}\n{self.metric_pageviews_key}\n{self.metric_unique_device_key}')
        else:
            dt = datetime.fromtimestamp(int(self.last_visited) / 1000) if self.last_visited is not None else None
            rounded_last_visited = int(round_time(dt).timestamp() * 1000)
            # tracker_log(f'Rounded time: {dt} to {rounded_last_visited}', f'Website - ')
            self.dimension_key = f'{Type.JSON.value}::{Dimension.WEBSITE.value}:{self.id}::'
            self.dimension_ts_key = f'::{Dimension.WEBSITE.value}:{self.id}:{rounded_last_visited}:'
            self.metric_pageviews_key = f'{Type.CMS.value}::{Dimension.WEBSITE.value}::{rounded_last_visited}:{Metric.PAGEVIEWS.value}'
            self.metric_unique_device_key = f'{Type.HLL.value}::{Dimension.WEBSITE.value}:{self.id}:{rounded_last_visited}:{Metric.UNIQUE_DEVICES.value}'
            # log(f'__post_init__ len(last_visited) > 1  \n{self.dimension_key}\n{self.metric_pageviews_key}\n{self.metric_unique_device_key}')

    def create(self):
        execute('SADD', Dimension.WEBSITE.value, f'{self.id}:{self.name}')
        # log(f'SADD websites {self.name}:{self.id}')
        execute('JSON.SET', self.dimension_key, '.', json.dumps({
            'id': self.id,
            'name': self.name,
            'last_visited': self.last_visited,
            'sections': [],
            'pages': []
        }))
        # log(f'JSON.SET {self.dimension_key}')

    def create_metrics(self):
        try:
            execute('CMS.INITBYDIM', self.metric_pageviews_key, self.cms_width, self.cms_depth)
            # tracker_log(f'CMS.INITBYDIM {self.metric_pageviews_key}', f'Website - create_metrics - ')
        except Exception as e:
            # tracker_log(f'{e} - {self.metric_pageviews_key}', 'Website - ')
            pass

        try:
            execute('PFADD', self.metric_unique_device_key)
            # tracker_log(f'PFADD {self.metric_unique_device_key}', f'Website - create_metrics - ')
        except Exception as e:
            # tracker_log(f'{e} - {self.metric_pageviews_key}', 'Website - ')
            pass

    def incr_metrics(self, device_id):
        execute('CMS.INCRBY', self.metric_pageviews_key, self.id, 1)
        # tracker_log(f'CMS.INCRBY {self.metric_pageviews_key} {self.id} 1', f'Website - incr_metrics - ')
        execute('PFADD', self.metric_unique_device_key, device_id)
        # tracker_log(f'PFADD {self.metric_unique_device_key} {device_id}', f'Website - incr_metrics - ')

    def expire_new_metrics(self):
        ttl_pageviews = execute('TTL', self.metric_pageviews_key)
        # tracker_log(f'TTL {self.metric_pageviews_key} {ttl_pageviews}', 'Website - expire new - ')
        if ttl_pageviews == -1:
            expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
            # tracker_log(f'Expire key {self.metric_pageviews_key} = {expire_pg}', f'Website - expire_new_metrics - ')

        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Website - expire new ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Website - expire_new_metrics - ')

    # Todo: put expire time in method params
    def expire_metrics(self):
        # Todo: compare current time with self.last_visited and apply : (self.last_visited - current_time) + expire_time
        # That leaves time for further merger services

        expire_pg = execute('EXPIRE', self.metric_pageviews_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_pageviews_key} = {expire_pg}', f'Website - expire_metrics - ')

        expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
        # tracker_log(f'EXPIRE {self.metric_unique_device_key} = {expire_ud}', f'Website - expire_metrics - ')

    def expire_record_metrics(self):
        ttl_unique_devices = execute('TTL', self.metric_unique_device_key)
        # tracker_log(f'TTL {self.metric_unique_device_key} {ttl_unique_devices}', 'Website - expire_record_metrics - ')
        if ttl_unique_devices == -1:
            expire_ud = execute('EXPIRE', self.metric_unique_device_key, 3600)
            # tracker_log(f'Expire key {self.metric_unique_device_key} = {expire_ud}', f'Website - expire_record_metrics - ')

    def is_exists(self):
        x = execute('EXISTS', self.dimension_key)
        # log(f'EXISTS {self.dimension_key} => {x}')
        return x

    def has_metrics(self):
        # check for weird timestamp
        x = execute('EXISTS', self.metric_pageviews_key)
        # log(f'EXISTS {self.metric_pageviews_key} => {x}')
        z = execute('EXISTS', self.metric_unique_device_key)
        # log(f'EXISTS {self.metric_unique_device_key} => {z}')
        # return x + z
        return x

    def update_last_visited(self):
        execute('JSON.SET', self.dimension_key, '.last_visited', self.last_visited)
        # log(f'update_last_visited: JSON.SET {self.dimension_key} .last_visited {self.last_visited}')

    def notification_of_new_website(self, stream_names):
        parsed_key = parse_key_name(self.dimension_ts_key)
        tracker_log(f'{parsed_key.get("ts")} new website {self.id}', f'Website - notification_of_new_website - ')
        execute('XADD', stream_names.get('website_pageviews'), 'MAXLEN', '8640', '*',
                'ts', parsed_key.get("ts"),
                'status', 'new',
                'ids', self.id)
        execute('XADD', stream_names.get('website_unique_devices'), 'MAXLEN', '8640', '*',
                'ts', parsed_key.get("ts"),
                'status', 'new',
                'ids', self.id)

    # Fixme: change method name
    def notification_of_active_websites(self, stream_names):
        parsed_key = parse_key_name(self.dimension_ts_key)

        # Utiliser le timestamp non arrondi
        current_ts = int(parsed_key.get("ts"))
        # real_ts = self.last_visited
        prev_unix_ts = int((datetime.fromtimestamp(int(self.last_visited) / 1000) - timedelta(minutes=1)).timestamp() * 1000)

        # Todo: create index_name with method instead of hard coding it
        # ids_raw = execute('FT.SEARCH', 'I::W:::', f'@last_visited:[{prev_unix_ts} {current_ts}]', 'RETURN', '1', 'id')
        # ids_raw = execute('FT.SEARCH', 'I::W:::', f'@last_visited:[{current_ts} 9999999999999]', 'RETURN', '1', 'id')
        ids_raw = execute('FT.SEARCH', 'I::W:::', f'@last_visited:[{self.last_visited} 9999999999999]', 'RETURN', '1', 'id')
        # tracker_log(f'FT.SEARCH I::W:: @last_visited:[{prev_unix_ts} {self.last_visited} {current_ts}] RETURN 1 id => {ids_raw}', 'Website - notification_of_active_websites - ')
        # tracker_log(f'FT.SEARCH I::W:: "@last_visited:[{prev_unix_ts} 9999999999999]" RETURN 1 id', 'Website - notification_of_active_websites - ')
        ids = []
        for d in ids_raw:
            if type(d) is list:
                ids.append(d[-1])

        # FixMe: HOT FIX
        if len(ids) > 0:
            tracker_log(f'[{prev_unix_ts} {current_ts}] active websites {len(ids)} {ids}', f'Website - notification_of_active_websites - ')
            execute('XADD', stream_names.get('website_pageviews'), 'MAXLEN', '8640', '*',
                    'ts', parsed_key.get("ts"),
                    'status', 'active',
                    'ids', json.dumps(ids))
            execute('XADD', stream_names.get('website_unique_devices'), 'MAXLEN', '8640', '*',
                    'ts', parsed_key.get("ts"),
                    'status', 'active',
                    'ids', json.dumps(ids))
        else:
            tracker_log(f'[{prev_unix_ts} {current_ts}] active websites {len(ids)} {ids}', f'Website - notification_of_active_websites - warning - ')

    def is_weird(self):
        ts = datetime.now()
        current_ts = datetime.fromtimestamp(int(self.last_visited) / 1000)
        # delta = (ts - current_ts).seconds
        delta = (ts - current_ts).seconds
        if current_ts > datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000):
        # if 55 <= delta <= 86000:
            tracker_log(f'DELTA - {ts} - {current_ts} = {(ts - current_ts).seconds}', f'Website - ')
            tracker_log(f'DELTA - {current_ts} - {ts} = {(current_ts - current_ts).seconds}', f'Website - ')
            output_log = {
                'id': self.id,
                'timezone': f'{datetime.now(timezone.utc)}',
                'now_ts': f'{ts.timestamp()} {ts}',
                'record_ts': f'{self.last_visited} {datetime.fromtimestamp(int(self.last_visited) / 1000)}',
                'delta': delta,
                'bucket_ts': f'{parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}'
            }
            tracker_log(f'WEIRDO!\n{json.dumps(output_log, indent=4, default=str)}', f'Website - ')
            return True
        else:
            return False

    def send_to_enrich(self):
        execute('XADD', 'ST:ENRICH:W:::', 'MAXLEN', '10', '*', 'key', self.dimension_key)

    def log_raw_record(self, device_id):
        # tracker_log(f'RAW!\t{self.id} {datetime.fromtimestamp(int(self.last_visited) / 1000)} {self.last_visited} at {parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}', f'Website - ')

        rounded_now_ts = int(round_time().timestamp() * 1000)
        now_ts = int(datetime.now().timestamp() * 1000)
        rounded_record_ts = int(round_time(datetime.fromtimestamp(int(self.last_visited) / 1000) if self.last_visited is not None else None).timestamp() * 1000)
        record_ts = self.last_visited

        rounded_now_dt = datetime.fromtimestamp(rounded_now_ts / 1000)
        now_dt = datetime.fromtimestamp(now_ts / 1000)
        rounded_record_dt = datetime.fromtimestamp(rounded_record_ts / 1000)
        record_dt = datetime.fromtimestamp(int(record_ts) / 1000)

        tracker_log(f'{rounded_now_ts} {now_ts} {rounded_record_ts} {record_ts} - {rounded_now_dt} {now_dt} {rounded_record_dt} {record_dt}', f'Website - ')

    def log_new_website(self, device_id):
        tracker_log(f'NEW WEBSITE!\t{self.id} {datetime.fromtimestamp(int(self.last_visited) / 1000)} {self.last_visited} at {parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}', f'Website - ')

    def log_new_weirdo(self, device_id):
        # tracker_log(f'WEIRDO!\t{self.id} {datetime.fromtimestamp(int(self.last_visited) / 1000)} {self.last_visited} at {parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}', f'Website - ')
        x = True

    def log_new_bucket(self, device_id):
        tracker_log(f'NEW BUCKET!\t{self.id} {datetime.fromtimestamp(int(self.last_visited) / 1000)} {self.last_visited} at {parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}', f'Website - ')

    def log_new_records(self, device_id):
        tracker_log(f'NEW RECORD!\t{self.id} {datetime.fromtimestamp(int(self.last_visited) / 1000)} {self.last_visited} at {parse_key_name(self.dimension_ts_key).get("ts")} {datetime.fromtimestamp(int(parse_key_name(self.dimension_ts_key).get("ts")) / 1000)}', f'Website - ')


def load_website(website, section, page, device, output_stream_names):
    website.log_raw_record(device.id)
    if website.is_exists() != 1:
        # FixMe: Register new website, section or page, but not notify merger services if ts is weird
        # website.log_new_website(device.id)
        website.create()
        website.create_metrics()
        website.incr_metrics(device.id)
        website.expire_new_metrics()
        website.notification_of_new_website(stream_names=output_stream_names)
        website.send_to_enrich()
    else:
        if website.has_metrics() < 1:
            # website.log_new_bucket(device.id)
            website.create_metrics()
            website.incr_metrics(device.id)
            website.expire_metrics()
            website.update_last_visited()
            website.notification_of_active_websites(stream_names=output_stream_names)
        else:
            # website.log_new_records(device.id)
            website.incr_metrics(device.id)
            website.expire_record_metrics()
            website.update_last_visited()


# else:
#     # FixMe: if we rerun the job, old data go to trash ...
#     if website.is_weird():
#         website.log_new_weirdo(device.id)
#     elif website.has_metrics() < 1:
#         # website.log_new_bucket(device.id)
#         website.create_metrics()
#         website.incr_metrics(device.id)
#         website.expire_metrics()
#         website.update_last_visited()
#         website.notification_of_active_websites(stream_names=output_stream_names)
#     else:
#         # website.log_new_records(device.id)
#         website.incr_metrics(device.id)
#         website.expire_record_metrics()
#         website.update_last_visited()