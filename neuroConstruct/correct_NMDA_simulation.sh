#!/bin/bash

# returns number of granule cell spikes for a simulation conducted
# with the 'hand corrected' version of the NMDA mod file.

# usage: correct_NMDA_simulation.sh sim_ref

cd /home/ucbtepi/nC_projects/GranCellRothmanIf/neuroConstruct/generatedNEURON &&
cp ../NMDA_hand_corrected.mod NMDA.mod &&
nrnivmodl &&
./runsim.sh <<EOF &&
EOF
numspikes=`wc -l < ../simulations/$1/GrCs_0.SPIKE_min40.spike`
echo "Number of spikes is $numspikes"