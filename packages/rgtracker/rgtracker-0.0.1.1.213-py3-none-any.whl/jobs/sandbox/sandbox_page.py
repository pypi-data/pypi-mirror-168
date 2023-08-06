from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.pageviews import *
from redisgears import log

# desc_json_p = {"name": 'P'}
# GB("StreamReader", desc=json.dumps(desc_json_p)). \
#     filter(lambda record: record['value']['dimension'] == 'P'). \
#     foreach(lambda record: log(f'sandbox-p-{record}')). \
#     register(
#     prefix='ST:1MINUTE:P:::PG',
#     convertToStr=True,
#     collect=True,
#     onFailedPolicy='abort',
#     onFailedRetryInterval=1,
#     batch=1,
#     duration=0,
#     trimStream=False)
# log(f'Register P OK')

job = {
    'name': 'MegaStar-1to5-P',
    'version': '99.99.99',
    'input_stream_name': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.PAGE.value, '', '', Metric.PAGEVIEWS.value),
    'dimension': Dimension.PAGE.value,
    'number_of_rotated_keys': 5, # rotate 5 keys of 1 minute each
    'write_to_ts': True,
    'timeseries_name': '5MINUTES',
    'key_expire_duration_sc': 1820, # keep 6 keys -> merged key expire 30 minutes later
    'batch_size': 10000,
    'batch_interval_ms': 300000, # run the job every 5 minutes
    'output_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', Dimension.PAGE.value, '', '', Metric.PAGEVIEWS.value)
}

# unregister_old_versions(job.get('name'), job.get('version'))

tracker_log(f'Register {job.get("name")} ...')

desc_json = {
    "name": job.get('name'),
    "version": job.get('version'),
    "desc": f"{job.get('name')} - Rotate Pageviews Keys"
}
GB("StreamReader", desc=json.dumps(desc_json)). \
    aggregate([],
              lambda a, r: a + [r['value']],
              lambda a, r: a + r). \
    map(lambda records: transform(records, job.get('number_of_rotated_keys'))). \
    foreach(lambda records: tracker_log(f'{Dimension.PAGE.value}-map - ids:{len(records.get("id"))} merged:{len(records.get("merge"))} reinjected:{len(records.get("reinject"))}\n{records}')). \
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
