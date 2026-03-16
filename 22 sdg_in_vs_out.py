'''

'''

import pandas as pd
import csv
import os

## import data files

# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

# import UFRs with sorted inside SDGs
SDGs_umr = pd.read_csv(data_folder + 'temp_umr_sdgs_inside.csv', sep=';')

## compare SDGs on their places
# create empty lists to fill in in each unit
in_out_match_list = []

# create the resulting df
in_out_match = pd.DataFrame({'in_out_match' : []})

# compose a list of failed rows
# for openalex goals
failed_out = SDGs_umr['unit_id'][SDGs_umr['oa_goals'].isna() ==
                      True].tolist()
# for text mining goals
failed_in  = SDGs_umr['unit_id'][SDGs_umr['SDG_list'] ==
                      'fail'].tolist()
# combine the list
failed_units  = failed_out + failed_in

# cycle through each unit
for unit in range(len(SDGs_umr)):

    # if there are no documents or no publications
    if SDGs_umr['unit_id'][unit] in failed_units:
        common_share = 'fail'
        # add to the list
        in_out_match_list.append(common_share)
    else:
        # create the lists of SDG and its likelihoods to compare
        # for inside SDGs
        list_inside  = SDGs_umr['SDG_list'][unit].split('|')

        # for outside SDGs
        list_outside = SDGs_umr['oa_goals'][unit].split('|')

        # make a list of common items whatever their position
        # knowing there are no dupplicates
        common = set(list_inside) & set(list_outside)

        # the total number of unique SDGs found by both
        # total = set(list_inside) | set(list_outside)
        total = set(list_inside).union(set(list_outside))

        # calculate the share
        common_share = len(common)/len(total)

        # add to the list
        in_out_match_list.append(common_share)

    SDGs_match_per_unit = pd.DataFrame({
                        'in_out_match' : in_out_match_list})

    # add the result to the initial DF
SDGs_umr = pd.concat([SDGs_umr,SDGs_match_per_unit], axis=1)

    # export to visual check the result
SDGs_umr.to_csv(data_folder + f'temp_umr_io_match.csv', sep=';', index = False)

## plot with different variables

import matplotlib.pyplot as plt

# drop rows where there's a failure
SDGs_umr_good = SDGs_umr[SDGs_umr['in_out_match'] != 'fail']

# drop with unknown faculties
SDGs_umr_good = SDGs_umr_good[SDGs_umr_good['faculty'].isna() == False]

## written with chatGPT

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

df = SDGs_umr_good.copy()

# Clean the language column: "HCERES|EN" -> "EN", "HCERES|FR" -> "FR"
lang_col = 'doc type and lang'
df[lang_col] = df[lang_col].str.replace(r'^HCERES\|', '', regex=True)

# Map faculties to numeric values for the X-axis
faculties = df['faculty'].unique()
fac_map = {fac: i for i, fac in enumerate(faculties)}

fig, ax = plt.subplots(figsize=(4, 4))

# Scatter points: faculty on X, in_out_match on Y
colors = {"EN": "blue", "FR": "red"}
for lang, sub in df.groupby('doc type and lang'):
    ax.scatter(
        sub['faculty'].map(fac_map),
        sub['in_out_match'],
        label=lang,
        color=colors.get(lang, "gray"),
        alpha=0.7
    )

# --- overlay boxplots ---
# Make sure faculties are in the same order as on the scatter's X-axis
faculties = list(fac_map.values())

# Prepare data for each faculty
data = [df.loc[df['faculty'] == fac, 'in_out_match'] for fac in fac_map.keys()]

# Overlay boxplot (narrower width, semi-transparent)
ax.boxplot(
    data,
    positions=faculties,
    widths=0.5,
    patch_artist=True,
    boxprops=dict(facecolor='none', color='black'),
    medianprops=dict(color='black', linewidth=1.2),
    whiskerprops=dict(color='black'),
    capprops=dict(color='black'),
)

# # Circles per faculty (mean ± std on Y)
# for fac, sub in df.groupby('faculty'):
#     mean_y = sub['in_out_match'].mean()
#     std_y  = sub['in_out_match'].std(ddof=1)
#     if not np.isfinite(std_y) or std_y == 0:
#         std_y = 0.03  # small visible radius
#     x_val = fac_map[fac]
#
#     # print values
#     print(mean_y, std_y)
#
#     # Draw circle
#     ax.add_patch(Circle((x_val, mean_y), std_y, fill=False, lw=2, color='0.3', alpha=0.9))

    # Add "+" marker at the center
    # ax.scatter(x_val, mean_y, marker='+', color='black', s=100, lw=2, zorder=3)

# Tidy up axes
ax.set_xticks(list(fac_map.values()))
ax.set_xticklabels(list(fac_map.keys()))
# ax.set_ylabel("in_out_match")
# ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.1))

plt.tight_layout()

plt.savefig(data_folder + 'figure_1.svg')

# plt.show()


