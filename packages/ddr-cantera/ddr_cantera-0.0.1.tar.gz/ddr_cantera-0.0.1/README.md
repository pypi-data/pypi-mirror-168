# ddr_cantera

To use this project Cantera should be installed in the environment otherwise *module not found error* will arise. Cantera is not installed by uinstalling this package.
This project includes some basic functionalities with cantera. Most of them includes density calculations using cantera but not all. Most functions calculates properties of air unless otherwise specified.

```py
import ddr_cantera
```

### Air properties calculation

```py
density = ddr_cantera.get_density(pressure=10, temperature=120)
```
returns air density at 10 bars(~ atm) pressure and 120 degree celcius temperature.

```py
mdot = ddr_cantera.LPM_to_kg_per_sec(LPM=100, pressure=10, temperature=120)
```
returns mass flow rate of air in kg/s from LPM.

```py
mdot = ddr_cantera.SLPM_to_kg_per_sec(SLPM=100)
```
returns mass flow rate of air in kg/s from SLPM. standard temperature is taken as 25 degree celcius and standard pressure is 1 atmosphere.

```py
a = ddr_cantera.sound_speed(pressure=2, temperature=25)
```
returns speed of sound in air. the sound speed is calculated by $\sqrt{\frac{\partial P}{\partial \rho}}$. wherein the gas is first equilibrium at initial TP and then pressure is perturbed and gas is again taken to another equilibrium at constant entropy. Hence from these two states $\partial P$ and $\partial \rho$ can be calculated.

This code is built upon the code from official cantera tutorials.