#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Simulation of random particle steps to left or right: Example4_1.py          
# Description: Diffusion in one-dimension starting from a step distribution

# Importing libraries and functions used later
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import random as rng      # Pseudo-random number generator
from numpy.random import seed               # Allows setting of rng seed
import datetime                             # Used to track runtime

# Setting fixed parameter values
X_Locs = 2 * 350                            # Even number of prtcl lctns
Max_Points = 1000                           # Init num of prtcls @ left lctns
Min_Points = 0                              # Init num of prtcls @ right lctns
N_Frames = 10000                            # Num of times to recalculate dist

# Creating the initial distribution of particles from which
#  we start the diffusion simulation
X = np.linspace(0,X_Locs-1,X_Locs,dtype=int)        # Int array of x locations
YA = Max_Points * np.ones(int(X_Locs/2),dtype=int)  # Prtcls on left half
YB = Min_Points * np.ones(int(X_Locs/2),dtype=int)  # Prtcls on right half
Y = np.hstack([YA,YB])                              # Prtcls for all x lctns
Y0= 1 * Y                                           # Save init distribution
Spread = np.zeros(N_Frames,dtype=int)               # To track profile spread

# Setting rng seed, printing out initial number of particles and
#  setting how often to print out simulation progress
seed(1)                                             # Seed num to start rng
print("Total number of particles at start = {}".format(np.sum(Y)))
NN = 4                                              # Num times to print prog
now0 = datetime.datetime.now()                      # Time at start of sim

# Calculate the particle profiles at each time point
for i in range(0,N_Frames):
    Z = 0 * Y                                       # Allocate next prtcl prfl
    # Print out progress at the desgnated intervals
    if(i!=0 and i%(N_Frames/NN)):
        now1 = datetime.datetime.now()
        print("{} out of {} frames; elapsed minutes = {:2f}".format(i\
         ,N_Frames,60*(now1.hour-now0.hour)+(now1.minute-now0.minute)+\
         (now1.second-now0.second)/60))
    # Here we run through each x location and move particles by randaom walk
    for j in range(X_Locs):
        # In the first x position we either stay or move to the right
        if j == 0:
            for k in range(Y[j]):
                if rng() < 0.5: Z[j] += 1           # Stays at first location
                else: Z[j+1] += 1                   # Moves right
        # At the last x position we either stay or move to the left
        elif j == X_Locs-1:
            for k in range(Y[j]):
                if rng() < 0.5: Z[j] += 1           # Stays at last location
                else: Z[j-1] += 1                   # Moves left
        # in the middle clocations either move left or right        
        else:
            for k in range(Y[j]):
                if rng() < 0.5: Z[j-1] += 1         # Movs left
                else: Z[j+1] += 1                   # Moves right
    Y = 1 * Z                                       # Now save Z as new Y 
    # Now calculate the spread for the recently calculated profile
    index_1 = 0
    index_2 = 0
    for j in range(X_Locs):
        if index_1 == 0 and Z[j] < (0.75*Max_Points):
            index_1 = j
        if index_2 == 0 and Z[j] < (0.25*Max_Points):
            index_2 = j
    Spread[i] = index_2 - index_1
    
# The simulation of the evolution of the diffusion is complete
#  so now we echo the final simulation time, statistics and make plots

# Final simulation time
now2 = datetime.datetime.now()
print("{} out of {} frames; minutes of caclulation = {:2f}".format(N_Frames\
 ,N_Frames,60*(now1.hour-now0.hour)+(now1.minute-now0.minute)+\
 (now1.second-now0.second)/60))
    
# Statistics
print("Total number of particles at end = {}".format(np.sum(Y)))
print("Number of particles in first half = {}".format(np.sum(Y[0:int(X_Locs/2)])))
print("Number of particles in second half = {}".format(np.sum(Y[int(X_Locs/2):X_Locs])))
print("Spread in final profile (3/4 to 1/4) = {}".format(index_2 - index_1))

# Plots - Initial and final profile then Spread as a function of frame number
plt.figure()
plt.plot(X,Y0,'gray')                               # Intital profile
plt.plot(X,Y,'.k',markersize=4)                     # Final profile
plt.xlim(0,X_Locs)
plt.ylim(0,1.2*Max_Points)
plt.xlabel("X Location")
plt.ylabel("Number of Particles")
plt.title("Simulation of 1-D Particle Diffusion Starting from a Step Distribution")
# plt.savefig("Example4_1a.png,dpi=200)

plt.figure()
plt.plot(range(N_Frames),Spread,'.k',markersize=1)
plt.xlim(0,N_Frames)
plt.ylim(0,1.6*np.sqrt(N_Frames))
plt.xlabel("Frame Number (Time)")
plt.ylabel("Spread of Profile (3/4 to 1/4)")
plt.title("Simulation of 1-D Particle Diffusion Starting from a Step Distribution")
# plt.savefig("Example4_1b.png,dpi=200)




           
            








