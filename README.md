# gamma-coincidence-spectroscopy

This is the repository for the gamma-coincidence-experiment at KIT

## Setup
### Physical Setup (16.12.2024)
* HPGe Detector 
    * -> High Voltage Supply (Kernforschung Nr. 62 848-72):
        * 3kV
        * Ramp Slope: 25V/Sec
        * Ouput Level: 10;0
        * Switch (Int/External Programming): Int
        * Switch (On/Off): On
        * Range: 0-3000
        * Ouput: Not connected
        * Preamp Supply: Not connected
        * (Back) Output H.V. connected to the Detector
    * -> One output (might be used with the oscilloscope for debugging)
    * -> One output to the Model 451 Spectroscopy Amplifier (Kernforschung Nr. 37 239-70)
        * Fine gain: ???
        * Coarse Gain: 100
        * Left Switch (Pos/Neg): Pos
        * Right Swich (Pos/Neg): Pos
        * Input: Connected to HPGe detector
        * Unipolar Output: Connected to RedPitaya (IN1)
        * Bipolar Output: (might be used with the oscilloscope for debugging)

* NaI Detector
    * -> Powersupply:
        * 1.09
        * Output connected to
    * -> Ortec Model 452 Spectroscopy Amplifier (Kernforschung Nr. 59 747-72)
        * Coarse Gain: 5
        * Fine Gain: 5;0
        * Shaping Time: 2.0
        * Output Range: +10V
        * Left Switch (Pos/Neg): Neg
        * Right Switch BLR (HI/LO/OUT) OUT
        * Unipolar Output: Connected to RedPitaya (IN2)






### Software
* Conda enviroment with python 11
* [mimoCoRB package](https://github.com/GuenterQuast/mimoCoRB) (64fc7826f13a1f00801dd0bddc1368cd67c8dc4f)
* [red-pitaya-notes](https://github.com/pavel-demin/red-pitaya-notes)
* This package

## The main.py script
* The `main.py` script creates a mimoCoRB setup and runs the mimoCoRB DAQ system.  
* The setup can be configured in three ways:
    * Input, whether the input data should be taken from the redpitaya or a tar source
    * Ouput, whether the data should be analyzed into a spectrum, a coincidence analysis or the raw pulses are to be saved
    * Trigger, on which channel the trigger is set.


# Debugging
`socket.gaierror: [Errno -2] Name or service not known`
* The connection to the RedPitaya could not be established. Check if the connection is

`TimeoutError: timed out`
* The RedPitaya did not receive a trigger signal on the specified channel for more than one second.
* To investigate the Problem:
    * Make sure both the detectors are connected correctly and have power
    * Check with an external Oscilloscope
    * Use the `mcpha.py` application from `git/red-pitaya-notes/projects/mcpha/client`
