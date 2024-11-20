from mimocorb.buffer_control import rbExport, rb_toParquetfile

import pandas as pd
import numpy as np
from numpy.lib import recfunctions as rfn
import time


def drain(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    exporter = rbExport(source_list=source_list, config_dict=config_dict, **rb_info)
    generator = exporter()

    while True:
        ret = next(generator)
        if ret is None:
            break


def save_csv(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    filename = config_dict['filename']
    save_interval = config_dict['save_interval']

    exporter = rbExport(source_list=source_list, config_dict=config_dict, **rb_info)

    if exporter.source.values_per_slot != 1:
        raise ValueError('CSV exporter only supports one value per slot')

    generator = exporter()

    header = []
    dtypes = []
    for dtype_name, dtype_type in exporter.source.metadata_dtype:
        header.append(dtype_name)
        dtypes.append(dtype_type)

    for dtype_name, dtype_type in exporter.source.dtype:
        header.append(dtype_name)
        dtypes.append(dtype_type)

    # create empty dataframe
    df = pd.DataFrame(columns=header)
    df.to_csv(config_dict['directory_prefix'] + '/' + filename + '.csv', index=False)
    count = 0

    last_save = time.time()
    while True:
        ret = next(generator)
        if ret is None:
            break
        count += 1
        data, metadata = ret
        unstructured_data = rfn.structured_to_unstructured(data[0])
        new_line = np.append(metadata, unstructured_data)
        df.loc[count] = new_line

        if time.time() - last_save > save_interval:
            df.to_csv(config_dict['directory_prefix'] + '/' + filename + '.csv', index=False, mode='a', header=False)
            last_save = time.time()
            df = pd.DataFrame(columns=header)
            count = 0


def save_spectrum(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    bins = np.linspace(config_dict['bins'][0], config_dict['bins'][1], config_dict['bins'][2])
    save_interval = config_dict['save_interval']
    filename = config_dict['filename']
    channels = config_dict['channels']

    exporter = rbExport(source_list=source_list, config_dict=config_dict, **rb_info)
    if exporter.source.values_per_slot != 1:
        raise ValueError('Spectrum exporter only supports one value per slot')
    generator = exporter()

    mimo_channels = [dtype[0] for dtype in exporter.source.dtype]
    for ch in channels:
        if ch not in mimo_channels:
            raise ValueError('Channel {} not found in source'.format(ch))

    hists = {ch: np.zeros(len(bins) - 1) for ch in channels}

    last_save = time.time()
    while True:
        ret = next(generator)
        if ret is None:
            break
        data, metadata = ret
        for ch in channels:
            hists[ch] += np.histogram(data[ch], bins=bins)[0]

        if time.time() - last_save > save_interval:
            for ch in channels:
                np.save(config_dict['directory_prefix'] + '/' + filename + '_' + ch + '.npy', hists[ch])
            last_save = time.time()

    for ch in channels:
        np.save(config_dict['directory_prefix'] + '/' + filename + '_' + ch + '.npy', hists[ch])


def save_parquet(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    sv = rb_toParquetfile(source_list=source_list, config_dict=config_dict, **rb_info)
    sv()
