'''
THIS COMES SECOND, I.E. AFTER LIKELIHOOD
'''
import pandas as pd
import numpy as np

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

output_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

# set data type among various units
type = 'UMR'

# create the dataframe
unitSDG = pd.read_csv(data_folder + f'{type}_likelihood.csv', sep=';')

# replace nan by fail
# unitSDG = unitSDG.dropna(subset=['oa_goals']).reset_index()
unitSDG = unitSDG.fillna('fail')

## Confidence

# empty lists to fill in in each unit
# 1. the column that contains SDGs
SDG_common = []

# 2. the column that contains confidence
SDG_confidence = []

# 3. the column that contains likelihood
SDG_likelihood = []

# 4. the column that contains a neat string
SDG_descriptive = []

# create all SDG list to compare what's found or not by each method
every_SDG_list = ['SDG0'+f'{i}' for i in list(range(10))[1:]] +\
                 ['SDG' +f'{i}' for i in list(range(18))[-8:]]

#test
# unit = 0

# make a dataset that contain the evaluation results
SDG_qualities = pd.DataFrame({'SDG_list'        : [],
                              'SDG_confidence'  : [],
                              'SDG_likelihood'  : [],
                              'SDG_description' : []})

# cycle through each unit
for unit in range(len(unitSDG)):

# create the lists of SDG and its likelihoods to compare
    # for Aukland
    list_auk      = unitSDG['Auk_goals'     ][unit].split('|')
    list_auk_like = unitSDG['Auk_likelihood'][unit].split('|')

    # for SDG Mapper
    list_sdgm      = unitSDG['SDG_mapper_goals'][unit].split('|')
    list_sdgm_like = unitSDG['SDGM_likelihood' ][unit].split('|')

    # for OA
    list_oa      = unitSDG['oa_goals'     ][unit].split('|')
    list_oa_like = unitSDG['oa_likelihood'][unit].split('|')

    # the empty list of SDGs (1st for sorting, 2nd for storage)
    SDG_common_list = []
    SDG_common_str  = ''
    # the one with confidence
    SDG_confidence_list = []
    SDG_confidence_str  = ''
    # and the one with quality factors
    SDG_likelihood_list = []
    SDG_likelihood_str  = ''
    # and the one with quality factors
    SDG_description_str  = ''

    for SDG in every_SDG_list:
        # set confidence to zero
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
            likelihood_auk = float(list_auk_like[position_auk])

            # increase confidence
            confidence += 50.0

        # zero helps to assign the greater likelihood
        else:
            likelihood_auk = 0

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

            # get its likelihood
            likelihood_sdgm = float(list_sdgm_like[position_sdgm])

            # increase confidence
            confidence += 50.0

        else:
            likelihood_sdgm = 0

        if confidence != 0:
            SDG_confidence_list.append(confidence)
            SDG_likelihood_list.append(max(likelihood_auk,
                                           likelihood_sdgm))

        # need to sort the list according to its likelihood
        # Zip the lists together
        SDG_zipped = list(zip(SDG_common_list,
                            SDG_confidence_list,
                            SDG_likelihood_list))

        # Sort the zipped list by the likelihood in descending order
        SDG_zipped.sort(key=lambda x: x[2], reverse=True)

        # Unzip them back into separate lists
        SDG_common_sorted, SDG_confidence_sorted, SDG_likelihood_sorted = zip(*SDG_zipped)

        # Convert tuples to lists
        SDG_common     = list(SDG_common_sorted)
        SDG_confidence = list(SDG_confidence_sorted)
        SDG_likelihood = list(SDG_likelihood_sorted)

    # make strings in order  to fill in the dataframe
    for i in range(len(SDG_common)):
        SDG_common_str = SDG_common_str + SDG_common[i] + '|'
        SDG_confidence_str = SDG_confidence_str + str(SDG_confidence[i]) \
                                                + '|'
        SDG_likelihood_str = SDG_likelihood_str + str(SDG_likelihood[i]) \
                                                + '|'

        # make the description string at the same time
        SDG_description_str = SDG_description_str                \
                    +           SDG_common[i]         + ':' \
                    + str(round(SDG_confidence[i],2)) + ':' \
                    + str(round(SDG_likelihood[i],2)) + '|'

    # remove the last unnecessary separator
    SDG_common_str = SDG_common_str[:-1]
    SDG_confidence_str = SDG_confidence_str[:-1]
    SDG_likelihood_str = SDG_likelihood_str[:-1]
    SDG_description_str = SDG_description_str[:-1]

    # make the data frame from all this in order to
    # contatenate it with the table of resuults
    SDG_qualities_unit = pd.DataFrame(
                            {'SDG_list' :        [SDG_common_str],
                             'SDG_confidence' :  [SDG_confidence_str],
                             'SDG_likelihood' :  [SDG_likelihood_str],
                             'SDG_description' : [SDG_description_str]})

    SDG_qualities = pd.concat([SDG_qualities, SDG_qualities_unit], ignore_index=True)

    # add the result to the initial DF
unitSDG = pd.concat([unitSDG,SDG_qualities], axis=1)

    ## Export the output
unitSDG.to_csv(output_folder + f'{type}_description.csv', sep=';', index = False)
