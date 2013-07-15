#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Compare the NeuroMLv2 version of the model with Jason Rothman's
# granule cell number 156, which is close to the population average in
# terms of leak conductance and membrane capacitance (Cm=1.2pF,
# Gm=1.279nS, Em=-78mV).
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append('../lemsSimulations/rate_IO')

import LEMS_rate_IO

# total stimulation rate (each of the 4 mossy fibres will spike at 1/4th of this)
jason_stim_range = np.arange(60., 660, 60)/4
jason_rates_156 = np.array([0.0, 0.7755102040816326, 4.55813953488372, 20.65625, 49.46153846153846, 88.9047619047619, 139.2222222222222, 187.6875, 227.64285714285717, 253.7142857142857])


result_filename = 'NEURON_firing_rate.dat'
stim_rate_range = jason_stim_range
firing_rates_STP = np.zeros(shape=stim_rate_range.shape)
firing_rates_noSTP = np.zeros(shape=stim_rate_range.shape)

sim_config = 'rate_IO'
output_array = firing_rates_STP

lems_firing_rates = LEMS_rate_IO.main(plot=False)[0]
print("LEMS firing rates: {}".format(lems_firing_rates))

for k, stim_rate in enumerate(stim_rate_range):
    subprocess.call(['nC.sh', '-python', 'rate_IO_simulate.py', sim_config, str(stim_rate)])
    with open(result_filename, "r") as f:
        output_firing_rate = float(f.read())
    output_array[k] = output_firing_rate
    print("in: {0:.1f}Hz  out: {1:.1f}Hz".format(stim_rate, output_firing_rate))

fig, ax = plt.subplots()
ax.plot(jason_stim_range, jason_rates_156, marker='o', color='k', label='Rothman 2012, +STD +inh')
ax.plot(stim_rate_range, firing_rates_STP, marker='s', color='g', label='2013, NEURON')
ax.plot(stim_rate_range, lems_firing_rates, marker='^', color='r', label='2013, jLEMS')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
for loc, spine in ax.spines.items():
    if loc in ['right','top']:
        spine.set_color('none')
ax.legend(loc='best')
plt.show()
