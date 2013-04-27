#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET

def create_stim_rate_file(inh_rate, exc_rate, golgi_sync=False):
    Lems = ET.Element("Lems")
    # include Inputs.xml
    include = ET.SubElement(Lems, "Include")
    include.set("file", "Inputs.xml")
    # GoC firing rate
    inh_spikegen = ET.SubElement(Lems, "spikeGenerator")
    inh_spikegen.set("id", "golgiSpiker")
    if golgi_sync:
        if inh_rate == 0:
            inh_period = 1000000
        else:
            inh_period = 1./inh_rate
        inh_spikegen.set("period", "{0:f} s".format(inh_period))
    else:
        inh_spikegen.set("averageRate", "{0:d} per_s".format(inh_rate))
    # MF firing rate
    exc_spikegen = ET.SubElement(Lems, "spikeGeneratorPoisson")
    exc_spikegen.set("id", "mossySpiker")
    exc_spikegen.set("averageRate", "{0:d} per_s".format(exc_rate))
    # save to disk
    with open("InputFrequencies.xml", "w") as freq_file:
        ET.ElementTree(Lems).write(freq_file)

def main():
    jason_stim_range = np.array([30,60,90,120,150,180,210,240,300,360,420,480,540,600],
                                dtype=np.float)/4.
    jason_rates_156 = np.array([1.95918 ,9.89796, 30.4286, 51.6735,
                                  87.8163, 121.86, 165.324, 197.594, 258.538,
                                  296.905, 328.778, 351.688, 368.357, 377])
    exc_rate_range = np.arange(0, 150, 20)
    inh_rate_range = [0, 10, 50]
    out_firing_rates = []

    out_filename = "spike_count.dat"

    for inh_rate in inh_rate_range:
        out_firing_rates.append(np.zeros(shape=exc_rate_range.shape))
        for k, exc_rate in enumerate(exc_rate_range):
            create_stim_rate_file(inh_rate, exc_rate, golgi_sync=True)
            if os.path.isfile(out_filename):
                os.remove(out_filename)
            proc = subprocess.Popen(["jnml LEMS_rate_IO.xml"],
                                    shell=True,
                                    stdout=subprocess.PIPE)
            proc.communicate()
            spike_count = np.loadtxt(out_filename)[-1,1]
            print(inh_rate, exc_rate, spike_count)
            out_firing_rates[-1][k] = spike_count/1.

    fig, ax = plt.subplots()
    ax.plot(jason_stim_range, jason_rates_156, color="k", label="java")
    for k, inh_rate in enumerate(inh_rate_range):
        ax.plot(exc_rate_range, out_firing_rates[k],
                label="inh: {0}Hz".format(inh_rate))
    ax.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    main()


