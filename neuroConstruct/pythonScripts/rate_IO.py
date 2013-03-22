#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import numpy as np
from matplotlib import pyplot as plt

jason_stim_range = np.arange(15, 165, 15)
jason_rates_plast_phi06 = np.array([0.00, 0.12, 0.53, 4.06, 13.04, 31.52, 56.33, 93.56, 134.29, 165.93])


stim_rate_range = np.arange(15, 45, 15)
firing_rates = np.zeros(shape=stim_rate_range.shape)

for k, stim_rate in enumerate(stim_rate_range):
    proc = subprocess.Popen(['nC.sh', '-python', 'rate_IO_simulate.py', str(stim_rate)], stdout=subprocess.PIPE)
    proc_output = proc.communicate()[0]
    output_firing_rate = float(proc_output.rpartition('Output firing rate is ')[-1])
    firing_rates[k] = output_firing_rate
    print("in: {0:d}Hz  out: {1:d}Hz".format(stim_rate, int(round(output_firing_rate))))



fig, ax = plt.subplots()
ax.plot(jason_stim_range, jason_rates_plast_phi06, marker='o', color='k', label='Rothman 2012, +STD +inh')
ax.plot(stim_rate_range, firing_rates, marker='s', color='g', label='NeuroMLv2')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
for loc, spine in ax.spines.items():
    if loc in ['right','top']:
        spine.set_color('none')
ax.legend(loc='best')
plt.show()
