'''
'''
import pandas as pd
import numpy as np
import os
import csv
from statistics import mean

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/coherence testing/_results/'

output_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/coherence testing/_results_formatted/'

# create the dataframe
# filename = data_folder + 'CAC.csv'
# testSDG = pd.read_csv(data_folder + 'CAC.csv', sep=';')

## assemble the evaluation results of different files in one file

# set the object containing the properties of the data folder
folder_object = os.scandir(data_folder)

# make an empty list of all files
filenames = []
unit_names = []

filename_ending = '_EN_outputR.csv'

# scan the folder and get a list of preprocessed output files
for file in folder_object:
    if file.is_file() and filename_ending in file.name:
        filenames.append(file.name)

    # make a list of files for each unit
    # it is finance, but it could've been anything else
    if file.is_file() and 'finance' in file.name:
        unit_name = file.name.split('_')[0].replace('finance','')
        unit_names.append(unit_name)

# free the ressources
folder_object.close()

## calculate one by one from R outputs

# create necessary empty objecs

processed_units = []

translation_list = ['finance', 'ip', 'gen', 'court', 'formal']
method_list = ['SIRIS', 'Aurora', 'Auckland', 'Elsevier']

# iterate over unit names
for unit in unit_names:

    # create an empty csv file
    with open(output_folder + unit + '.csv', 'w', newline='') as csvfile:

        # open a file, write a title row
        writer = csv.writer(csvfile, delimiter ='\t', quoting=csv.QUOTE_NONE)
        writer.writerow(['translation;SIRIS;Aurora;Auckland;Elsevier;SDGM'])

        # iterate over translation options
        for translation in translation_list:

            # create an empty string containing sdgs for each method
            methods_each_translation = ''

            # read the document for each translation option
            output_r = pd.read_csv(data_folder + unit +
                                translation + filename_ending, sep=',')

            for method in method_list:
                # calculate top 3 SDGs for each method
                method_out = output_r.loc[output_r['system'] == method]
                method_top = method_out['sdg'].value_counts().rename_axis(['sdg']).reset_index(name='share')
                # the top SDG
                method_top1 = f"{method_top.loc[0, 'sdg']}"

                # sometimes there are less than three methods
                # no need to condition and repeat
                # if there are more that one SDG
                if method_top.shape[0] > 1:
                    method_top2 = f"{method_top.loc[1, 'sdg']}"
                else:method_top2 = method_top1

                # if there are more than two SDG
                if method_top.shape[0] > 2:
                    method_top3 = f"{method_top.loc[2, 'sdg']}"
                else:method_top3 = method_top2

                method_top3_str = method_top1 + "|" + \
                                  method_top2 + "|" + \
                                  method_top3

                # for each translation write a top 3 row
                methods_each_translation = methods_each_translation + \
                                            method_top3_str + ';'

            # don't need to remove the last unnecessary semicolon
            # because the values coming from SDG mapper will be added afterwards
            translation_row = translation + ';' + methods_each_translation
            writer.writerow([translation_row])
    csvfile.close()
# #
