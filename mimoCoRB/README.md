# Requirements
[mimocorb 1.0.2rc2](https://pypi.org/project/mimocorb/)


# redpitaya.py
## class rpControll
This class is designed to controll and communicate with the RedPitaya running the DAQ server.
* ADC:
    * Sample Rate
    * Input Negators
* Oscilloscope/Trigger:
    * Source
    * Slope
    * Mode
    * Total samples
    * Pre trigger samples
* Generator:
    * Fall time
    * Rise time
    * Average Rate
    * Distribution
    * Spectrum
    * Starting/Stopping
* MCPHA:
    * Not implemented
* PHA:
    * Not implemented


A testing setup is included which generates pulses on OUT1 and measures them on IN1.

## mimoCoRB-function redpitaya_to_mimoCoRB
Creates an instance of the rpControll class and imports oscilloscope data into the first RingBuffer.

# visualizers.py
A oscilloscope and spectrum visualizer.

# gamma_coincidence_live_visualisation.py
Live visualistaion for the coincidence measurements. Consists of a scatter plot showing the pulse heights of both channels and a histogram of the time differences. Zooming in the top plot limits the data set for the bottom plot to the corresponding energy range.

# file_source.py
Can be used to import raw pulses from a tar source

# exporters.py
* drain: drains the buffer
* save_csv: saves entrys of the ringbuffer into a csv
* save_spectrum: creates a spectrum of the entrys and saves into a npy file
* save_parquet: saves raw pulses into a tar file

# analyzers.py
* single: analyzes the trigger channel for the pulse height
* coincidence: analyzes both channels, if in both channels exactly one peak was found, returns the height of both peaks and their time difference

# modules/pha.py
* find_pulse_start: finds the first zero crossing of the derivative left of the 'left_ips' defined by [scipy.signal.find_peaks()](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html).
* pha: returns the heights and times of pulses