# gamma-coincidence-spectroscopy

## Setup
### RedPitaya
* Copy the Image onto an SD card
* Connect the RedPitaya to the amplifiers, PC and power.
### Amplifiers
* This is the setup that was used during the Bachelor Thesis:

| Configuration               | HPGe                                     | NaI                                 |
|-----------------------------|------------------------------------------|-------------------------------------|
| Pre-Amplifier               | $2.6\mathrm{kV}$                         | 0.94                                |
| Amplifier                   | Ortec Model 410 Linear Amplifier         | Ortec Model 410 Multimode Amplifier |
| Kernforschung Nr.           | 44 140-70                                | 0500 66                             |
| Input Polarity              | Pos                                      | Neg                                 |
| Input Attenuator            | 1                                        | 1                                   |
| Fine Gain                   | 1.7                                      | 2.5                                 |
| Coarse Gain                 | 1                                        | 1                                   |
| Integration                 | 2                                        | 5                                   |
| 1st Differentiation (Outer) | 1                                        | 1                                   |
| 2nd Differentiation (Inner) | Out                                      | D.L. (Delay Line)                   |
| Output                      | Unipolar Output ($Z_0 \approx 10\Omega$) | Unipolar Output                     |
| Red Pitaya Connection       | Ch1 $50\Omega$                           | Ch2 $50\Omega$                      |


### Software
* ?? Is python11 enviroment still required??
* Install mimoCoRB &rarr; what release
* Install packages &rarr; test what packages are required; kafe2 and PhyPraKit should suffice

## The main.py script
* The ```main.py``` script creates a mimoCoRB setup and runs the mimoCoRB DAQ system.  
* The setup can be configured in three ways:
    * Input, whether the input data should be taken from the redpitaya or a tar source
    * Ouput, whether the data should be analyzed into a spectrum, a coincidence analysis or the raw pulses are to be saved
    * Trigger, on which channel the trigger is set. This is only relevant for the spectrum and the redpitaya.