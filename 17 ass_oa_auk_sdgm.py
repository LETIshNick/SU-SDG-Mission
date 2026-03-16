## TABLE OF CONTENTS
'''
The file is used to assemble all the evaluation results so far.
First, the pure OA + OA using HAL DOIs with the info about UFRs
Second, these fuller evaluation results with Aukland and SDG mapper
The Aukland results had been assembled using a script 22 auk_eval.py
whereas SDG mapper ones were matched by hand.

'''

import pandas as pd
import csv
import os

# data source
output_data = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

# info folder
input_data ='/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/data by type/PUBLICATIONS/'

## import files
# import labs supplementary biblio info
info_UFR = pd.read_csv(input_data + 'src_units_pub_info.csv', sep=';')

# import the combined OA analysis
SDGs_oa = pd.read_csv(input_data + 'res_oa_combined.csv', sep=';')

# import Aukland and SDG mapper
SDGs_UMR_sdgm_auk = pd.read_csv(output_data + 'src_hand_sdgm&auk.csv', sep=';')

    ## merge full OA with UFR info
# merge oa info and side info
SDGs_UMR_oa = pd.merge(SDGs_oa, info_UFR,
                             how='right', on='oa_id')

# export to visually check the file
# SDGs_UFR_oa.to_csv(output_data + 'res_temp_umr_oa.csv', sep=';', index = False)

    ## merge SDG mapper and Aukland to OA
# on column 'unit_id'
'''
Sanity checks: all units has unit_id, not everyone has oa_id
all units except for MOSAIC has OA SDGs found
'''
# SDGs_UMR_all = pd.merge(SDGs_UMR_sdgm_auk, SDGs_UMR_oa,
#                              how='right', on='unit_id')
#
# # export to visually check the file
# SDGs_UMR_all.to_csv(output_data + f'res_umr_all&info.csv', sep=';', index = False)


    ## update method
SDGs_UMR_all = SDGs_UMR_sdgm_auk.set_index('unit_id').combine_first(
               SDGs_UMR_oa.set_index('unit_id')).reset_index()

# put columns in order
new_order = ['unit_id','acronym','unit_code','unit_name','faculty','ROR',
             'oa_id','oa_url','oa_work_count','hal_structId_i',
             'hal_work_count','doc_name','doc type and lang',
             'Auk_goals','Auk_scores','Auk_Q','SDG_mapper_goals',
             'SDG_mapper_scores','SDG_mapper_counts','oa_goals','oa_scores',
             'oa_q','pub_count','comment','Auk_succes?','SDG_m_success?',
             'oa_success?','hal_url']

SDGs_UMR_all = SDGs_UMR_all[new_order]

# export to visually check the file
SDGs_UMR_all.to_csv(output_data + f'res_umr_all&info.csv', sep=';', index = False)

