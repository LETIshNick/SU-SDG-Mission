 import requests
import io
import pandas as pd
import json
import os
# import csv

'''
This script downloads the lists of DOIs from HAL based on HAL ID

Some things need to be rescrapped for no reason, therefore, use
2 oa_scrap_oaid_checks.py
to check the gaps
'''

    ## 0 Import the list

# data source multiple hal ids
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

# import data
UFR = pd.read_csv(data_folder + 'src_units_pub_info.csv', sep=';')

# make a list of HAL ids
hal_id_list = UFR['hal_structId_i'].dropna().tolist()

# manual in case of rescrapping
# hal_id_list = ['28504|542210', '541882', '542017']

    ## 2. Extract the data with necessary fields in bulk

# just row by row without fancy methods
for entry in range(len(hal_id_list)):

    # create an output file
    # acccess OA id of the unit to be put in the file name
    oaid = UFR.loc[UFR['hal_structId_i'] ==
                   hal_id_list[entry],'oa_id'].tolist()[0]

    # name a file
    file = data_folder + f'hal_rawdata_halid/{oaid}_hal_doi.txt' # .0f

    # old version
    # file = data_folder + f'hal_rawdata_halid/{name_list[entry]}.txt' # .0f

    # if HALid is absent, write a file containting nan
    if UFR['hal_structId_i'][entry] == 'nan':
        print(f"unit{entry} don't have a halid")
        response = ''
        with open(file, 'w') as f:
            f.write(response)
        f.close()

    else:
        print(f'{oaid} for unitid={UFR["hal_structId_i"][entry]} found')
        # get each halid if there are many
        multiple_halids = hal_id_list[entry].split('|')

        # download publications for every halid
        for halid in multiple_halids:
            # make an API request for each halid
            request = ('http://api.archives-ouvertes.fr/search/?q=*' +
            '&fq=docType_s:(ART OR COMM OR REPORT)' +
            f'&fq=structId_i:{halid}' +
            '&fq=producedDateY_i:[2017 TO 2022]' +
            '&sort=producedDateY_i asc' +
            # '&fl=structId_i,halId_s,doiId_s,title_s,uri_s,'+
            '&fl=doiId_s'+
            # 'labStructAcronym_s,structAcronym_s' +
            '&rows=8000&wt=csv')

            response = requests.get(request)

            with open(file, 'wb') as f:
                f.write(response.content)
            f.close()

    # close the file
    f.close()

