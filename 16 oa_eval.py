import io
import pandas as pd
import json
import os
import csv

'''
This file evaluates oa
'''

# data sources
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_data_combined/'

output_data = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

    ## 1 Import the list
# 1 scan the folder for evaluated units
# set an object containing the properties of the data folder
folder_object = os.scandir(data_folder)

# make an empty list
filenames = []

# scan the folder and get a list of preprocessed output files
for file in folder_object:
    if file.is_file() and 'paper2sdg.csv' in file.name:
        filenames.append(file.name.split('_')[0])

# free ressources
folder_object.close()

# create an assessment data frame that will be merged later
oa_units = pd.DataFrame({'oa_id'     : [], 'oa_goals' : [],
                         'oa_scores' : [], 'oa_q'     : []})

## Option 1: merge the outputs to a single dataframe
## But without a threshold
'''
for each unit in the list calculate the sdg scores
and then export to the csv file
'''
for unit in filenames:
    # read a document from the list
    unitSDG = pd.read_csv(data_folder + unit + '_paper2sdg.csv', sep=';')

    # if no SDG have been found, put that into the output file
    # in the form: SDG;score;Q;
    if unitSDG.shape[0] == 0:
        sdgs ='nan'
        sdg_score = 'nan'
        sdg_q = 'nan'
    else:
        # make a list of SDGs
        # first, a normal one, second a normalized one
        # and make dataframes at the same step
        sdg_list      = unitSDG['sdg_id'].value_counts().rename_axis(
                            ['sdg_id']).reset_index(name='share')
        sdg_list_norm = unitSDG['sdg_id'].value_counts(
                            normalize=True).rename_axis(['sdg_id']).reset_index(
                                name='normalized share')

        # make a counnter
        sdg_norm_share = sdg_list_norm.shape[0]

        # add sdgs to the string
        sdgs = ''
        for sdg in range(sdg_norm_share):
            goal = sdg_list_norm['sdg_id'][sdg]
            if goal < 10:
                sdgs = sdgs + 'SDG' + f'0{goal}' + '|'
            else:
                sdgs = sdgs + 'SDG' + f'{goal}' + '|'

        # remove the last unnecessary | sign
        sdgs = sdgs[:-1]

        # add corresponging sdg scores as a normalized value
        sdg_scores = ''
        for sdg in range(sdg_norm_share):
            score = sdg_list_norm['normalized share'][sdg]
            sdg_scores = sdg_scores + f'{score:.4f}' + '|'

        # remove the last unnecessary | sign
        sdg_scores = sdg_scores[:-1]

        # add the least sdg occurrence as a quality factor
        sdg_q = f"{sdg_list['share'][sdg_norm_share-1]}"

    # make an adhoc dataframe
    sdg_unit_df = pd.DataFrame({'oa_id' : [unit], 'oa_goals' : [sdgs],
                                'oa_scores' : [sdg_scores],
                                'oa_q' : [sdg_q],
                                'pub_count':[unitSDG['sdg_id'].shape[0]]})

    # merge in with the assessment frame
    oa_units = pd.concat([oa_units, sdg_unit_df])

# export the result
oa_units.to_csv(output_data + 'res_oa_combined.csv', sep=';', index = False)

