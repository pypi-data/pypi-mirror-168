from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.uniquedevices import *

job = {
    'name': 'P-UD-5to10',
    'version': '99.99.99',
    'input_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', Dimension.PAGE.value, '', '', Metric.UNIQUE_DEVICES.value),
    'dimension': Dimension.PAGE.value,
    'number_of_rotated_keys': 2, # rotate 2 keys of 5 minutes each
    'write_to_ts': True,
    'timeseries_name': '10MINUTES',
    # 'key_expire_duration_sc': 3620, # keep 6 keys -> merged key expire 60 minutes later
    'key_expire_duration_sc': 7240, # TEST
    'batch_size': 9999999,
    'batch_interval_ms': 600000, # run the job every 10 minutes
    'output_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', Dimension.PAGE.value, '', '', Metric.UNIQUE_DEVICES.value)
}

# Todo: unregister_old_versions job
# unregister_old_versions(job.get('name'), job.get('version'))

tracker_log(f'Register {job.get("name")} ...')

desc_json = {
    "name": job.get('name'),
    "version": job.get('version'),
    "desc": f"Rotate Page Unique Devices Keys, 5 minutes to 10 minutes buckets"
}

GB("StreamReader", desc=json.dumps(desc_json)). \
    aggregate([],
              lambda a, r: a + [r['value']],
              lambda a, r: a + r). \
    map(lambda record: transform(record, job.get('number_of_rotated_keys'), job.get('dimension'))). \
    foreach(lambda record: load(
        job.get('name'),
        record,
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
