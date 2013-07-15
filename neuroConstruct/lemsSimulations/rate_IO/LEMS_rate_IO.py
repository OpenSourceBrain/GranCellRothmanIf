#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
script_dir = os.path.dirname(__file__)

def create_stim_rate_file(inh_rate, exc_rate, golgi_sync=False):
    Lems = ET.Element("Lems")
    # include Inputs.xml
    include = ET.SubElement(Lems, "Include")
    include.set("file", "Inputs.xml")
    # # GoC firing rate
    # inh_spikegen = ET.SubElement(Lems, "spikeGenerator")
    # inh_spikegen.set("id", "golgiSpiker")
    # if golgi_sync:
    #     if inh_rate == 0:
    #         inh_period = 1000000
    #     else:
    #         inh_period = 1./inh_rate
    #     inh_spikegen.set("period", "{0:f} s".format(inh_period))
    # else:
    #     inh_spikegen.set("averageRate", "{0:d} per_s".format(inh_rate))
    # MF firing rate
    exc_spikegen = ET.SubElement(Lems, "spikeGeneratorPoisson")
    exc_spikegen.set("id", "mossySpiker")
    exc_spikegen.set("averageRate", "{0:d} per_s".format(exc_rate))
    #exc_spikegen.set("minimumISI", "1 ms")
    # save to disk
    with open(script_dir+"/InputFrequencies.xml", "w") as freq_file:
        ET.ElementTree(Lems).write(freq_file)

def main(plot=True):
    jason_stim_range = np.arange(60, 660, 60)/4
    jason_rates_156 = np.array([0.0, 0.7755102040816326, 4.55813953488372, 20.65625, 49.46153846153846, 88.9047619047619, 139.2222222222222, 187.6875, 227.64285714285717, 253.7142857142857])
    exc_rate_range = jason_stim_range
    inh_rate_range = [0]
    out_firing_rates = []
    exc_conductances_AMPA = []
    exc_conductances_NMDA = []

    sim_duration = 20. # s

    out_filename = "LEMS_spike_count.dat"
    print script_dir

    for inh_rate in inh_rate_range:
        out_firing_rates.append(np.zeros(shape=exc_rate_range.shape))
        exc_conductances_AMPA.append(np.zeros(shape=exc_rate_range.shape))
        exc_conductances_NMDA.append(np.zeros(shape=exc_rate_range.shape))
        for k, exc_rate in enumerate(exc_rate_range):
            create_stim_rate_file(inh_rate, exc_rate, golgi_sync=True)
            if os.path.isfile(out_filename):
                os.remove(out_filename)
            proc = subprocess.Popen(["jnml "+script_dir+"/LEMS_rate_IO.xml"],
                                    shell=True,
                                    stdout=subprocess.PIPE)
            proc.communicate()
            
            sim_data = np.loadtxt(out_filename)
            spike_count = sim_data[-1,1]
            # exc_cond_AMPA = 4 * sim_data[:,2:6].mean()
            # exc_cond_NMDA = 4 * sim_data[:,6:].mean()

            out_rate = spike_count/sim_duration
            print(inh_rate, exc_rate, out_rate)
            out_firing_rates[-1][k] = out_rate
            # exc_conductances_AMPA[-1][k] = exc_cond_AMPA * 1e9
            # exc_conductances_NMDA[-1][k] = exc_cond_NMDA * 1e9

    if plot:
        fig, ax = plt.subplots()
        ax.plot(jason_stim_range,
                jason_rates_156,
                color="r",
                linewidth=1.5,
                label="Jason (java)")
        for k, inh_rate in enumerate(inh_rate_range):
            ax.plot(exc_rate_range,
                    out_firing_rates[k],
                    linewidth=1.5,
                    label="jLEMS tGABA: {0}Hz".format(inh_rate))
        ax.legend(loc="best")


        cond_fig, cond_ax = plt.subplots()
        ratio_ax = cond_ax.twinx()
        ln_AMPA = cond_ax.plot(exc_rate_range,
                               exc_conductances_AMPA[0],
                               linewidth=1.5,
                               color="r",
                               label="AMPA")
        ln_NMDA = cond_ax.plot(exc_rate_range,
                               exc_conductances_NMDA[0],
                               linewidth=1.5,
                               color="#5F04B4",
                               label="NMDA")
        ln_ratio = ratio_ax.plot(exc_rate_range,
                                 exc_conductances_NMDA[0]/exc_conductances_AMPA[0],
                                 linewidth=1.5,
                                 color="k",
                                 label="NMDA/AMPA ratio")
        lines = ln_AMPA + ln_NMDA + ln_ratio
        labels = [ln.get_label() for ln in lines]
        cond_ax.legend(lines, labels, loc="best")
        cond_ax.set_xlabel("Input rate (Hz) (single MF)")
        cond_ax.set_ylabel("Time-averaged conductance (nS)")
        ratio_ax.set_ylabel("NMDA to AMPA conductance ratio")
        
        plt.show()

    return out_firing_rates


if __name__ == "__main__":
    main()


