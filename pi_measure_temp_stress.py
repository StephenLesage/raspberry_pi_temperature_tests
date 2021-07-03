# Measure RPi's CPU temperature over time and plot it

# Import libraries
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import os
import gpiozero

# Initial Parameters (i=0 == 0V: i=1 == 3.3V: i=2 == 5V)
i=0

# Define variables
dt = 5                       # approx seconds to wait between consecutive measurements
I = 12                       # total measurements on idle
S = 12                       # total measurements under stress
C = 13                       # total measurements during cooldown
M = I+S+C                    # total measurements
temps_idle = np.zeros(I)     # Array to hold temperature measurements on idle
time_idle = np.zeros(I)      # Array to hold temperature times on idle
temps_stress = np.zeros(S)   # Array to hold temperature measurements under stress
time_stress = np.zeros(S)    # Array to hold temperature times under stress
temps_cooldown = np.zeros(C) # Array to hold temperature measurements during cooldown
time_cooldown = np.zeros(C)  # Array to hold temperature times during cooldown
data_loc = "/sys/class/thermal/thermal_zone0/temp" #Path to file with thermal info

# Take measurements
print("\nStarting temperature measurements.")
time0 = int(time.time())                             # Read the "reference time"
for T in range(I):
    temp_file = open(data_loc, "r")                  # Open temperature file
    temps_idle[T] = float(temp_file.read())/1000     # Read temperature
    time_idle[T] = int(time.time())-time0            # Read time
    temp_file.close()                                # Close temperature file
    time.sleep(dt)                                   # Wait dt seconds
print("Maximizing CPU usage")
os.system("yes &")
for T in range(S):
    temp_file = open(data_loc, "r")                  # Open temperature file
    temps_stress[T] = float(temp_file.read())/1000   # Read temperature
    time_stress[T] = int(time.time())-time0          # Read time
    temp_file.close()                                # Close temperature file
    time.sleep(dt)                                   # Wait dt seconds
os.system("killall yes")
print("Cooling down system")
for T in range(C):
    temp_file = open(data_loc, "r")                  # Open temperature file
    temps_cooldown[T] = float(temp_file.read())/1000 # Read temperature
    time_cooldown[T] = int(time.time())-time0        # Read time
    temp_file.close()                                # Close temperature file
    time.sleep(dt)                                   # Wait dt seconds
print("Finished temperature measurements.")

# For .txt and plot lables
volts=''
if i==0:
    volts='0V'
if i==1:
    volts='3.3V'
if i==2:
    volts='5V'

# Plot data
np.savetxt("temp_data_idle_"+volts+".txt", (time_idle,temps_idle))             # Save data in text file in current folder
np.savetxt("temp_data_stress_"+volts+".txt", (time_stress,temps_stress))       # Save data in text file in current folder
np.savetxt("temp_data_cooldown_"+volts+".txt", (time_cooldown,temps_cooldown)) # Save data in text file in current folder
print("temp_data values have been outputed to .txt file.")

plt.plot(np.append(time_idle,time_stress[0]),np.append(temps_idle,temps_stress[0]),'gs-',
	np.append(time_stress,time_cooldown[0]),np.append(temps_stress,temps_cooldown[0]),'rs-',
	time_cooldown,temps_cooldown,'bs-')
plt.xlabel("Time (s)")
plt.ylabel("Temperature ($\circ$C)")
plt.title("RPi CPU Temperature Evolution ("+volts+")")
plt.legend(["Idle","Stress","Cooldown"])

plt.savefig("temp_data_stress_"+volts+".png", dpi=300)
print("temp_data_stress graph has been outputed to .png file.")
