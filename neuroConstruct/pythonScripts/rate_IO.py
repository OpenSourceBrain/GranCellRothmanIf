#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Compare the NeuroMLv2 version of the model with Jason Rothman's
# granule cell number 156, which is close to the population average in
# terms of leak conductance and membrane capacitance (Cm=1.2pF,
# Gm=1.279nS, Em=-78mV).
import subprocess
import numpy as np
from matplotlib import pyplot as plt

# total stimulation rate (each of the 4 mossy fibres will spike at 1/4th of this)
jason_stim_range = np.array([30,60,90,120,150,180,210,240,300,360,420,480,540,600],
                            dtype=np.float)
jason_rates_156 = np.array([1.95918 ,9.89796, 30.4286, 51.6735,
                            87.8163, 121.86, 165.324, 197.594, 258.538,
                            296.905, 328.778, 351.688, 368.357, 377])


stim_rate_range = jason_stim_range
firing_rates_STP = np.zeros(shape=stim_rate_range.shape)
firing_rates_noSTP = np.zeros(shape=stim_rate_range.shape)

for stp in [True]:
    if stp:
        print(" --- STP --- ")
        sim_config = 'rate_IO_156'
        output_array = firing_rates_STP
    else:
        print(" --- no STP --- ")
        sim_config = 'rate_IO_noSTP'
        output_array = firing_rates_noSTP

    for k, stim_rate in enumerate(stim_rate_range):
        proc = subprocess.Popen(['nC.sh', '-python', 'rate_IO_simulate.py', sim_config, str(stim_rate)], stdout=subprocess.PIPE)
        proc_output = proc.communicate()[0]
        output_firing_rate = float(proc_output.rpartition('Output firing rate is ')[-1])
        output_array[k] = output_firing_rate
        print("in: {0:.1f}Hz  out: {1:.1f}Hz".format(stim_rate, output_firing_rate))

fig, ax = plt.subplots()
ax.plot(jason_stim_range, jason_rates_156, marker='o', color='k', label='Rothman 2012, +STD +inh')
ax.plot(stim_rate_range, firing_rates_STP, marker='s', color='g', label='NeuroMLv2, +STP')
#ax.plot(stim_rate_range, firing_rates_noSTP, marker='s', color='r', label='NeuroMLv2, -STP')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
for loc, spine in ax.spines.items():
    if loc in ['right','top']:
        spine.set_color('none')
ax.legend(loc='best')
plt.show()
