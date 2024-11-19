import matplotlib.pyplot as plt
import numpy as np
import time


def vis_spectrum(source_list=None, sink_list=None, observe_list=None, config_dict=None, **rb_info):
    """config_dict must be shared with the corresponding exporter"""
    bins = np.linspace(config_dict['bins'][0], config_dict['bins'][1], config_dict['bins'][2])
    save_interval = config_dict['save_interval']
    filename = config_dict['filename']
    channels = config_dict['channels']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ys = {ch: np.zeros(len(bins) - 1) for ch in channels}
    stairs = {ch: ax.stairs(ys[ch], edges=bins, label=ch) for ch in channels}

    # create the legend and make it interactive
    legend = ax.legend(title='Click to hide/show')
    legend_texts = legend.get_texts()
    legend_lines = legend.get_lines()
    legend_artists = legend_texts + legend_lines

    for a in legend_artists:
        a.set_picker(5)

    artist_to_channel = {artist: ch for artist, ch in zip(legend_artists, 2 * channels)}
    channel_to_texts = {artist_to_channel[text]: text for text in legend_texts}
    channel_to_lines = {artist_to_channel[patch]: patch for patch in legend_lines}

    def on_pick(event):
        artist = event.artist
        if artist not in legend_artists:
            return
        ch = artist_to_channel[artist]
        # Toggle visibility of plot
        visible = not stairs[ch].get_visible()
        stairs[ch].set_visible(visible)
        # Toggle visibility of legend
        channel_to_texts[ch].set_alpha(1.0 if visible else 0.2)
        channel_to_lines[ch].set_alpha(1.0 if visible else 0.2)
        # Update the plot
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    legend.set_draggable(True)

    # make the y axis clickable to toggle between lin and log
    ax.yaxis.label.set_picker(True)

    def update_yaxis(current_scale):
        ax.set_ylabel('Log (click to toggle)' if current_scale == 'linear' else 'Linear (click to toggle)')
        ax.set_yscale('log' if current_scale == 'linear' else 'linear')
        ax.relim()
        ax.autoscale_view()
        ax.figure.canvas.draw()
        fig.tight_layout()

    update_yaxis('log')  # toggles to linear

    def toggle_scale(event):
        if event.artist == ax.yaxis.label:
            current_scale = ax.get_yscale()
            update_yaxis(current_scale)

    fig.canvas.mpl_connect('pick_event', toggle_scale)

    plt.ion()
    plt.show()

    last_update = time.time()
    while True:
        if time.time() - last_update > save_interval:
            for ch in channels:
                try:
                    y = np.load(config_dict['directory_prefix'] + '/' + filename + '_' + ch + '.npy')
                except FileNotFoundError:
                    continue
                # Update the plot
                stairs[ch].set_data(values=y)
            last_update = time.time()
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()

        fig.canvas.flush_events()
        plt.pause(0.05)  # Updates at 20 FPS
