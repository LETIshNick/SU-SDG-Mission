'''
Hello, I've got a pandas dataframe and I'd like to make a scatter plot using matplotlib only. The column 'pub_count' contains values on the X axis. The values on the Y axis are found in the found in the column 'oa_goals', it's the number of items in each cell separated by a vertical bar |. Would you mind to help me on that?

I'd like to make two adjustments, first, i'd like to make a figure smaller, like 4x4 maximum. Second, I'd like to calculate a correlation coefficient, write its value in the bottow right corner, and draw the corresponding line alongside the points.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

out_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

type = 'UMR'

# create the dataframe
unitSDG = pd.read_csv(data_folder + f'{type}_description.csv', sep=';',
                        na_values='fail')

unitSDG = unitSDG.dropna(subset=['oa_goals'])

# compute the number of goals per row
unitSDG['oa_goal_count'] = unitSDG['oa_goals'].str.split('|').apply(len)

# compute correlation (Pearson's r)
x = unitSDG['pub_count']
y = unitSDG['oa_goal_count']
r = np.corrcoef(x, y)[0, 1]

# compute p
r, p = pearsonr(x, y)


# fit regression line
m, b = np.polyfit(x, y, 1)  # slope and intercept

# scatter plot
fig, ax = plt.subplots(figsize=(3.2, 3))

ax.scatter(
    unitSDG['pub_count'],
    unitSDG['oa_goal_count'],
    alpha=0.7,
    color='teal',
    edgecolor='k'
)

# regression line
ax.plot(x, m*x + b, color='black', linewidth=1.5, linestyle='--')

# annotate correlation in bottom-right corner
ax.text(
    0.95, 0.05,
    f"r = {r:.2f}\np = {p:.2e}",
    transform=ax.transAxes,
    ha='right', va='bottom',
    fontsize=10
)

plt.yticks([2*i for i in range(9)])

ax.set_xlabel('Publication Count')
ax.set_ylabel('Number of OA Goals')
# ax.set_title('OA Goals vs Publication Count')
plt.ylim(0,18)

plt.tight_layout()
# plt.show()
output_path = out_data_folder + f'figure_sdg.svg'
plt.savefig(output_path, format='svg')
