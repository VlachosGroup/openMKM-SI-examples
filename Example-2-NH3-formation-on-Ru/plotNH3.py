import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_yes = pd.read_csv('lateral-yes/surf_cov_ss.csv',
                       index_col=False,
                       usecols=['N(T)', 'H(T)', 'RU(T)', 'N(S)', 'H(S)', 'RU(S)'])
data_no = pd.read_csv('lateral-no/surf_cov_ss.csv',
                      index_col=False,
                      usecols=['N(T)', 'H(T)', 'RU(T)', 'N(S)', 'H(S)', 'RU(S)']
                      )
df = pd.DataFrame(
    {'With Lateral-Interaction': data_yes.loc[1].values,
     'Without Lateral-Interactions': data_no.loc[1].values},
    index=data_yes.columns
)
print(df)
ax = df.plot.bar(rot=0)
ax.set_xlabel('Surface Species')
ax.set_ylabel('Fractional Coverage')
plt.tight_layout()
plt.legend(loc='best')
plt.savefig("Fig1.png")
# plt.show()
plt.figure()

data_yes = pd.read_csv('lateral-yes/surf_cov_tr.csv',
                       index_col=False,
                       usecols=['t(s)', 'RU(T)', 'RU(S)'])
data_yes = pd.DataFrame([[0.0, 1.0, 1.0]],
                        columns=data_yes.columns).append(data_yes)
data_yes.reset_index(inplace=True, drop=True)
data_no = pd.read_csv('lateral-no/surf_cov_tr.csv',
                      index_col=False,
                      usecols=['t(s)', 'RU(T)', 'RU(S)']
                      )
data_no = pd.DataFrame([[0.0, 1.0, 1.0]],
                       columns=data_no.columns).append(data_no)
data_no.reset_index(inplace=True, drop=True)

print(data_no, data_yes)
plt.plot(data_yes['t(s)'],
         data_yes['RU(S)'],
         marker='o',
         label='With Interaction - Ru(S)',
         markevery=5,
         )
plt.plot(data_yes['t(s)'],
         data_yes['RU(T)'],
         marker='v',
         label='With Interaction - Ru(T)',
         markevery=5,
         )
plt.plot(data_no['t(s)'],
         data_no['RU(S)'],
         marker='s',
         label='Without Interaction - Ru(S)',
         markevery=5,
         )
plt.plot(data_no['t(s)'],
         data_no['RU(T)'],
         marker='x',
         label='Without Interaction - Ru(T)',
         markevery=5,
         )
plt.legend(loc='best')
plt.xlabel('time(s)')
plt.ylabel('Fractional Surface Coverage')
plt.tight_layout()
plt.savefig('Fig2.png')
