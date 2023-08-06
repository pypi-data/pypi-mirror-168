from rgtracker.common import *
from rgtracker.record import *
from rgtracker.tracker import *
from rgtracker.website import *
from rgtracker.section import *
from rgtracker.page import *
from rgtracker.device import *


def transform(record):
    serialized_object = Record(
        redis_event=record.get('event'),
        redis_key=record.get('key'),
        redis_type=record.get('type'),
        redis_value=record.get('value')
    ).serialize_record()

    if type(serialized_object) is Tracker:
        return serialized_object.serialize_tracker()
    else:
        raise Exception(f'Record is not a Tracker object')


def load(tracker):
    website: Website = tracker.get('website')
    section = tracker.get('section')
    page = tracker.get('page')
    device = tracker.get('device')

    output_stream_names = {
        'default': create_key_name(Type.STREAM.value, '1MINUTE'),
        'pageviews': create_key_name(Type.STREAM.value, '1MINUTE', '', '', '', Metric.PAGEVIEWS.value),
        'unique_devices': create_key_name(Type.STREAM.value, '1MINUTE', '', '', '', Metric.UNIQUE_DEVICES.value),
        'website_pageviews': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.WEBSITE.value, '', '', Metric.PAGEVIEWS.value),
        'section_pageviews': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.SECTION.value, '', '', Metric.PAGEVIEWS.value),
        'page_pageviews': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.PAGE.value, '', '', Metric.PAGEVIEWS.value),
        'website_unique_devices': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.WEBSITE.value, '', '', Metric.UNIQUE_DEVICES.value),
        'section_unique_devices': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.SECTION.value, '', '', Metric.UNIQUE_DEVICES.value),
        'page_unique_devices': create_key_name(Type.STREAM.value, '1MINUTE', Dimension.PAGE.value, '', '', Metric.UNIQUE_DEVICES.value),
    }
    if not is_weird(website.last_visited, website.last_visited_rounded):
        load_website(website, section, page, device, output_stream_names)
        load_section(website, section, page, device, output_stream_names)
        load_page(website, section, page, device, output_stream_names)

    return tracker


desc_json = {
    "name": 'BigBang',
    "version": '99.99.99',
    "desc": f"BigBang - Backbone Job"
}
# unregister_old_versions(desc_json.get('name'), desc_json.get('version'))
GB("StreamReader", desc=json.dumps(desc_json)). \
    map(transform). \
    foreach(load). \
    register(
    prefix='ST:TRACKER::::',
    convertToStr=True,
    collect=True,
    onFailedPolicy='abort',
    onFailedRetryInterval=1,
    batch=1,
    duration=0,
    trimStream=False)

# run('ST:TRACKER::::', trimStream=False)
# register(
# prefix='ST:TRACKER::::',
# convertToStr=True,
# collect=True,
# onFailedPolicy='abort',
# onFailedRetryInterval=1,
# batch=1,
# duration=0,
# trimStream=False)
