import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time


def main(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    filename = config_dict['filename']
    save_interval = config_dict['save_interval']

    min_difference = config_dict['t_range'][0]
    max_difference = config_dict['t_range'][1]

    min_height = 0
    max_height = 4095

    fig = plt.figure(figsize=(6, 12))
    fig.canvas.manager.set_window_title('Gamma Coincidence')
    axs = fig.subplots(2, 1)

    ax_scatter = axs[0]
    ax_scatter.set_xlabel('Height 1 [ADC]')
    ax_scatter.set_ylabel('Height 2 [ADC]')
    scatter = ax_scatter.scatter([], [], s=1)
    ax_scatter.set_xlim(min_height, max_height)
    ax_scatter.set_ylim(min_height, max_height)

    ax_delta_t = axs[1]
    ax_delta_t.set_xlabel('Time difference [Samples]')
    ax_delta_t.set_ylabel('Counts')
    ax_delta_t.set_title('The time difference distribution is shown for the visible energy range')

    bins = np.arange(min_difference, max_difference, 1)
    y_delta_t = np.histogram([], bins=bins)[0]
    x_delta_t = bins[:-1]

    line_delta_t = ax_delta_t.plot(x_delta_t, y_delta_t)[0]

    ax_delta_t.set_xlim(min_difference, max_difference)
    ax_delta_t.set_ylim(bottom=0)

    plt.ion()
    plt.show()

    xlim = ax_scatter.get_xlim()
    ylim = ax_scatter.get_ylim()

    last_update = time.time()
    while True:
        old_xlim = xlim
        old_ylim = ylim
        xlim = ax_scatter.get_xlim()
        ylim = ax_scatter.get_ylim()
        if xlim != old_xlim or ylim != old_ylim:
            last_update = 0
        if time.time() - last_update > save_interval:
            try:
                df = pd.read_csv(config_dict['directory_prefix'] + '/' + filename + '.csv')
            except FileNotFoundError:
                print("File not found")
                continue

            # ax_scatter.clear()
            scatter.set_offsets(np.array([df['height_1'], df['height_2']]).T)

            mask1 = df['height_1'] >= xlim[0]
            mask2 = df['height_1'] <= xlim[1]
            mask3 = df['height_2'] >= ylim[0]
            mask4 = df['height_2'] <= ylim[1]

            mask = mask1 & mask2 & mask3 & mask4

            y_delta_t = np.histogram(df['time_difference'][mask], bins=bins)[0]
            line_delta_t.set_ydata(y_delta_t)

            ax_delta_t.set_ylim(0, 1.1 * np.max(y_delta_t) + 0.1)

            fig.canvas.draw()
            last_update = time.time()

        fig.canvas.flush_events()
        time.sleep(0.05)
