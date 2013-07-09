TITLE Mod file for component: Component(id=NMDA type=NMDA)

NEURON {
    POINT_PROCESS NMDA
    RANGE erev                             : parameter
    RANGE directAmp1                       : parameter
    RANGE directAmp2                       : parameter
    RANGE directTauRise                    : parameter
    RANGE directTauDecay1                  : parameter
    RANGE directTauDecay2                  : parameter
    RANGE directDepressionConstant         : parameter
    RANGE directMinimumDepression          : parameter
    RANGE directDepressionRecoveryTime     : parameter
    RANGE directFacilitationConstant       : parameter
    RANGE directMaximumFacilitation        : parameter
    RANGE directFacilitationRecoveryTime   : parameter
    RANGE g                                : exposure
    RANGE i                                : exposure

    NONSPECIFIC_CURRENT i

    RANGE RothmanBlock_z                   : parameter
    RANGE RothmanBlock_T                   : parameter
    RANGE RothmanBlock_blockConcentration  : parameter
    RANGE RothmanBlock_deltaBind           : parameter
    RANGE RothmanBlock_deltaPerm           : parameter
    RANGE RothmanBlock_C1                  : parameter
    RANGE RothmanBlock_C2                  : parameter
    RANGE RothmanBlock_faradayConstant     : parameter
    RANGE RothmanBlock_idealGasConstant    : parameter
    RANGE RothmanBlock_scaling             : exposure
    RANGE RothmanBlock_theta               : derived var

    RANGE block                            : derived var

    RANGE directPeakTime1                  : derived var

    RANGE directPeakTime2                  : derived var

    RANGE directFactor1                    : derived var

    RANGE directFactor2                    : derived var

}

UNITS {

    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (um) = (micrometer)

}

PARAMETER {

    erev = 0 (mV)
    directAmp1 = 2.129E-4 (uS)
    directAmp2 = 1.616E-4 (uS)
    directTauRise = 1.035 (ms)
    directTauDecay1 = 8.118 (ms)
    directTauDecay2 = 37.050003 (ms)
    directDepressionConstant = 0.9
    directMinimumDepression = 0.1
    directDepressionRecoveryTime = 70 (ms)
    directFacilitationConstant = 1.7
    directMaximumFacilitation = 3.4
    directFacilitationRecoveryTime = 3.5 (ms)
    RothmanBlock_z = 2
    RothmanBlock_T = 308.15 (K)
    RothmanBlock_blockConcentration = 1 (mM)
    RothmanBlock_deltaBind = 0.35
    RothmanBlock_deltaPerm = 0.53
    RothmanBlock_C1 = 2.07 (mM)
    RothmanBlock_C2 = 0.015 (mM)
    RothmanBlock_faradayConstant = 96485.336 (coulomb)
    RothmanBlock_idealGasConstant = 8314.462 (millijoule / K) : (idealGasConstantDims)
}

ASSIGNED {
    ? Standard Assigned variables with baseSynapse
    v (mV)

    RothmanBlock_theta (/mV)               : derived var

    RothmanBlock_scaling                   : derived var

    block                                  : derived var

    g (uS)                                 : derived var

    i (nA)                                 : derived var

    directPeakTime1 (ms)                   : derived var

    directPeakTime2 (ms)                   : derived var

    directFactor1                          : derived var

    directFactor2                          : derived var
    rate_directA1 (1/ms)
    rate_directA2 (1/ms)
    rate_directB1 (1/ms)
    rate_directB2 (1/ms)
    rate_directDepressionFactor (1/ms)
    rate_directFacilitationFactor (1/ms)

}

STATE {
    directA1
    directA2
    directB1
    directB2
    directDepressionFactor
    directFacilitationFactor

}

INITIAL {
    rates()

    directA1 = 0

    directA2 = 0

    directB1 = 0

    directB2 = 0

    directDepressionFactor = 1

    directFacilitationFactor = 1

}

