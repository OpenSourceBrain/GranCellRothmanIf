# Integrate and Fire cerebellar granule cell model

This project contains an integrate and fire model of the cerebellar
granule cell and a simple model of the mossy fibre to granule cell
synapse. The cell model (IaF_GrC.nml) is the average (ie the one whose
parameters have the average value) of the model population developed
by Jason Rothman and published in Schwartz et, J Neurosci (2012). The
synaptic model is based on the one used in that same paper, but it has
been developed further to improve the fit to the experimental data and
to ensure LEMS/NeuroMLv2 compatibility.

## Current status

The model is conceptually stable, but less so as far as the
implementation is concerned. Currently, development is focused on
ensuring that most of the simulation configurations defined in this
neuroConstruct project run as intended in both NEURON and jLEMS (via
NeuroMLv2 export).
