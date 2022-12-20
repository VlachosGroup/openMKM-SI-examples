"""
A simplistic approach to mechanism reduction which demonstrates Cantera's
features for dynamically manipulating chemical mechanisms.

Here, we use the full GRI 3.0 mechanism to simulate adiabatic, constant pressure
ignition of a lean methane/air mixture. We track the maximum reaction rates for
each reaction to determine which reactions are the most important, according to
a simple metric based on the relative net reaction rate.

We then create a sequence of reduced mechanisms including only the top reactions
and the associated species, and run the simulations again with these mechanisms
to see whether the reduced mechanisms with a certain number of species are able
to adequately simulate the ignition delay problem.

Requires: cantera >= 2.6.0, matplotlib >= 2.0
Keywords: kinetics, combustion, reactor network, editing mechanisms, ignition delay,
          plotting
"""

import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

gas = ct.Solution('gri30.yaml')
initial_state = 1200, 5 * ct.one_atm, 'CH4:0.35, O2:1.0, N2:3.76'

# Run a simulation with the full mechanism
gas.TPX = initial_state
r = ct.IdealGasConstPressureReactor(gas)
sim = ct.ReactorNet([r])

t = 0.0
dt = 0.0001
states = ct.SolutionArray(gas, extra=['t'])
while t < 0.02:
    print(t)
    t += dt
    sim.advance(t)
    states.append(r.thermo.state, t=t*1000)

aliases = {'CO2': 'CO$_2$', 'CH4': 'CH$_4$'}
for name, alias in aliases.items():
    gas.add_species_alias(name, alias)

data = pd.read_csv('rctr_state_tr.csv', index_col=False)
print(data)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1,
                               figsize=(6, 8)
                               )
ax1.plot(states.t, states.T, lw=4, label='Cantera')
ax1.plot(data['t(s)']*1000, data['Temperature'], '^-', markevery=50, label='OpenMKM')
ax1.set_xlabel('time [ms]')
ax1.set_ylabel('Temperature (K)')
ax1.legend(loc='best')

data = pd.read_csv('gas_mass_tr.csv', index_col=False)
for spc in aliases:
    ax2.plot(states.t, states(aliases[spc]).Y,
             label=aliases[spc] + '-Cantera',
             lw=4
             )
    ax2.plot(data['t(s)']*1000, data[spc],
             marker='^',
             markevery=50,
             label=aliases[spc] + '-OpenMKM')
ax2.set_xlabel('time [ms]')
ax2.set_ylabel('mass fraction')
ax2.legend(loc='best')
plt.tight_layout()
plt.savefig("Figure.png")
plt.show()