BREAKPOINT {

    SOLVE states METHOD cnexp

    if (directDepressionFactor < directMinimumDepression) {
        directDepressionFactor = directMinimumDepression
    }

    if (directFacilitationFactor > directMaximumFacilitation) {
        directFacilitationFactor = directMaximumFacilitation
    }


}

NET_RECEIVE(weight (uS)) {
    state_discontinuity(directA1, ( directA1 + ( directDepressionFactor * directFactor1 )))
    state_discontinuity(directA2, ( directA2 + ( directDepressionFactor * directFactor2 )))
    state_discontinuity(directB1, ( directB1 + ( directDepressionFactor * directFactor1 )))
    state_discontinuity(directB2, ( directB2 + ( directDepressionFactor * directFactor2 )))
    state_discontinuity(directDepressionFactor, ( directDepressionConstant * directDepressionFactor ))
    state_discontinuity(directFacilitationFactor, ( directFacilitationConstant * directFacilitationFactor ))

}

DERIVATIVE states {
    rates()
    directA1' = rate_directA1
    directA2' = rate_directA2
    directB1' = rate_directB1
    directB2' = rate_directB2
    directDepressionFactor' = rate_directDepressionFactor
    directFacilitationFactor' = rate_directFacilitationFactor

}

PROCEDURE rates() {

    RothmanBlock_theta = (( RothmanBlock_z * RothmanBlock_faradayConstant ) / ( RothmanBlock_idealGasConstant * RothmanBlock_T )) ? evaluable

    RothmanBlock_scaling = ((( RothmanBlock_C1 * exp((( RothmanBlock_deltaBind * RothmanBlock_theta ) * v))) + ( RothmanBlock_C2 * exp((0 - (( RothmanBlock_deltaPerm * RothmanBlock_theta ) * v))))) / ((( RothmanBlock_C1 * exp((( RothmanBlock_deltaBind * RothmanBlock_theta ) * v))) + ( RothmanBlock_C2 * exp((0 - (( RothmanBlock_deltaPerm * RothmanBlock_theta ) * v))))) + ( RothmanBlock_blockConcentration * exp((( RothmanBlock_deltaBind * RothmanBlock_theta ) * v))))) ? evaluable

    ? DerivedVariable is based on path: RothmanBlock/scaling from RothmanBlock: Component(id=null type=RothmanBlock)
    block = RothmanBlock_scaling ? path

    g = ( block * (( directAmp1 * ( directB1 - directA1 )) + ( directAmp2 * ( directB2 - directA2 )))) ? evaluable

    i = -1 * ( g * ( erev - v)) ? evaluable

    directPeakTime1 = ((( directTauRise * directTauDecay1 ) / ( directTauDecay1 - directTauRise )) * log(( directTauDecay1 / directTauRise ))) ? evaluable

    directPeakTime2 = ((( directTauRise * directTauDecay2 ) / ( directTauDecay2 - directTauRise )) * log(( directTauDecay2 / directTauRise ))) ? evaluable

    directFactor1 = (1 / ((0 - exp((0 - ( directPeakTime1 / directTauRise )))) + exp((0 - ( directPeakTime1 / directTauDecay1 ))))) ? evaluable

    directFactor2 = (1 / ((0 - exp((0 - ( directPeakTime2 / directTauRise )))) + exp((0 - ( directPeakTime2 / directTauDecay2 ))))) ? evaluable

    rate_directA2 = (0 - ( directA2 / directTauRise ))
    rate_directFacilitationFactor = ((1 - directFacilitationFactor ) / directFacilitationRecoveryTime )
    rate_directDepressionFactor = ((1 - directDepressionFactor ) / directDepressionRecoveryTime )
    rate_directA1 = (0 - ( directA1 / directTauRise ))
    rate_directB2 = (0 - ( directB2 / directTauDecay2 ))
    rate_directB1 = (0 - ( directB1 / directTauDecay1 ))





}

