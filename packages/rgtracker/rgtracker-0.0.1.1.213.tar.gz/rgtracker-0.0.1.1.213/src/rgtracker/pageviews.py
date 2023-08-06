from rgtracker.common import *
import math
import pandas as pd
from redisgears import executeCommand as execute
from redisgears import log


def extract(record, dimension):
    return record['value']['dimension'] == dimension


def transform(records, number_of_rotated_keys, dimension):
    df = pd.DataFrame(records)
    df['ids'] = df['ids'].apply(lambda x: json.loads(x) if x.startswith('[') else x)
    # tracker_log(f'all_ids - {df["ids"].values.tolist()}', f'W-PG-1to5 - transform - ')

    def flatten_list(A):
        rt = []
        for i in A:
            if isinstance(i, list):
                rt.extend(flatten_list(i))
            else:
                rt.append(i)
        return rt

    def unique_item(_list):
        return list(set(_list))

    grouped_df = df.groupby('ts').agg(lambda ids: unique_item(flatten_list(list(ids)))).sort_values('ts').reset_index()
    # tracker_log(f'all_ts - {grouped_df["ts"].values.tolist()}', f'W-PG-1to5 - transform - ')

    expected_rows = number_of_rotated_keys
    chunks = math.floor(len(grouped_df['ts']) / expected_rows + 1)
    i = 0
    j = expected_rows

    results = {
        'ids': [],
        'merge': [],
        'reinject': []
    }
    for x in range(chunks):
        df_sliced = grouped_df[i:j]
        if df_sliced.shape[0] >= number_of_rotated_keys:

            # Add only ids from 'complete' chunk
            ts = df_sliced["ts"].values.tolist()
            # tracker_log(f'chunk_{x}_ts - {ts}', f'X-PG-1to5 - transform - ')

            ids = df_sliced.apply(lambda ids: unique_item(flatten_list(ids)))['ids']
            for unique_id in ids:
                results.get('ids').append(unique_id)
            # tracker_log(f'chunk_{x}_ids - {ids}', f'X-PG-1to5 - transform - ')

            results.get('merge').append({
                'name': create_key_name(
                    Type.CMS.value,
                    '',
                    dimension,
                    '',
                    get_ts_df(ts[0], df_sliced["ts"]),
                    Metric.PAGEVIEWS.value
                ),
                'keys': [create_key_name(Type.CMS.value, '', dimension, '', ts, Metric.PAGEVIEWS.value) for ts in
                         df_sliced['ts']]
            })
        else:
            [results.get('reinject').append({
                'ts': row[1],
                'ids': row[0]
            }) for row in zip(df_sliced['ids'], df_sliced['ts'])]

        i += expected_rows
        j += expected_rows

    # Deduplicate ids
    results.update({'ids': list(set(results.get('ids')))})
    # tracker_log(f'final_ids - {results.get("ids")}', f'X-PG-1to5 - transform - ')
    return results


