#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt

stim_rate_range = np.arange(0, 15, 10)
firing_rates = np.zeros(shape=stim_rate_range.shape)

filename = "spike_count.dat"

for k, stim_rate in enumerate(stim_rate_range):
    while True:
        try:
            if os.path.isfile(filename):
                os.remove(filename)
            proc = subprocess.Popen(['jnml LEMS_rate_IO.xml'], shell=True, stdout=subprocess.PIPE)
            proc.communicate()
            spike_count = np.loadtxt(filename)[-1,1]
            print(spike_count)
            firing_rates[k] = spike_count/10.
            break
        except ValueError:
            print("Error while reading LEMS output file. Retrying...")
            pass
print(firing_rates)

