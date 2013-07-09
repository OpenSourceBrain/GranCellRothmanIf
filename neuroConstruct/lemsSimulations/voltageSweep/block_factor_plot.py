#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

lems_data = np.loadtxt('blockFactorVSVoltage.dat')
voltage = lems_data[:,1] * 1000. # (mV)
block_factor_Rothman = lems_data[:,2]
block_factor_Ward = lems_data[:,3]

fig, ax = plt.subplots()
ax.fill_between(voltage, block_factor_Rothman, color="g")
ax.fill_between(voltage, block_factor_Ward, color="r", alpha=0.5)
ax.set_xlabel('membrane voltage (mV)')
ax.set_ylabel('gNMDA unblocked fraction')
ax.set_xlim(left=-102, right=42)
ax.set_ylim(bottom=0, top=1)
ax.grid()

plt.show()
