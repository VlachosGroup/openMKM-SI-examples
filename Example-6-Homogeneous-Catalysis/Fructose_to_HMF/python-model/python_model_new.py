# -*- coding: utf-8 -*-

'''
'''
import time
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.integrate import odeint, ode
from scipy.integrate import solve_ivp
t = time.time()


# %%-------------------------------------------------------------------------
# Reactor functions
def Reactor(**conditions):
    '''
    Reactor model under certain temperature, pH and residence time tf
    '''
    T_degC = conditions['T_degC']  # reaction temperature in C
    pH = conditions['pH']  # reaction pH
    tf = conditions['tf']  # Final time point [s]
    t0 = 0  # Initial time point [s]
    Fru0 = 0.3  # Normalized initial fructose concentration (always equal to 1)
    C_Hplus = 10 ** (-pH)  # H+ concentraction [mol/L]
    T = T_degC + 273
    C_H2O = 47.522423477254065 + 0.06931572301966918 * T - 0.00014440077466393135 * (T ** 2)  # Water
    print("H+ {} and H2O {} in mol/L".format(C_Hplus, C_H2O))
    
    atom_wt = [12.011, 1.008, 15.999] # C, H, O
    species_list = ['Fructose-1',
                    'Inter-2',
                    'Inter-3',
                    'Inter-4',
                    'Inter-5',
                    'Inter-6',
                    'Inter-7',
                    'Inter-8',
                    'HMF-9',
                    'H2O',
                    'H+',
                    'LA+FA'
                    ]
    C0 = np.zeros(len(species_list))
    C0[0] = Fru0  # Fructose
    C0[-3] = C_H2O
    C0[-2] = C_Hplus


    def PFR(t, C, T_degC, pH):
        '''
        #The "PFR" function describes the species conservative equation as a
        #set of ODEs at T
        '''
        # CONSTANTS
        # R = 8.314  # Ideal gas law constant [J/mol-K]
        R = 1.98720  # Ideal gas law constant [cal/mol-K]
        kb = 3.297623483E-24  # Boltzman constant [cal/K]
        h = 6.62607009e-34/4.184  # Plancks constant [cal-S]

        # OTHER MODEL PARAMETERS
        T = T_degC + 273.15  # reaction temperarure in K

        # concentration as a function of temperature from 25 °C to 300 °C
        # [mol/L]
        # ACTIVATIONS ENERGIES FOR RXN1,RXN2,...,RXN8
        Ea = np.array([9.195, 12.569, 6.74, 20.43,
                       9.31, 10.21, 3.348, 12.51]) * (10 ** 3)  # [cal/mol]

        A0 = np.ones(8) * (kb*T)/(2*np.pi*h)
        k = np.zeros(8)
        for i in range(len(k)):
            k[i] = A0[i] * np.exp(-Ea[i]/(R*T))
        kr = np.zeros(8)
        Eab = np.array([8.54, 19.42, 0.04, 9.15, 43.90, 0.0, 44.38, 12.80]) * (10 ** 3)
        for i in range(len(kr)):
            kr[i] = A0[i] * np.exp(-Eab[i]/(R*T))
        C_H2O = C[9]
        C_Hplus = C[10]
        # RXN RATES FOR THE RXN NETWORK OF FRUCTOSE DEHYDRATION
        Rxn = np.zeros(9)
        Rxn[0] = k[0] * C[0] * C_Hplus - kr[0] * C[1]
        Rxn[1] = k[1] * C[1] - kr[1] * C[2] * C_H2O
        Rxn[2] = k[2] * C[2] - kr[2] * C[3]
        Rxn[3] = k[3] * C[3] - kr[3] * C[4]
        Rxn[4] = k[4] * C[4] - kr[4] * C[5] * C_H2O
        Rxn[5] = k[5] * C[5] - kr[5] * C[6]
        Rxn[6] = k[6] * C[6] - kr[6] * C[7] * C_H2O
        Rxn[7] = k[7] * C[7] - kr[7] * C[8] * C_Hplus
        Rxn[8] = 9.37e8 * np.exp(-23260 / (R * T)) * C[8]  # HMF to LA

        # SPECIES CONSERVATIVE EQUATIONS
        # Notation: rhs = dC/dt
        rhs = np.zeros(len(C))  # [mol/L-min]
        rhs[0] = (-Rxn[0])  # Fructose-1
        rhs[1] = (Rxn[0] - Rxn[1])  # 2
        rhs[2] = (Rxn[1] - Rxn[2])  # 3
        rhs[3] = (Rxn[2] - Rxn[3])  # 4
        rhs[4] = (Rxn[3] - Rxn[4])  # 5
        rhs[5] = (Rxn[4] - Rxn[5])  # 6
        rhs[6] = (Rxn[5] - Rxn[6])  # 7
        rhs[7] = (Rxn[6] - Rxn[7])  # 8
        rhs[8] = (Rxn[7] - Rxn[8])  # HMF-9
        rhs[9] = (-Rxn[1] - Rxn[4] - Rxn[6])  # H2O
        rhs[10] = (-Rxn[0] + Rxn[7])  # H+
        rhs[11] = (Rxn[8])  #LA+FA
        return rhs
    # %% SOLVING FOR THE PFR MODEL at certain temperature T_K  
    # Construct the ode solver, ode45 with varying step size
    sol = []
    sol = solve_ivp(PFR, t_span=(t0, tf), y0=C0, method='LSODA',
                    args=(T_degC, pH))
    # RESULTS
    return sol['t'], sol['y']


# %%------------------------------------------------------------------------
# INPUT PARAMETERS: n_T, pH, Tmin_degC, Tmax_degC, tmin, tmax, Fru0
pH = 1.8  # Rxn pH
t0 = 0  # Initial time point [s]
tf = 300  # Final time point[s]
# Tmin_degC = 100  # %Min rxn temperature [°C]
# Tmax_degC = 200  # %Max rxn temperature [°C]
n_T = 1;  # Number of temperature points
# VARIABLE REACTION PARAMETERS
# T_degC = np.linspace(Tmin_degC, Tmax_degC, n_T)  # Rxn temperature [°C]
T_degC = [210.0]
# -------------------------------------------------------------------------
# Run the reactor model and collect data at each temperature
Tau = []
Conc = []
HMF_Select = []
HMF_Yield = []
LA_Yield = []
FA_Yield = []
Opt_Cond = []

for Ti in T_degC:
    Conditions = {'T_degC': Ti, 'pH': pH, 'tf': tf}
    Tau_i, Conc_i = Reactor(**Conditions)
    Tau.append(Tau_i)
    Conc.append(Conc_i)

# %% Plotting Section
# Set the parameters for plotting
font = {'size': 12}

matplotlib.rc('font', **font)
matplotlib.rcParams['axes.linewidth'] = 1.2
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 1.2
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 1.2

Conc[0] = Conc[0]/np.sum(Conc[0],axis=0)
fig = plt.figure(figsize=(8, 6))
for i in range(n_T):
    plt.plot(Tau[i]/60.0, Conc[0][0], label='Fructose')
for i in range(n_T):
    plt.plot(Tau[i]/60.0, Conc[0][8], label='HMF')
for i in range(n_T):
    plt.plot(Tau[i]/60.0, Conc[0][-1], label='LA+FA')
plt.xlabel('time (min)')
plt.ylabel('Conc. normalized (no units)')
plt.legend(loc='best', frameon=True)
plt.savefig('Python-plot-no-Marcus.png', dpi=300)
plt.show()