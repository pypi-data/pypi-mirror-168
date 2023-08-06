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
    # tracker_log(f'all_ids - {df["ids"].values.tolist()}', f'W-UD-1to5 - transform - ')

    aggs = {'ids': rotate_agg}
    grouped_df = df.groupby(['ts']).agg(aggs).sort_values('ts').reset_index()
    # tracker_log(f'all_ts - {grouped_df["ts"].values.tolist()}', f'W-UD-1to5 - transform - ')

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
            # tracker_log(f'chunk_{x}_ts - {df_sliced["ts"].values.tolist()}', f'W-UD-1to5 - transform - ')
            # tracker_log(f'chunk_{x}_ids - {df_sliced["ids"].values.tolist()}', f'W-UD-1to5 - transform - ')

            # ids = [id for id in df_sliced['ids']]
            # unique_ids = {x for l in ids for x in l}
            # for unique_ids in unique_ids:
            #     results.get('ids').append(unique_ids)

            ids = df_sliced['ids'].values.tolist()
            ids = [list(id.split(' ')) if type(id) is str else id for id in ids]
            # unique_ids = {x for l in ids for x in l}
            unique_ids = list(set([item for sublist in ids for item in sublist]))
            for unique_id in unique_ids:
                results.get('ids').append(unique_id)

            # tracker_log(f'chunk_{x}_unique_ids - {unique_ids}', f'W-UD-1to5 - transform - ')

            results.get('merge').append({
                'name': create_key_name(
                    Type.HLL.value,
                    '',
                    dimension,
                    '',
                    get_ts_df(df_sliced["ts"].iloc[0], df_sliced["ts"]),
                    Metric.UNIQUE_DEVICES.value
                ),
                'keys': [create_key_name(Type.HLL.value, '', dimension, '', ts, Metric.UNIQUE_DEVICES.value) for ts in
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
    # tracker_log(f'final_ids - {results.get("ids")}', f'W-UD-1to5 - transform - ')
    return results


def load(job_name, records, dimension, write_to_ts, timeseries_name, key_expire_duration_sc, reinject_stream_name,
         output_stream_name):
    def get_ts(ts):
        if len(ts.split('_')) > 1:
            return ts.split("_")[-1]
        else:
            return ts

    # tracker_log(
    #     f'ids:{len(records.get("ids"))} merged:{len(records.get("merge"))} reinjected:{len(records.get("reinject"))}\n{records}',
    #     f'{job_name} - load - ')

    capped_stream = get_maxlen_capped_stream(timeseries_name, dimension)

    index_name = create_key_name(
        type=Type.INDEX.value,
        name='',
        dimension=dimension,
        record_id='',
        ts='',
        metric='')

    for hll_reinject in records.get('reinject'):
        execute('XADD', reinject_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                'ts', hll_reinject.get('ts'),
                'status', 'reinject',
                'ids', json.dumps(hll_reinject.get('ids')))
        # tracker_log(
        #     f'XADD {reinject_stream_name} * ts {hll_reinject.get("ts")} status reinject ids {json.dumps(hll_reinject.get("ids"))}',
        #     f'{job_name} - load - ')

    for hll_merge in records.get("merge"):
        if execute('EXISTS', hll_merge.get('name')) != 1:

            parsed_key = parse_key_name(hll_merge.get('name'))
            for id in records.get('ids'):
                k = create_key_name(Type.HLL.value, '', Dimension.WEBSITE.value, id, parsed_key.get('ts'),
                                    Metric.UNIQUE_DEVICES.value)
                keys = [create_key_name(Type.HLL.value, '', Dimension.WEBSITE.value, id, parse_key_name(k).get('ts'),
                                        Metric.UNIQUE_DEVICES.value) for k in hll_merge.get('keys')]
                execute('PFMERGE', k, *keys)
                # tracker_log(f'PFMERGE {k} {keys}', f'{job_name} - load - ')

                if write_to_ts:
                    unique_devices = execute('PFCOUNT', *keys)
                    # tracker_log(f'PFCOUNT {keys}', f'{job_name} - load - ')

                    timeseries_key_name = create_key_name(
                        type=Type.TIMESERIES.value,
                        name=timeseries_name,
                        dimension=dimension,
                        record_id=id,
                        metric=Metric.UNIQUE_DEVICES.value)

                    if dimension == Dimension.WEBSITE.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}',
                                               'RETURN', '3', 'name', 'AS', 'website_name')
                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get('ts')), unique_devices,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                'website_id', id, *record_infos[-1])
                        # tracker_log(
                        #     f'Write {unique_devices} devices to {timeseries_key_name} at {get_ts(parsed_key.get("ts"))}',
                        #     f'{job_name} - load - ')
                    elif dimension == Dimension.SECTION.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                                               'name', 'AS', 'section_name', 'website_id', 'website_name')
                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get("ts")), unique_devices,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                'section_id', id, *record_infos[-1])
                        # tracker_log(f'Write to Timeseries {id}->{timeseries_key_name}', f'{job_name} ')
                    elif dimension == Dimension.PAGE.value:
                        record_infos = execute('FT.SEARCH', index_name, f'@id:{{{id}}}', 'RETURN', '5',
                                               'website_id', 'website_name', 'section_id', 'section_name', 'article_id')
                        # tracker_log(f'Get {dimension} infos - {record_infos}', f'{job_name} ')
                        execute('TS.ADD', timeseries_key_name, get_ts(parsed_key.get("ts")), unique_devices,
                                'ON_DUPLICATE', 'LAST',
                                'LABELS', 'ts_name', timeseries_name,
                                'dimension', dimension, Dimension.METRIC.value, Metric.UNIQUE_DEVICES.value,
                                'page_id', id, *record_infos[-1])
                        # tracker_log(f'Write to Timeseries {id}->{timeseries_key_name}', f'{job_name} ')

            execute('XADD', output_stream_name, 'MAXLEN', f'{capped_stream}', '*',
                    'ts', parsed_key.get('ts'),
                    'ids', json.dumps(records.get('ids')))
            # tracker_log(f'Write to OutputStream {id}->{output_stream_name}', f'{job_name} ')
            # tracker_log(
            #     f'XADD {output_stream_name} * ts {parsed_key.get("ts")} ids {json.dumps(records.get("ids"))}',
            #     f'{job_name} - load - ')

            execute('EXPIRE', hll_merge.get('name'), key_expire_duration_sc)

    return records
