# Source: heart_throb_slider (demos/heart_throb_slider)
# Project URL: https://gitlab.pavlovia.org/demos/heart_throb_slider
# Original file: analysis/heartthrob-plot.py
'''
A basic plot of heart throb data

Author: Rebecca J Hirst
'''
import matplotlib.pyplot as plt
from psychopy import gui
import pandas as pd

# open a gui to select the data file
file = gui.fileOpenDlg(allowed="*.csv")
print('Opening file: ', file)

# read in the data
thisDat = pd.read_csv(file[0])

# extract the heart size column 
sizeData = thisDat['heart_height'][1:-1]# heart not set on first fame so size is 1
timeData = thisDat['time_stamp'][1:-1]# last sample is a NaN

# plot the data
with plt.xkcd():
    # plotting in xkcd style for fun (not necissary)
    fig, ax = plt.subplots(1)
    ax.plot(timeData, sizeData)
    ax.set_ylim([0, 1.5])
    ax.set_title("NERD EXCITEMENT")
    
    ax.annotate(
        'THAT DAY I\nPLAYED\nWITH SLIDERS',
        xy=(12, 0.4), arrowprops=dict(arrowstyle='->'), xytext=(14, 1))
        
        
    # add some axis labels
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    
    plt.show()