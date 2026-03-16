## TABLE OF CONTENTS
'''
1.
2.
3a.
3b.
4.
'''

import pandas as pd
import csv
import os

## set data types and data folders

# choose what to analyse: ED, FORMATIONS, PUBLICATIONS, UFR, USM, HCERES
type = '3 HCERES'

# data source
data_folder = '/Users/nikolaicheplagin/Documents/Doctorat/_mission expertise/data by type/' + type + '/_outputs_R/'

## assemble the evaluation results of different files in one file

# set the object containing the properties of the data folder
folder_object = os.scandir(data_folder)

# make an empty list
filenames = []

# scan the folder and get a list of preprocessed output files
for file in folder_object:
    if file.is_file() and 'output.csv' in file.name:
        filenames.append(file.name)

# free the ressources
folder_object.close()

## calculate one by one from R outputs
# read the document
docSDG = pd.read_csv(data_folder + '102 UMR 8112 LERMA_output.csv', sep=',')

# make a list of SDGs, first normal, second nornalized
# make dataframes at the same step
sdg_list      = docSDG['sdg'].value_counts().rename_axis(['sdg']).reset_index(name='share')
sdg_list_norm = docSDG['sdg'].value_counts(normalize=True).rename_axis(['sdg']).reset_index(name='normalized share')

# detect how many goals have more that 5 % (0.05)
share5percent = sdg_list_norm[sdg_list_norm['normalized share'] > 0.05].shape[0]

# create and empty string
sdg_aukland = ''

# add sdgs > 5% to the string
for sdg in range(share5percent):
    goal = sdg_list['sdg'][sdg]
    sdg_aukland = sdg_aukland + goal + '|'

# remove the last unnecessary | sign, and add a semicolon
sdg_aukland = sdg_aukland[:-1] + ';'

# add corresponging sdg scores
for sdg in range(share5percent):
    score = f"{sdg_list_norm['normalized share'][sdg]:.3f}"
    sdg_aukland = sdg_aukland + score + '|'

# remove the last unnecessary | sign, and add a semicolon
sdg_aukland = sdg_aukland[:-1] + ';'

# add the last sdg occurrence as a quality factor
# one by one can be simle copy-pasted from the terminal
sdg_aukland = sdg_aukland + f"{sdg_list['share'][share5percent-1]}" + ';'

## calculate en masse from R outputs

with open(data_folder + '_SDG_per_unit.csv', 'w', newline='') as csvfile:

    # open a file, write a title row
    writer = csv.writer(csvfile,delimiter ='\t',quoting=csv.QUOTE_NONE)
    writer.writerow(['unité;SDG_Aukland;score_Aukland;Q_Aukland;'])

    # for each unit in the
    for unit in range(len(filenames)):
        # read a document from the list
        unitSDG = pd.read_csv(data_folder + filenames[unit], sep=',')

        # create an empty string containting the name of the unit
        sdg_aukland = f'{filenames[unit]}' + ';'

        # if no SDG have been found, put that into the output file
        if unitSDG.shape[0] == 0:
            sdg_aukland = sdg_aukland + 'nan;' + 'nan;' + 'nan' + ';'
            writer.writerow([sdg_aukland])
        else:
            # make a list of SDGs, first normal, second normalized
            # make dataframes at the same step
            sdg_list      = unitSDG['sdg'].value_counts().rename_axis(['sdg']).reset_index(name='share')
            sdg_list_norm = unitSDG['sdg'].value_counts(normalize=True).rename_axis(['sdg']).reset_index(name='normalized share')

            # detect how many goals have more that 5 % (0.05)
            share5percent = sdg_list_norm[sdg_list_norm['normalized share'] > 0.05].shape[0]

            # the same if I decide to make more proper names
            # sdg_aukland = f'{filenames[unit].split("output")[0]}' + ';'

            # add sdgs > 5% to the string
            for sdg in range(share5percent):
                goal = sdg_list['sdg'][sdg]
                sdg_aukland = sdg_aukland + goal + '|'

            # remove the last unnecessary | sign, and add a semicolon
            sdg_aukland = sdg_aukland[:-1] + ';'

            # add corresponging sdg scores
            for sdg in range(share5percent):
                score = f"{sdg_list_norm['normalized share'][sdg]:.3f}"
                sdg_aukland = sdg_aukland + score + '|'

            # remove the last unnecessary | sign, and add a semicolon
            sdg_aukland = sdg_aukland[:-1] + ';'

            # add the last sdg occurrence as a quality factor
            sdg_aukland = sdg_aukland + f"{sdg_list['share'][share5percent-1]}" + ';'

            # write a row
            writer.writerow([sdg_aukland])
    # end

# free ressources
csvfile.close()
