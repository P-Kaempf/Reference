# Reference


## Getting started

Launch main.py and make sure that some data is available. For that reason, the folder Daten_2022 has been added. Unzip it and enter its path when prompted.

## Use

First select the data folder, then click "compute". Then the results can be plotted or pickled. A simple console window (output only) keeps you informed of what happens.

## Components and Dependencies

**main.py**
- import ui
- import sys

**classes.py**
- from dataclasses import dataclass
- import pandas as pd
- from datetime import date

**ui.py**
- import os.path
- import shutil
- import PySimpleGUI as sg
- import platform
- import traceback
- import file
- import data
- import plot
- import classes

**data.py**
- import numpy as np
- import pandas
- import classes
- from classes import parameters
- import ui

**files.py**
- import os
- import csv
- import traceback
- import numpy as np
- from operator import add
- from datetime import date
- import pickle
- import classes
- import data
- import plot
- import ui

**plot.py**
- import numpy as np
- import platform
- import matplotlib.pyplot as plt
- import matplotlib
- import classes
- import data
- from scipy.signal import savgol_filter

## License

This is the super-closed STABILO license. If you only do as much as look at the files and are not part of the team, you will burn in hell.
