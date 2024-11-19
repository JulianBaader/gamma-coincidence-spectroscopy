import numpy as np
import scipy.signal as signal


def pha(osc_data, config):
    prominence = config['prominence']
    width = config['width']
    gradient_min = config['gradient_min']

    peaks, peak_properties = signal.find_peaks(osc_data, prominence=prominence, width=width)

    heights = []
    times = []
    for peak, left_ip in zip(peaks, peak_properties['left_ips']):
        start = find_pulse_start(np.gradient(osc_data), gradient_min, int(left_ip))
        if start < 0:
            continue
        heights.append(osc_data[peak] - osc_data[start])
        times.append(peak)
    return heights, times


def find_pulse_start(gradient, min_value, start_index):
    if start_index < 0 or start_index > len(gradient):
        raise ValueError("peak_index is out of the array bounds")

    valid_indices = np.where(gradient[:start_index] <= min_value)[0]
    if len(valid_indices) == 0:
        return -1
    return int(valid_indices[-1])
