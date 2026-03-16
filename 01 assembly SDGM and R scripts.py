## TABLE OF CONTENTS
'''
todo
- import my R_aukland
- import flavia's SDG_mapper
- import my OA
- figure out how to merge them
'''

import pandas as pd
import csv
import os

## assemble the evaluations of different files in one file

## 1 importing Flavia's results as a dataframe

# data source
data_folder = '/Users/nikolaicheplagin/Documents/Doctorat/_mission expertise/_results/'

# make an empty list
filenames = []

# read a file
results_Flavia = pd.read_excel(data_folder + 'outputs_SDG_mapper_online.xlsx', sheet_name='HCERES_en')
'''
the other sheets are  'HCERES previusly lacking' 'Formations' 'UFR' 'USM' 'ED'
'''
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
sdg_aukland = sdg_aukland + f"{sdg_list['share'][share5percent-1]}" + ';'


## calculate en masse

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


## assemble the outputs

# choose what to analyse: ED, FORMATIONS, PUBLICATIONS, UFR, USM
types = ['ED', 'FORMATIONS', 'UFR', 'HCERES', 'USM'] #

# set an output folder
data_output = '/Users/nikolaicheplagin/Documents/Doctorat/_mission expertise/data by type/'

# set the data folder, starting from ED, then make a big dataframe
data_folder = '/Users/nikolaicheplagin/Documents/Doctorat/_mission expertise/data by type/' + types[0] + '/_output/'

# create the first dataframe to put others into
totalSDG = pd.read_csv(data_folder + '_SDG_per_unit.csv', sep=';')

# take every other type of unit, and add to the totalSDG df
for type in types[1:]:
    data_folder = '/Users/nikolaicheplagin/Documents/Doctorat/_mission expertise/data by type/' + type + '/_output/'
    pd_to_merge = pd.read_csv(data_folder + '_SDG_per_unit.csv', sep=';')
    totalSDG = pd.merge(totalSDG, pd_to_merge, how='outer')

# write the data
totalSDG.to_csv(data_output + 'export.csv', sep=';', index = False)