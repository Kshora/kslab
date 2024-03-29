# kslab
Frequent use python modules for analysis.

# Features
graph_tools : usual graphic tools for spectrum analysis.<br>
langmuirprobe : Analysis module for Langmuire Probe signal. Underconstructing.<br>
qms : Processing module for QMS, permeations.<br>
raspi : Processing module for Raspberry pi data.<br>
spectrum : Analysis module for data from Czerny turner spectrometer.<br>

# Installation
Install kslab with pip command.
```bash
pip install git+https://github.com/Kshora/kslab
```

# Usage
```bash
import kslab

spec = Spectrometer(path)

lang = Langmuirprobe(basepath,date,species)

raspi = Raspi()

qms = Qms(datapath)
```

# Note 
I don't test environments under Linux and Mac

# Version , update
The latest version is '1.3.1'
The last update was on Decembeer 21 th '23

'1.0.0' : June 6 th '23<br>
'1.0.1' : June 15 th '23<br>
'1.1.0' : June 26 th '23<br>
'1.1.1' : June 27 th '23<br>
'1.1.2' : June 27 th '23<br>
'1.2.0' : October 5 th '23<br>
'1.2.1' : October 5 th '23<br>
'1.2.2' : October 5 th '23<br>
'1.2.3' : October 6 th '23<br>
'1.2.4' : October 12 th '23<br>
'1.2.5' : October 18 th '23<br>
'1.2.6' : October 20 th '23<br>
'1.2.7' : November 8 th '23<br>
'1.2.8' : November 22 th '23<br>
'1.2.9' : November 22 th '23<br>
'1.2.10' : November 24 th '23<br>
'1.2.11' : November 24 th '23<br>
'1.3.0' : November 30 th '23<br>
'1.3.1' : December 21 th '23<br>


When you have to update me, please smash
```bash
pip install -U git+https://github.com/Kshora/kslab
```

When I have to update, I have to update dist by
```bash
python setup.py sdist
```


# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details



