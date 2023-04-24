import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('gas_mole_tr.csv')

sns.lineplot(data['t(s)']/60.0, data['Fructose-1'], label='Fructose')
sns.lineplot(data['t(s)']/60.0, data['HMF-9'], label='HMF')
sns.lineplot(data['t(s)']/60.0, data['LA-FA'], label='LA+FA')
plt.legend()
plt.xlabel('time (min)')
plt.ylabel('Mole Fraction (no unit)')
plt.legend(loc='best', frameon=True)
plt.savefig('OpenMKM-plot-no-Marcus.png', dpi=300)
plt.show()