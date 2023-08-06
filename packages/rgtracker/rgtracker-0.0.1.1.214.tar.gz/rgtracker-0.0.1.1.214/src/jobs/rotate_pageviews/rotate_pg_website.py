from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.pageviews import *

job = {
    'name': 'W-PG-1to5',
    'version': '99.99.99',
    'input_stream_name': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.WEBSITE.value, '', '', Metric.PAGEVIEWS.value),
    'dimension': Dimension.WEBSITE.value,
    'number_of_rotated_keys': 5, # rotate 5 keys of 1 minute each
    'write_to_ts': True,
    'timeseries_name': '5MINUTES',
    # 'key_expire_duration_sc': 1820, # keep 6 keys -> merged key expire 30 minutes later
    'key_expire_duration_sc': 3600, # TEST
    'batch_size': 9999999,
    'batch_interval_ms': 300000, # run the job every 5 minutes
    'output_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', Dimension.WEBSITE.value, '', '', Metric.PAGEVIEWS.value)
}

# Todo: unregister_old_versions job
# unregister_old_versions(job.get('name'), job.get('version'))

tracker_log(f'Register {job.get("name")} ...')

desc_json = {
    "name": job.get('name'),
    "version": job.get('version'),
    "desc": f"Rotate Website Pageviews Keys, 1 minute to 5 minutes buckets"
}

GB("StreamReader", desc=json.dumps(desc_json)). \
    aggregate([],
              lambda a, r: a + [r['value']],
              lambda a, r: a + r). \
    map(lambda records: transform(records, job.get('number_of_rotated_keys'), job.get('dimension'))). \
    foreach(lambda records: load(
        job.get('name'),
        records,
        job.get('dimension'),
        job.get('write_to_ts'),
        job.get('timeseries_name'),
        job.get('key_expire_duration_sc'),
        job.get('input_stream_name'),
        job.get('output_stream_name')
    )). \
    foreach(lambda records: tracker_log(f'ids:{len(records.get("ids"))} merged:{len(records.get("merge"))} reinjected:{len(records.get("reinject"))} - {records}', f'{job.get("name")} - ')). \
    register(
        prefix=job.get('input_stream_name'),
        convertToStr=True,
        collect=True,
        onFailedPolicy='abort',
        onFailedRetryInterval=1,
        batch=job.get('batch_size'),
        duration=job.get('batch_interval_ms'),
        trimStream=False)

tracker_log(f'Register {job.get("name")} OK')