def load(job_name, records, dimension, write_to_ts, timeseries_name, key_expire_duration_sc, reinject_stream_name,
         output_stream_name):
    def get_ts(ts):
        if len(ts.split('_')) > 1:
            return ts.split("_")[-1]
        else:
            return ts

    capped_stream = get_maxlen_capped_stream(timeseries_name, dimension)

    index_name = create_key_name(
        type=Type.INDEX.value,
        name='',
        dimension=dimension,
        record_id='',
        ts='',
        metric='')

    for cms_reinject in records.get('reinject'):
        execute('XADD', reinject_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                'ts', cms_reinject.get('ts'),
                'status', 'reinject',
                'ids', json.dumps(cms_reinject.get('ids')))
        # tracker_log(f'Reinject {cms_reinject}', f'{job_name} - ')

    for cms_merge in records.get("merge"):
        if execute('EXISTS', cms_merge.get('name')) != 1:
            try:
                execute('CMS.INITBYDIM', cms_merge.get('name'), 2000, 5)
            except Exception as e:
                tracker_log(f'Error during CMS key init: {e} {cms_merge.get("name")}', f'{job_name} ', 'warning')

            try:
                execute('CMS.MERGE', cms_merge.get('name'), len(cms_merge.get('keys')), *cms_merge.get('keys'))
            except Exception as e:
                tracker_log(
                    f'Error during CMS merging key: {e} {cms_merge.get("name")} {len(cms_merge.get("keys"))} {cms_merge.get("keys")}',
                    f'{job_name} ', 'warning')
                # FixMe: one of merged keys is expire or missing, create strategy to not crash app and standardize data

            parsed_key_name = parse_key_name(cms_merge.get('name'))

            if write_to_ts:
                for id in records.get('ids'):
                    pageviews = execute('CMS.QUERY', cms_merge.get('name'), id)[0]

                    timeseries_key_name = create_key_name(
                        type=Type.TIMESERIES.value,
                        name=timeseries_name,
                        dimension=dimension,
                        record_id=id,
                        metric=Metric.PAGEVIEWS.value)

                    if dimension == Dimension.WEBSITE.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '3', 'name', 'AS',
                        #                        'website_name')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.WEBSITE.value, id, '', '')
                        # JSON.GET J::S:46535707faf945b66a11ddf37f8017b2c29bfa3e:: website.id website.name name
                        record_infos = execute('JSON.GET', json_key, 'name')
                        record_infos = json.loads(record_infos)

                        # tracker_log(f'records_infos {json_key} {record_infos}', f'{job_name} - ')
                        # FixMe: HOT FIX -> no records info found
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get('ts')), pageviews,
                                        'ON_DUPLICATE', 'LAST',
                                        'LABELS', 'ts_name', timeseries_name,
                                        'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                        'website_id', id, 'website_name', record_infos)
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - warning - ')
                    elif dimension == Dimension.SECTION.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                        #                        'name', 'AS', 'section_name', 'website_id', 'website_name')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.SECTION.value, id, '', '')
                        # JSON.GET J::S:46535707faf945b66a11ddf37f8017b2c29bfa3e:: website.id website.name name
                        record_infos = execute('JSON.GET', json_key, 'website.id', 'website.name', 'name')
                        record_infos = json.loads(record_infos)

                        # tracker_log(f'records_infos {json_key} {record_infos}', f'{job_name} - ')
                        # FixMe: HOT FIX -> no records info found
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get("ts")), pageviews,
                                    'ON_DUPLICATE', 'LAST',
                                    'LABELS', 'ts_name', timeseries_name,
                                    'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                    'section_id', id, 'section_name', record_infos.get('name'),
                                    'website_id', record_infos.get('website.id'), 'website_name', record_infos.get('website.name'))
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - warning - ')
                    elif dimension == Dimension.PAGE.value:
                        # record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                        #                        'website_id', 'website_name', 'section_id', 'section_name', 'article_id')
                        json_key = create_key_name(Type.JSON.value, '', Dimension.PAGE.value, id, '', '')
                        # JSON.GET J::P:620070307ea50a61c177f8c3dbb063b708dad92c:: website.id website.name section.id section.name article_id
                        record_infos = execute('JSON.GET', json_key, 'website.id', 'website.name', 'section.id', 'section.name', 'article_id')
                        record_infos = json.loads(record_infos)

                        # tracker_log(f'records_infos {json_key} {record_infos}', f'{job_name} - ')
                        # FixMe: HOT FIX -> no records info found
                        if bool(record_infos):
                            execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get("ts")), pageviews,
                                    'ON_DUPLICATE', 'LAST',
                                    'LABELS', 'ts_name', timeseries_name,
                                    'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                    'page_id', id,
                                    'website_id', record_infos.get('website.id'), 'website_name', record_infos.get('website.name'),
                                    'section_id', record_infos.get('section.id'), 'section_name', record_infos.get('section.name'),
                                    'article_id', record_infos.get('article_id'))
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - ')
                        else:
                            tracker_log(
                                f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                                f'{job_name} - warning - ')

            execute('XADD', output_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                    'ts', parsed_key_name.get('ts'),
                    'status', 'merged',
                    'ids', json.dumps(records.get('ids')))
            # tracker_log(f'Write key {cms_merge.get("name")} with ids {json.dumps(records.get("ids"))} to {output_stream_name} ', f'{job_name} - ')

            execute('EXPIRE', cms_merge.get('name'), key_expire_duration_sc)

    return records
