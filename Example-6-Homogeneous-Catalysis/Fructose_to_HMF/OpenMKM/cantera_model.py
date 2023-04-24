import cantera as ct


liquid = ct.Solution('thermo.yaml')
# liquid.X = {'H2O': 1.0}
# liquid.TP = 463.15, 20132500.0
liquid.TP = 463.15, 101325.0
liquid.X = {'H2O': 52.7330,
            'Fructose-1': 0.2775,
            'H-BA': 0.01584}
print(liquid.density)
print(liquid.TDX)
print(liquid.concentrations, liquid.partial_molar_volumes, liquid.activity_coefficients)

batch = ct.Reactor(liquid)
print(batch.T, batch.volume, batch.density, batch.Y, batch.mass)

sim = ct.ReactorNet([batch])
sim.verbose = True

dt_max = 1.0
t_end = 300 * dt_max
states = ct.SolutionArray(liquid, extra=['t'])

print('{:10s} {:10s} {:10s}'.format(
    't [s]', 'T [K]', 'Density'))
while sim.time < t_end:
    sim.advance(sim.time + dt_max)
    states.append(batch.thermo.state, t=sim.time)
    # print('{:10.3e} {:10.3f} {:10.3f}'.format(
    #         sim.time, batch.T, batch.thermo.density))

# Plot the results if matplotlib is installed.
import matplotlib.pyplot as plt
plt.clf()
plt.subplot(2, 2, 1)
plt.plot(states.t, states.T)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')
plt.subplot(2, 2, 2)
# plt.plot(states.t, states.concentrations[:, liquid.species_index('Fructose-1')])
plt.plot(states.t, states.Y[:, liquid.species_index('Fructose-1')]*(1000/180.16))
plt.xlabel('Time (s)')
plt.ylabel('Fruc Mole Fraction')
plt.subplot(2, 2, 3)
plt.plot(states.t, states.Y[:, liquid.species_index('HMF-9')]*(1000/126.11))
plt.xlabel('Time (s)')
plt.ylabel('HMF Mole Fraction')
plt.subplot(2, 2, 4)
plt.plot(states.t, states.Y[:, liquid.species_index('LA-FA')]*(1000/126.11))
plt.xlabel('Time (s)')
plt.ylabel('LA Mole Fraction')
plt.tight_layout()
plt.show()