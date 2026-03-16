'''
1 converting R output to the data possible to apply Jacardy

    Convert 'SDG-11|SDG-09|SDG-08'
    into {11, 9, 8}

2 calculate
3 ???
4 PROFIT
'''
import pandas as pd
import numpy as np
import itertools
import os
import csv
from statistics import mean
import matplotlib.pyplot as plt

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/coherence testing/_results+sdgm/'

output_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/coherence testing/_results-sdgm/'

## assemble the evaluation results of different files in one file

# set the object containing the properties of the data folder
folder_object = os.scandir(data_folder)

# make an empty list of all files
filenames = []
unit_names = []

filename_ending = '+.csv'

# scan the folder and get a list of preprocessed output files
for file in folder_object:
    if file.is_file() and filename_ending in file.name:
        filenames.append(file.name)

    # make a list of files for each unit
    # it is finance, but it could've been anything else
    # if file.is_file() and 'csv' in file.name:
    #     unit_name = file.name.split('_')[0].replace('finance','')
    #     unit_names.append(unit_name)

# free the ressources
folder_object.close()

## define
# convert strings in the csv file
def parse_sdg_string(s):
    parts = s.split("|")
    return {int(p.replace("SDG-", "")) for p in parts}

# Jaccard similarity metric
def jaccard(a, b):
    return len(a & b) / len(a | b)

# set names of the methods skipping the word 'translation'
method_names = ['SIRIS', 'Aurora', 'Auckland', 'Elsevier', 'SDGM']

# set translation names
translation_names = ['finance', 'ip', 'gen', 'court', 'formal']

# empty strings to put in a df and to plot afterwards
method_all_scores = []
method_flat_scores = []
best_method_all = []

translation_all_scores = []
translation_flat_scores = []
best_translation_all = []

#todo
'''
monaris finance dl the translation
put scores inside squares
fix boxes
convert to txt and try to reevaluate
'''

## process
for file in [filenames[3]]:

    df = pd.read_csv(data_folder + file, sep=';')

    # convert the string to a set
    for col in method_names:
        df[col] = df[col].apply(parse_sdg_string)

    data = df[method_names].values.tolist()

    # methods
    # for each method j test every translation i
    n_translations = len(data)
    n_methods = len(data[0])

    method_scores = []

    # calculate method coherence scores
    for j in range(n_methods):
        sets = [data[i][j] for i in range(n_translations)]

        similarities = []

        for a, b in itertools.combinations(sets, 2):
            similarities.append(jaccard(a, b))

        method_scores.append(mean(similarities))

    best_method = int(np.argmax(method_scores))

    # add to the final df to plot
    # append or extend? it depends
    method_flat_scores.extend(method_scores)
    method_all_scores.append(method_scores)
    best_method_all.append(method_names[best_method])

    # caulculate translation coherence scores
    translation_scores = []

    # for each translation i test every method
    for i in range(n_translations):
        sets = data[i]

        similarities = []
        for a, b in itertools.combinations(sets, 2):
            similarities.append(jaccard(a, b))

        translation_scores.append(mean(similarities))

    best_translation = int(np.argmax(translation_scores))

    # add to the final df to plot
    # append or extend? it depends
    translation_flat_scores.extend(translation_scores)
    translation_all_scores.append(translation_scores)
    best_translation_all.append(translation_names[best_translation])

## create dataframes
# method_best_df = pd.DataFrame()
# method_best_df['best translation'] = best_translation_all
# method_best_df['best method'] = best_method_all
# #

## plotting
# heatmap
# make arrays
T = np.array(translation_all_scores)
M = np.array(method_all_scores)

# the background layer of the heatmap
heatmap_matrix = np.zeros((M.shape[1], T.shape[1]))

# for each method, and for each translation
for i in range(M.shape[1]):
    for j in range(T.shape[1]):
        combined = M[:, i] + T[:, j]
        heatmap_matrix[i, j] = combined.sum()

# # plot a heatmap
fig, ax = plt.subplots(figsize=(4, 4))

im = ax.imshow(heatmap_matrix)

method_names = ["SIRIS", "Aurora", "Auckland", "Elsevier","SDGM"]
translation_names = ["finance", "ip", "gen", "court", "formal"]

ax.set_xticks(np.arange(len(translation_names)))
ax.set_yticks(np.arange(len(method_names)))

ax.set_xticklabels(translation_names)
ax.set_yticklabels(method_names)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# Add numbers inside squares
for i in range(heatmap_matrix.shape[0]):
    for j in range(heatmap_matrix.shape[1]):
        value = heatmap_matrix[i, j]

        # choose white or black text depending on background
        text_color = "white" if value > 0.5 else "black"

        ax.text(j, i,
                f"{value:.2f}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=9)

ax.set_title("Total Coherence Score per \n Method–Translation Pair")

plt.savefig(output_folder + 'figure_coherence_table.svg')
plt.tight_layout()
plt.show()

# # plot a distribution
fig, ax = plt.subplots(figsize=(4, 4))

        # scatter
        # translations on 1
ax.scatter([1 for i in range(len(translation_flat_scores))],
        translation_flat_scores, alpha=0.7)
        # on 2
ax.scatter([2 for i in range(len(method_flat_scores))],
            method_flat_scores, alpha=0.7)

# overlay with a box
plt.boxplot(
    [method_flat_scores, translation_flat_scores],
    tick_labels=["Methods", "Translations"],
    positions=[2, 1],
            )

plt.ylabel("Coherence Score")
plt.ylim(0, 1)

plt.title("Distribution of Coherence Scores")

plt.savefig(output_folder + 'figure_coherence_scores.svg')

plt.tight_layout()
plt.show()