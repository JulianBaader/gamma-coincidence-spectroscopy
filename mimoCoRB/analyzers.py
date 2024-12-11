from mimocorb.buffer_control import rbProcess
from modules.pha import pha
import numpy as np


def coincidence(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    peak_config1 = config_dict['peak_config1']
    peak_config2 = config_dict['peak_config2']

    entry_out = np.zeros((1,), dtype=sink_list[0]['dtype'])

    channels = [dtype[0] for dtype in source_list[0]['dtype']]
    ch1 = channels[0]
    ch2 = channels[1]

    def ufunc(data):
        if np.max(data[ch1]) >= 4095 or np.max(data[ch2]) >= 4095:
            return None
        heights_1, times_1 = pha(data[ch1], peak_config1)
        heights_2, times_2 = pha(data[ch2], peak_config2)

        if len(heights_1) != 1 or len(heights_2) != 1:
            return None

        entry_out['height_1'] = heights_1[0]
        entry_out['height_2'] = heights_2[0]
        entry_out['time_difference'] = times_2[0] - times_1[0]
        return [entry_out]

    process = rbProcess(source_list=source_list, sink_list=sink_list, config_dict=config_dict, ufunc=ufunc, **rb_info)
    process()


def single(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    source_dtypes = source_list[0]['dtype']
    ch1 = source_dtypes[0][0]
    ch2 = source_dtypes[1][0]
    if ch1 == 'trigger_channel':
        peak_config = config_dict['peak_config1']
    elif ch2 == 'trigger_channel':
        peak_config = config_dict['peak_config2']
    else:
        raise ValueError("ERROR! No trigger channel found")

    entry_out = np.zeros((1,), dtype=sink_list[0]['dtype'])

    def ufunc(data):
        if np.max(data['trigger_channel']) >= 4095:
            return None
        heights, times = pha(data['trigger_channel'], peak_config)
        out = []
        for height in heights:
            entry_out['height'] = height
            out.append(entry_out.copy())
        return [out]

    process = rbProcess(source_list=source_list, sink_list=sink_list, config_dict=config_dict, ufunc=ufunc, **rb_info)
    process()
