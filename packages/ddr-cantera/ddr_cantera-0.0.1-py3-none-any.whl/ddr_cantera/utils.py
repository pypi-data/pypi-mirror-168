# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 15:38:13 2022

@author: Darshan

Important functions dealing with cantera.
"""

import cantera as _ct


def get_density(pressure:float, temperature:float)->float:
    '''
    returns the density of air at given pressure and temperature. Calculates from equilibrating the gas to given temperature and pressure.

    Parameters
    ----------
    pressure : float
        gas pressure in atmosphere (atm).
    temperature : float
        temperature in degree celcius

    Returns
    -------
    float
        air density at given temperatuer and pressure.

    '''
    
    gas1 = _shared.air1
    gas1.TP = 273.15+temperature, pressure * _shared.one_atm
    gas1.equilibrate('TP')
    return gas1.density

def LPM_to_kg_per_sec(LPM: float,pressure:float=1,temperature:float=25)->float:
    '''
    converts LPM of air to kg/s. For this temperature and pressure at which the LPM is measured is to be mentioned.
    To convert LPM to kg/s, density is required and to specify the density we need pressure and temperature of the flow.

    Parameters
    ----------
    LPM : float
        Liters per minute.
    pressure : float, optional
        pressure in atmosphere (atm).pressure at which LPM is measured. The default is 1.
    temperature : float, optional
        temperature in degree celcius. temperature at which LPM is measured. The default is 25.

    Returns
    -------
    float
        kg/s

    '''
    return LPM /60000 * get_density(pressure=pressure, temperature=temperature)

def SLPM_to_kg_per_sec(SLPM: float)-> float:    
    '''
    converts SLPM of air to kg/s. the standard temperature is 25 degree celcius. and pressure is 1 atmosphere absolute.

    Parameters
    ----------
    SLPM : float
        standard liters per minute(SLPM) value.

    Returns
    -------
    float
        kg/s

    '''
    return SLPM /60000 * get_density(pressure=1, temperature=25)
    



def sound_speed(pressure=1, temperature=25, rtol=1.0e-6, maxiter=5000):
    """
    Sound speed is calculated by expression sqrt(dp/d(rho)).
    """
    
    gas = _shared.air1
    gas.TP = 273.15+temperature, pressure * _shared.one_atm

    # set the gas to equilibrium at its current T and P
    gas.equilibrate('TP', rtol=rtol, maxiter=maxiter)

    # save properties
    s0 = gas.s
    p0 = gas.P
    r0 = gas.density

    # perturb the pressure
    p1 = p0*1.0001

    # set the gas to a state with the same entropy and composition but
    # the perturbed pressure
    gas.SP = s0, p1

    # frozen sound speed
    afrozen = ((p1 - p0)/(gas.density - r0))**0.5

    return afrozen


