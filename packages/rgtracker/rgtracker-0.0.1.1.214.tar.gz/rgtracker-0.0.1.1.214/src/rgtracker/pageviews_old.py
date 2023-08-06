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
    tracker_log(f'all_ids - {df["ids"].values.tolist()}', f'W-PG-1to5 - transform - ')

    aggs = {'ids': rotate_agg}
    grouped_df = df.groupby(['ts']).agg(aggs).sort_values('ts').reset_index()
    tracker_log(f'all_ts - {grouped_df["ts"].values.tolist()}', f'W-PG-1to5 - transform - ')

    def flatten(A):
        rt = []
        for i in A:
            if isinstance(i,list): rt.extend(flatten(i))
            else: rt.append(i)
        return rt

    grouped_df['ids'] = grouped_df['ids'].apply(lambda x: flatten(x))

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
            tracker_log(f'chunk_{x}_ts - {df_sliced["ts"].values.tolist()}', f'X-PG-1to5 - transform - ')

            ids = df_sliced['ids'].values.tolist()
            ids = [list(id.split(' ')) if type(id) is str else id for id in ids]
            # unique_ids = {x for l in ids for x in l}

            execute('SET', 'mykey', f'{ids}')
            tracker_log(f'chunk_{x}_ids - {ids}', f'X-PG-1to5 - transform - ')

            unique_ids = list(set([item for sublist in ids for item in sublist]))
            for unique_id in unique_ids:
                results.get('ids').append(unique_id)
            tracker_log(f'chunk_{x}_unique_ids - {unique_ids}', f'X-PG-1to5 - transform - ')

            results.get('merge').append({
                'name': create_key_name(
                    Type.CMS.value,
                    '',
                    dimension,
                    '',
                    get_ts_df(df_sliced["ts"].iloc[0], df_sliced["ts"]),
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
    tracker_log(f'final_ids - {results.get("ids")}', f'X-PG-1to5 - transform - ')
    return results


def load(job_name, records, dimension, write_to_ts, timeseries_name, key_expire_duration_sc, reinject_stream_name,
         output_stream_name):
    def get_ts(ts):
        if len(ts.split('_')) > 1:
            return ts.split("_")[-1]
        else:
            return ts

    capped_stream = get_maxlen_capped_stream(timeseries_name, dimension)

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
                    index_name = create_key_name(
                        type=Type.INDEX.value,
                        name='',
                        dimension=dimension,
                        record_id='',
                        ts='',
                        metric='')
                    timeseries_key_name = create_key_name(
                        type=Type.TIMESERIES.value,
                        name=timeseries_name,
                        dimension=dimension,
                        record_id=id,
                        metric=Metric.PAGEVIEWS.value)

                    if dimension == Dimension.WEBSITE.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '3', 'name', 'AS',
                                               'website_name')
                        tracker_log(f'records_infos {record_infos}', f'{job_name} - ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get('ts')), pageviews,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                'website_id', id, *record_infos[-1])
                        tracker_log(
                            f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                            f'{job_name} - ')
                    elif dimension == Dimension.SECTION.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                                               'name', 'AS', 'section_name', 'website_id', 'website_name')
                        tracker_log(f'records_infos {record_infos}', f'{job_name} - ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get("ts")), pageviews,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                'section_id', id, *record_infos[-1])
                        tracker_log(
                            f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                            f'{job_name} - ')
                    elif dimension == Dimension.PAGE.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                                               'website_id', 'website_name', 'section_id', 'section_name', 'article_id')
                        tracker_log(f'records_infos {record_infos}', f'{job_name} - ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key_name.get("ts")), pageviews,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.PAGEVIEWS.value,
                                'page_id', id, *record_infos[-1])
                        tracker_log(
                            f'Write {pageviews} pageviews to {timeseries_key_name} at {get_ts(parsed_key_name.get("ts"))}',
                            f'{job_name} - ')

            execute('XADD', output_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                    'ts', parsed_key_name.get('ts'),
                    'ids', json.dumps(records.get('ids')))
            # tracker_log(f'Write to OutputStream {id}->{output_stream_name}', f'{job_name} ')

            execute('EXPIRE', cms_merge.get('name'), key_expire_duration_sc)

    return records
