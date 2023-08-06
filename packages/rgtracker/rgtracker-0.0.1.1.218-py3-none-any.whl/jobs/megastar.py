from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.common import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *
from rgtracker.pageviews import *
from redisgears import log


# Pageviews Rotation Jobs - CMS
pageviews_rotate_jobs = [
    # Run the job every 5 minutes to rotate 5 key of 1 minute each.
    # Expire new merged key after 30 minutes (keep 6 merged keys of 5 minutes each)
    {
        'name': 'MegaStar-1to5-W',
        'version': '99.99.99',
        'input_stream_name': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.WEBSITE.value, '', '', Metric.PAGEVIEWS.value),
        'dimension': Dimension.WEBSITE.value,
        'number_of_rotated_keys': 5, # rotate 5 keys of 1 minute each
        'write_to_ts': True,
        'timeseries_name': '5MINUTES',
        'key_expire_duration_sc': 1820, # keep 6 keys -> merged key expire 30 minutes later
        'batch_size': 10000,
        'batch_interval_ms': 300000, # run the job every 5 minutes
        'output_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', Dimension.WEBSITE.value, '', '', Metric.PAGEVIEWS.value)
    },
    {
        'name': 'MegaStar-1to5-S',
        'version': '99.99.99',
        'input_stream_name': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.SECTION.value, '', '', Metric.PAGEVIEWS.value),
        'dimension': Dimension.SECTION.value,
        'number_of_rotated_keys': 5, # rotate 5 keys of 1 minute each
        'write_to_ts': True,
        'timeseries_name': '5MINUTES',
        'key_expire_duration_sc': 1820, # keep 6 keys -> merged key expire 30 minutes later
        'batch_size': 10000,
        'batch_interval_ms': 300000, # run the job every 5 minutes
        'output_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', Dimension.SECTION.value, '', '', Metric.PAGEVIEWS.value)
    },
    {
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
    },


    # # Run the job every 10 minutes to rotate 2 key of 5 minutes each.
    # # Expire new merged key after 60 minutes (keep 6 merged keys of 10 minutes each)
    # {
    #     'name': 'MegaStar-5to10-W',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.WEBSITE.value,
    #     'number_of_rotated_keys': 2, # rotate 2 keys of 5 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 3620, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 600000, # run the job every 10 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value)
    # },
    # {
    #     'name': 'MegaStar-5to10-S',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.SECTION.value,
    #     'number_of_rotated_keys': 2, # rotate 2 keys of 5 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 3620, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 600000, # run the job every 10 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value)
    # },
    # {
    #     'name': 'MegaStar-5to10-P',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '5MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.PAGE.value,
    #     'number_of_rotated_keys': 2, # rotate 2 keys of 5 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 3620, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 600000, # run the job every 10 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value)
    # },
    # # Run the job every 60 minutes to rotate 6 key of 10 minutes each.
    # # Expire new merged key after 24 hours (keep 24 merged keys of 1 hour each)
    # {
    #     'name': 'MegaStar-10to60-W',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.WEBSITE.value,
    #     'number_of_rotated_keys': 6, # rotate 6 keys of 10 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 86420, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 3600000, # run the job every 60 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '1HOUR', '', '', '', Metric.PAGEVIEWS.value)
    # },
    # {
    #     'name': 'MegaStar-10to60-S',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.SECTION.value,
    #     'number_of_rotated_keys': 6, # rotate 6 keys of 10 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 86420, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 3600000, # run the job every 60 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '1HOUR', '', '', '', Metric.PAGEVIEWS.value)
    # },
    # {
    #     'name': 'MegaStar-10to60-P',
    #     'version': '99.99.99',
    #     'input_stream_name': create_key_name(Type.STREAM.value, '10MINUTES', '', '', '', Metric.PAGEVIEWS.value),
    #     'dimension': Dimension.PAGE.value,
    #     'number_of_rotated_keys': 6, # rotate 6 keys of 10 minutes each
    #     'write_to_ts': False,
    #     'timeseries_name': '',
    #     'key_expire_duration_sc': 86420, # keep 6 keys -> merged key expire 60 minutes later
    #     'batch_size': 10000,
    #     'batch_interval_ms': 3600000, # run the job every 60 minutes
    #     'output_stream_name': create_key_name(Type.STREAM.value, '1HOUR', '', '', '', Metric.PAGEVIEWS.value)
    # },
]
for job in pageviews_rotate_jobs:
    # unregister_old_versions(job.get('name'), job.get('version'))
    desc_json = {
        "name": job.get('name'),
        "version": job.get('version'),
        "desc": f"{job.get('name')} - Rotate Pageviews Keys"
    }
    tracker_log(f'Register {job.get("name")} ...')
    GB("StreamReader", desc=json.dumps(desc_json)). \
        foreach(lambda records: tracker_log(f'start - {len(records)}->{records}')). \
        aggregate([],
                  lambda a, r: a + [r['value']],
                  lambda a, r: a + r). \
        map(lambda records: transform(records, job.get('number_of_rotated_keys'))). \
        foreach(lambda records: tracker_log(f'map - {records}')). \
        foreach(lambda records: load(
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
