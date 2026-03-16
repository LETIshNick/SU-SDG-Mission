'''

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

# create the dataframe
unitSDG = pd.read_csv(data_folder + f'temp_umr_io_match.csv', sep=';',
                        na_values='fail')

# unitSDG = unitSDG.dropna(subset=['oa_goals'])
unitSDG = unitSDG.dropna(subset=['in_out_match'])

# compute correlation (Pearson's r)
x = unitSDG['pub_count']
y = unitSDG['in_out_match']
r = np.corrcoef(x, y)[0, 1]

# compute p
r, p = pearsonr(x, y)

# fit regression line
m, b = np.polyfit(x, y, 1)  # slope and intercept

# scatter plot
fig, ax = plt.subplots(figsize=(3.2, 3))

ax.scatter(
    unitSDG['pub_count'],
    unitSDG['in_out_match'],
    alpha=0.7,
    color='grey',
    edgecolor='k'
)

# regression line
ax.plot(x, m*x + b, color='black', linewidth=1.5, linestyle='--')

# annotate correlation in bottom-right corner
ax.text(
    0.95, 0.05,
    f"r = {r:.2f}\np = {p:.2f}",
    transform=ax.transAxes,
    ha='right', va='bottom',
    fontsize=10
)

# plt.xticks([10*i for i in range(10)])

ax.set_xlabel('Publication Count')
ax.set_ylabel('Internal vs External SDG\nCorrespondend Ratio')
# ax.set_title('OA Goals vs Publication Count')
plt.ylim(0,0.8)

plt.tight_layout()
# plt.show()
output_path = data_folder + f'figure_io.svg'
plt.savefig(output_path, format='svg')

