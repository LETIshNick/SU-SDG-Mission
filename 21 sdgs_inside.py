'''
This file takes as input the assembled evaluation results and then calculates
inside goals

'''

import pandas as pd
import csv
import os

## import data files

# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

# import UMRs
SDGs_umr = pd.read_csv(data_folder + 'res_umr_all&info.csv', sep=';')

## use rather confidence-like algo
# create all SDG list to compare what's found or not by
# each method
SDGs_list17 = ['SDG0'+f'{i}' for i in list(range(10))[1:]] +\
               ['SDG'+f'{i}' for i in list(range(18))[-8:]]

# create empty lists to fill in in each unit
# 1. the column that contains SDGs
SDG_common = []

# 2. the column that contains scores (used to sort the SDGs)
SDG_confidence = []

# create the resulting df
SDGs_inside = pd.DataFrame({'SDG_list' : [], 'SDG_scores' : []})

# cycle through each unit
for unit in range(len(SDGs_umr)):

# create the lists of SDG and its likelihoods to compare
    # for Aukland
    list_auk        = SDGs_umr['Auk_goals' ][unit].split('|')
    list_auk_scores = SDGs_umr['Auk_scores'][unit].split('|')

    # for SDG Mapper
    list_sdgm        = SDGs_umr['SDG_mapper_goals' ][unit].split('|')
    list_sdgm_scores = SDGs_umr['SDG_mapper_scores'][unit].split('|')

    # the empty lists of SDGs (1st for sorting, 2nd for storage)
    SDG_common_list = []
    SDG_common_str  = ''
    # the one with the scores (the same logic for 1, 2)
    SDG_scores_list = []
    SDG_scores_str  = ''

    for SDG in SDGs_list17:
        # set confidence to zero. While seemingly useless, it helps
        # compose a single list of the SDGs found by two methods
        confidence = 0

        # There's no need to check if the method succeded.
        # because if there's anything other than SDGx, it'll be false anyway.
        # check if found by Aukland
        if SDG in list_auk:

            # if so, add to the list
            SDG_common_list.append(SDG)

            # find the place of the element in the list
            position_auk = list_auk.index(SDG)

            # get its likelihood
            score_auk = float(list_auk_scores[position_auk])

            # increase confidence
            confidence += 50.0

        # zero helps to assign a greater score
        else:
            score_auk = 0

        #
        # check if the same goal is found by SDG Mapper
        if SDG in list_sdgm:

            # if confidence is zero, this item wasn't found by Auk
            # so, if it's not zero, it shouldn't be added = pass
            if confidence != 0:
                pass
            else:
                # if confidence is zero,
                #therefore it should be added to the array.
                SDG_common_list.append(SDG)

            # find the place of the element in the list
            position_sdgm = list_sdgm.index(SDG)

            # get its score
            score_sdgm = float(list_sdgm_scores[position_sdgm])

            # increase confidence,
            # so it becomes 100 if both methods found a goal
            confidence += 50.0

        else:
            score_sdgm = 0

        if confidence != 0:
            # SDG_confidence_list.append(confidence)
            SDG_scores_list.append(max(score_auk, score_sdgm))

    if SDG_common_list != []:
        # sort the list according to its score
        # zip the lists together
        SDG_zipped = list(zip(SDG_common_list, SDG_scores_list))

        # sort the zipped list by the score in descending order
        SDG_zipped.sort(key=lambda x: x[1], reverse=True)

        # unzip them back into separate lists
        SDG_common_sorted, SDG_scores_sorted = zip(*SDG_zipped)

        # convert tuples to lists
        SDG_common = list(SDG_common_sorted)
        SDG_scores = list(SDG_scores_sorted)

        # make strings in order to fill in the dataframe
        for i in range(len(SDG_common)):
            SDG_common_str = SDG_common_str + SDG_common[i] + '|'
            SDG_scores_str = SDG_scores_str + str(SDG_scores[i]) + '|'

        # remove the last unnecessary separator
        SDG_common_str = SDG_common_str[:-1]
        SDG_scores_str = SDG_scores_str[:-1]
        # USELESS

        # make the data frame from all this in order to
        # contatenate it with the table of resuults
        SDGs_inside_unit = pd.DataFrame(
                                {'SDG_list'   : [SDG_common_str],
                                 'SDG_scores' : [SDG_scores_str]})
    else:
        SDGs_inside_unit = pd.DataFrame(
                                {'SDG_list'   : ['fail'],
                                 'SDG_scores' : ['fail']})

    SDGs_inside = pd.concat([SDGs_inside, SDGs_inside_unit],
                                ignore_index=True)


    # add the result to the initial DF
SDGs_umr = pd.concat([SDGs_umr,SDGs_inside], axis=1)

    # export to visually check the result
SDGs_umr.to_csv(data_folder + f'temp_umr_sdgs_inside.csv',
                sep=';', index = False)





