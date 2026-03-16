'''
This file compares the number of DOIs indexed in HAL with those found in
OpenAlex and exports a list of oaids to scrap
'''
import requests
import io
import pandas as pd
import json
import os
import csv

# working folders
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

hal_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/hal_rawdata_halid/'

oa_data_folder  = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/oa_rawdata_oaid/'

# import unit info
UFR = pd.read_csv(data_folder + 'src_units_pub_info.csv', sep=';')

institution_list = UFR['oa_id'].dropna().tolist()

oa_filename  = '_paper2sdg.csv'
hal_filename = '_hal_doi.txt'

    ## create the lists of extracted files
# set an object containing the properties of the data folder
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

# create two lists
oa_id_scr_oa = [filenames_oa[i].split('_paper2sdg.csv')[0]
                            for i in range(len(filenames_oa))]

oa_id_scr_hal = [filenames_hal[i].split('_hal_doi.txt')[0]
                            for i in range(len(filenames_hal))]

    ## open each file and see what's inside
# create a list of units for which No of HAL pub is superior to those of OA
hal_more_oa = []
# create, in passing, a list containing a total No of pub
work_count = []

for entry in range(len(filenames_hal)):

    # if there's a file open the corresponding file
    # normally all oa files exist
    try:
        oa_raw_file = pd.read_csv(oa_data_folder + oa_id_scr_hal[entry] +
                                  oa_filename, sep=';')
        # get the number of non-empty strings in each file
        # easy for oa
        oa_work_count = oa_raw_file.shape[0]
        # print(f'OA file found {UFR["unit_id"][entry]}:{institution_list[entry]} with {oa_work_count} works')

    except pd.errors.EmptyDataError:
        # file is empty
        oa_work_count = 0

    except FileNotFoundError:
        oa_work_count = 0

    # they are never empty because the first line is doi_s
    hal_raw_file = pd.read_csv(hal_data_folder + filenames_hal[entry]
                                   , sep=';')
        # drop empty dois for hal
    hal_work_count = hal_raw_file.dropna().shape[0]
    # print(f'HAL file found {UFR["unit_id"][entry]}:{institution_list[entry]} with {hal_work_count} works')

if hal_work_count > oa_work_count:
    print('hal has more works than oa')
    # append to the list to scrap
    hal_more_oa.append(filenames_hal[entry])
    # append to the list to count
    work_count.append(hal_work_count)
else:
    work_count.append(oa_work_count)

# already done
# # make a df work count vs unity
# work_count_df['unit_id']

# export
export_df = pd.DataFrame(hal_more_oa)
export_df.to_csv(data_folder + 'temp_oaid_to_hal_more_workcount.csv', sep=';', index = False)

