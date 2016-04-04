#!/usr/bin/env python

from decimal import Decimal
import numpy as np
import scipy as scp
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import math as m
import cmath as cm
import os
import time
import datetime
import serial

# arrays defining relationship of temperature profile
tempArray = []
timeArray = []

# variable to keep track of measurement count (to determine desired reference time)
iteration = 1

# request and convert sampling rate to interval period
os.system("clear")
print("Enter a sampling rate:\n"),
sRate = input()
sPeriod = (1.0 / float(sRate))
print("\n")

# calculating necessary precision to represent selected sampling resolution
if (float(sRate) < 1.0):
    precision = 0
else:
    precision = len(sRate)-1

# set reference starting time
start_time = time.time()

# identify save file for all data recorded via start time ref.
filename = "DataLogs/TemperatureProfile(" + str(datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d-%H:%M:%S')) + ").txt"

# prep file with relevant categorical header titles
with open(filename, "a") as myfile:
    myfile.write("Time (s) | Temp (C)\n") 

try:
    while 1:
    
        # open UART connection to LM4f at spec. baud rate
        ser = serial.Serial('/dev/lm4f', 115200)

        # dictates sampling intervals by comparing current lapse to discrete rate
        if (time.time() - start_time) >= (sPeriod * iteration):

            # read data from lm4f UART (not gonna lie, taking it twice is a hack)
            temp = ser.readline()
            temp = ser.readline()

            # generate associated data time stamp (relative to start)
            elapsed_time = time.time() - start_time

            # convert binary literal to float and int values
            temp = temp.decode()
            temp = float(temp.rstrip('\x00\r\n'))
            dtemp = int(temp)

            # convert time float value to decimal with designated precision
            dtime = Decimal(elapsed_time)
            dtime = round(dtime, precision)

            # append time-temp combination to end of associated arrays
            tempArray.append(temp)
            timeArray.append(elapsed_time)

            # display and save time-temp combination as data variable
            data = str(dtime) + "     -     " + str(dtemp)
            print(data)
            with open(filename, "a") as myfile:
                myfile.write(data + "\n") 

            # do I really need to explain?
            iteration += 1
            ser.close()

except:
    KeyboardInterrupt

print("\nStopping...")

# start of plotting section
fig = plt.figure(1)
 
# aesthetics are important, bro
ax = plt.gca()
ax.set_axis_bgcolor('black')
ax.yaxis.label.set_color('gray')
ax.xaxis.label.set_color('gray')
ax.tick_params(axis = 'x', colors = 'green')
ax.tick_params(axis = 'y', colors = 'green')
fig.patch.set_facecolor('0.000')
plt.grid(color = 'green')
ax.spines['top'].set_visible(0.5)
ax.spines['right'].set_visible(0.5)
ax.spines['bottom'].set_visible(0.5)
ax.spines['left'].set_visible(0.5)
ax.spines['top'].set_color('0.15')
ax.spines['right'].set_color('0.15')
ax.spines['bottom'].set_color('0.15')
ax.spines['left'].set_color('0.15')

# final output
plt.plot(timeArray, tempArray, linewidth=1.5, color='green')
plt.show()


# /// CAUTION - DEBUGGING ZONE - KEEP OUT ///


#for i in range(len(tempArray)):
#    print ("\nTemps: " + str(tempArray[i]))
#for i in range(len(timeArray)):
#    print ("\nTimes: " + str(timeArray[i]))
