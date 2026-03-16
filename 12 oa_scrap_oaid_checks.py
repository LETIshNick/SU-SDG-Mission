import io
import pandas as pd
import json
import os
import csv

'''
This file compares the hal raw scrapped data by halid
with the oa raw scraped data by oaid with the list of units

Afterwards, it's possible to manually scrap missing units
and then check the results here

I4210103770 has a 2nd oaid I4210155524
'''

# data sources
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

hal_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/hal_rawdata_halid/'

oa_data_folder  = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_rawdata_oaid/'

    ## 0 Prepare the list of institutions for the OA scrapper
UFR = pd.read_csv(data_folder + 'src_units_pub_info.csv', sep=';')

institution_list = UFR['oa_id'].dropna()

# export
institution_list.to_csv(data_folder + 'temp_oa_inst_list2scrap.csv',
                        sep=';', index = False)

    ## 1 check the scrapper's results
# 1 create the list of HAL extracted files
# set up an object containing the properties of the data folder
folder_object_hal = os.scandir(hal_data_folder)
folder_object_oa =  os.scandir(oa_data_folder)

# make empty lists
filenames_hal = []
filenames_oa =  []

# scan the HAL raw data folder and get a list of output files
for file in folder_object_hal:
    if file.is_file() and 'txt' in file.name:
        filenames_hal.append(file.name)

# scan the OA raw data folder and get a list of output files
for file in folder_object_oa:
    if file.is_file() and 'csv' in file.name:
        filenames_oa.append(file.name)

# free the ressources
folder_object_hal.close()
folder_object_oa.close()

# compare whether the list of files correspond and show the ones which dosent'
# create two lists
oa_id_scr_oa = [filenames_oa[i].split('_paper2sdg.csv')[0]
                            for i in range(len(filenames_oa))]

oa_id_scr_hal = [filenames_hal[i].split('_hal_doi.txt')[0]
                            for i in range(len(filenames_hal))]

# make sets of items that don't correspond
lost_by_hal = set(institution_list) - set(oa_id_scr_hal)
lost_by_oa  = set(institution_list) - set(oa_id_scr_oa)
lost_both   = set(oa_id_scr_oa) - set(oa_id_scr_hal)
