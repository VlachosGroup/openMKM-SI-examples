import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data_FIM = pd.read_csv('FIM/1d_pfr_sensitivity.dat',
                       sep='\t',
                       )
data_NSC = pd.read_csv('LSA/1d_pfr_sensitivity.dat',
                       sep='\t',
                       usecols=['CH2CH2', 'CH4'],
                      )
data_FIM.pop('Rxnid')
data_FIM['FIM-Diag.'] = data_FIM['FIM-Diag.']/np.abs(data_FIM['FIM-Diag.']).max()
data_reac = pd.read_csv('reactions.out',
                        usecols=['Reaction ID'])
react_names = data_reac['Reaction ID'].values.T


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,8), sharex=True)
ax1.barh(range(len(data_FIM)), data_FIM['FIM-Diag.'].values.T, label='FIM Diagonal')
ax1.set_xlabel('Normalized FIM Diagonal')

ax2.barh(np.arange(len(data_NSC)), data_NSC['CH4'].values.T,
         label='NSC - CH$_4$')
ax2.barh(np.arange(len(data_NSC)),
         data_NSC['CH2CH2'].values.T,
         left=list(data_NSC['CH4'].values.T),
         label='NSC - C$_2$H$_4$')
ax2.set_xlabel('Normalized LSA Co-efficients')

ax1.yaxis.tick_right()
ax1.set_yticks(np.arange(0,len(data_FIM)))
ax1.set_yticklabels(react_names)
ax2.set_yticks(np.arange(0,len(data_NSC)))
# ax2.set_yticklabels(np.arange(1,len(data_NSC)+1))
plt.setp(ax2.get_yticklabels(), visible=False)

ax1.legend(loc='best')
ax2.legend(loc='best')

ax1.grid(axis='y', zorder=0)
ax2.grid(axis='y', zorder=0)
# ax2.tick_params(length=30)
fig.subplots_adjust(wspace=2.0, hspace=0)
plt.tight_layout()
plt.savefig("Fig3.png")
plt.show()
