import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#########
# Plot OpenMKM mole-fraction vs. time
#########
data = pd.read_csv('gas_mole_tr.csv')
sns.lineplot(data['t(s)'], data['react1'], label='react1')
sns.lineplot(data['t(s)'], data['react2'], label='react2')
sns.lineplot(data['t(s)'], data['prod'], label='prod')
sns.lineplot(data['t(s)'], data['int1'], label='int1')
sns.lineplot(data['t(s)'], data['int2'], label='int2')
sns.lineplot(data['t(s)'], data['int3'], label='int3')
sns.lineplot(data['t(s)'], data['cat'], label='cat')
plt.xscale('log')
plt.ylabel("mole-fraction")
plt.xlabel("time (s) in log-scale")
plt.legend()
plt.savefig('OpenMKM.png', dpi=600)

#########
# Plot COPASI concentration (mol/L) vs. time
#########

data = pd.read_csv('copasi_conc.txt', delimiter='\t')
data['t(s)'] = data['# Time']
plt.figure()
sns.lineplot(data['t(s)'], data['react1'], label='react1')
sns.lineplot(data['t(s)'], data['react2'], label='react2')
sns.lineplot(data['t(s)'], data['prod'], label='prod')
sns.lineplot(data['t(s)'], data['INT1'], label='int1')
sns.lineplot(data['t(s)'], data['INT2'], label='int2')
sns.lineplot(data['t(s)'], data['INT3'], label='int3')
sns.lineplot(data['t(s)'], data['cat'], label='cat')
plt.xscale('log')
plt.ylabel("Conc. (mol/L)")
plt.xlabel("time (s) in log-scale")
plt.legend()
plt.savefig('Copasi.png', dpi=600)

#########
# Plot COPASI norm. conc. vs. time
#########
df = pd.read_csv('copasi_conc.txt', delimiter='\t')
cols = ['cat', 'INT2', 'INT1', 'react2', 'react1', 'INT3', 'prod']
data = df[cols].div(df[cols].sum(axis=1), axis=0)
data['t(s)'] = df['# Time']
plt.figure()
sns.lineplot(data['t(s)'], data['react1'], label='react1')
sns.lineplot(data['t(s)'], data['react2'], label='react2')
sns.lineplot(data['t(s)'], data['prod'], label='prod')
sns.lineplot(data['t(s)'], data['INT1'], label='int1')
sns.lineplot(data['t(s)'], data['INT2'], label='int2')
sns.lineplot(data['t(s)'], data['INT3'], label='int3')
sns.lineplot(data['t(s)'], data['cat'], label='cat')
plt.xscale('log')
plt.ylabel("Normalized Concentration (no units)")
plt.xlabel("time (s) in log-scale")
plt.legend()
plt.savefig('Copasi_norm.png', dpi=600)