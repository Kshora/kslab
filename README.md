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
The latest version is '1.0.1'
The last update was on June 15 th '23

When you have to update me, please smash
```bash
pip install -U git+https://github.com/Kshora/kslab
```

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details
