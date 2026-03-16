import io
import pandas as pd
import json
import os
import csv

'''
This file prepares temporary files for scrapping oa by hal dois for the
institution having more publications on hal that on openalex

However, the file must be processed by hand as there are many instances
of dois missing from openalex. These lines must be removed
'''

# data sources
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

hal_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/hal_rawdata_halid/'

output_folder  = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_rawdata_haldoi/'


# file list with doi to scrap
oaid_filenames = pd.read_csv(data_folder + 'temp_oaid_to_hal_more_workcount.csv',
                             skiprows = 0, sep=';')

# create a common dataframe containing oaid and dois
oaid_doi_table = pd.DataFrame({'oa_id' : [], 'doi' : []})

# create and add one just to see

for file in oaid_filenames['0'].tolist():

    # import the file and drop empty dois ""
    unit_dois = pd.read_csv(hal_data_folder + file, sep=';').dropna()

    # make another column
    # unit_dois = unit_dois.rename_axis(['oa_id']).reset_index()

    # rename to make it correspond
    unit_dois = unit_dois.rename(columns={'doiId_s':'doi'})

    # create a new column
    file_oa_id = file.split('_hal_doi.txt')[0]
    unit_dois['oa_id'] = file_oa_id

    oaid_doi_table = pd.concat([oaid_doi_table, unit_dois])

# export the file for scrapping
doi_list = oaid_doi_table['doi']
doi_list.to_csv(data_folder + 'temp_doi_2scrap.csv', sep=';', index = False)

# export the file for adding the results
oaid_doi_table.to_csv(data_folder + 'temp_doi_2fill_in.csv', sep=';', index = False)


















