## TABLE OF CONTENTS
'''
1. This fail assembles the best scrapping results from both OA and HAL
Then can copy by hand in the oa raw data folder by replacing
So the oa data folder is 'oa_data_combined'
'''

#todo don't forget to manually cope the output data into the raw oa data
#todo this is intentional
import numpy as np
import pandas as pd
import csv
import os

# data sources

## set data types and data folders

hal_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_rawdata_haldoi/'

data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

output_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_oaid_by_haldoi/'

# create the file for adding the results
oaid_doi_table = pd.read_csv(data_folder + 'temp_doi_2fill_in.csv', sep=';')

# # import ufr info with oaids

## 1 assemble the outputs of oa obtained by scrapping DOIs
# 1 create the list of HAL extracted files
# set up an object containing the properties of the data folder

folder_object_doi = os.scandir(hal_data_folder)

# make empty lists
filenames_haldoi = []

# scan the OA raw data folder and get a list of output files
for file in folder_object_doi:
    if file.is_file() and 'csv' in file.name:
        filenames_haldoi.append(file.name)

# free the ressources
folder_object_doi.close()

# create an empty dataframe
oa_haldoi = pd.DataFrame({'paper_id'  : [], 'sdg_id' : [],
                          'sdg_score' : [], 'doi'    : []})

types = {'paper_id': str, 'sdg_id': str, 'sdg_score': float}

# add the evaluation results together
for file in filenames_haldoi:
    oa_temp_haldoi = pd.read_csv(hal_data_folder + f'{file}', sep=';',
                                dtype = types)
    oa_haldoi = pd.concat([oa_haldoi, oa_temp_haldoi])

oa_haldoi.drop_duplicates(subset=['doi'])

## make the output the same as for standard oa scragging
'''
this makes it like a number of files with I****_paper2sdg.csv
Then the data scrapped normally will be evaluated using one script
'''

# merge the df containing Ws, sdg and doi with the one containg Is and doi
oa_haldoi_inst = pd.merge(oa_haldoi, oaid_doi_table, how='left', on='doi')

# loop for each oa_id and export
oaid_list = oa_haldoi_inst['oa_id'].drop_duplicates().tolist()

# for each institution name
for oaid in oaid_list:

    inst_paper2sdg = oa_haldoi_inst.loc[oa_haldoi_inst['oa_id'] == oaid,
['paper_id', 'sdg_id', 'sdg_score']]

    # export
    inst_paper2sdg.to_csv(output_folder + f'{oaid}_paper2sdg.csv',
                          sep=';', index = False)




