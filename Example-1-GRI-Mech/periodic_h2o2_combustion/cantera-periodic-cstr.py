"""
Modified by K.S and B.M Oct-2022:
This is a modified Cantera Example taken from:
https://cantera.org/examples/python/reactors/periodic_cstr.py.html

Original code description starts here:
This example illustrates a continuously stirred tank reactor (CSTR) with steady
inputs but periodic interior state.

A stoichiometric hydrogen/oxygen mixture is introduced and reacts to produce
water.  But since water has a large efficiency as a third body in the chain
termination reaction

       H + O2 + M = HO2 + M

as soon as a significant amount of water is produced the reaction stops. After
enough time has passed that the water is exhausted from the reactor, the mixture
explodes again and the process repeats. This explanation can be verified by
decreasing the rate for reaction 7 in file h2o2.yaml and re-running the
example.

Acknowledgments: The idea for this example and an estimate of the conditions
needed to see the oscillations came from Bob Kee, Colorado School of Mines

Requires: cantera >= 2.5.0, matplotlib >= 2.0
Keywords: combustion, reactor network, well-stirred reactor, plotting
"""

import cantera as ct
import matplotlib.pyplot as plt
import pandas as pd


# create the gas mixture
gas = ct.Solution('h2o2.yaml')

# pressure ~60 Torr, T = 770 K
p = 8000.0  # Pressure in Pa (modified)
t = 770.0

gas.TPX = t, p, 'H2:2, O2:1'

# create an upstream reservoir that will supply the reactor. The temperature,
# pressure, and composition of the upstream reservoir are set to those of the
# 'gas' object at the time the reservoir is created.
upstream = ct.Reservoir(gas)

# Now create the reactor object with the same initial state
cstr = ct.IdealGasReactor(gas)

# Set its volume to 10 cm^3. In this problem, the reactor volume is fixed, so
# the initial volume is the volume at all later times.
cstr.volume = 10.0 * 1.0e-6

# We need to have heat loss to see the oscillations. Create a reservoir to
# represent the environment, and initialize its temperature to the reactor
# temperature.
env = ct.Reservoir(gas)

# Create a heat-conducting wall between the reactor and the environment. Set its
# area, and its overall heat transfer coefficient. Larger U causes the reactor
# to be closer to isothermal. If U is too small, the gas ignites, and the
# temperature spikes and stays high.
w = ct.Wall(cstr, env, A=1.0, U=0.002)

# Connect the upstream reservoir to the reactor with a mass flow controller
# (constant mdot). Set the mass flow rate to 0.75 cm^3/s
vdot = 0.75 * 1.0e-6  # m3/s (modified)
mdot = gas.density * vdot  # kg/s
mfc = ct.MassFlowController(upstream, cstr, mdot=mdot)

# now create a downstream reservoir to exhaust into.
downstream = ct.Reservoir(gas)

# connect the reactor to the downstream reservoir with a valve, and set the
# coefficient sufficiently large to keep the reactor pressure close to the
# downstream pressure of 60 Torr.
v = ct.Valve(cstr, downstream, K=1.0e-9)

# create the network
network = ct.ReactorNet([cstr])

# now integrate in time
t = 0.0
dt = 1e-2

states = ct.SolutionArray(gas, extra=['t'])
while t < 100.0:
    print(t)
    t += dt
    network.advance(t)
    states.append(cstr.thermo.state, t=t)

# Plot result comparisons between OpenMKM and Cantera.
# modified section

aliases = {'H2O': 'H$_2$O'}
for name, alias in aliases.items():
    gas.add_species_alias(name, alias)

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1,
                               figsize=(6, 8),
                               )

for spc in aliases.values():
    ax1.plot(states.t, states(spc).Y,
             marker='^',
             label='-Cantera',
             markevery=50)
data = pd.read_csv('gas_mass_tr.csv')
for spc in aliases.keys():
    ax1.plot(data['t(s)'],
             data[spc],
             label='-OpenMKM'
            )
ax1.set_xlabel('time [s]')
ax1.set_ylabel(aliases['H2O'] + ' mass fraction')
ax1.legend(loc='best')

aliases = {'H2': 'H$_2$'}
for name, alias in aliases.items():
    gas.add_species_alias(name, alias)
for spc in aliases.values():
    ax2.plot(states.t, states(spc).Y,
             marker='^',
             label='-Cantera',
             markevery=50)
for spc in aliases.keys():
    ax2.plot(data['t(s)'],
                 data[spc],
                 label='-OpenMKM'
                 )
ax2.set_xlabel('time [s]')
ax2.set_ylabel(aliases['H2'] + ' mass fraction')
ax2.legend(loc='best')
plt.tight_layout()
plt.savefig("Fig1.png")

