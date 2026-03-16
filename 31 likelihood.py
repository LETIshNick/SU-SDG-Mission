'''
THIS COMES FIRST, I.E. BEFORE CONFIDENCE
'''

import pandas as pd
import numpy as np

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

output_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

source_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/_results/'

# set data type among various units
type = 'UMR'

# create the dataframe
# unitSDG = pd.read_csv(data_folder + f'{type}',
#                        dtype = types, sep=';')

# import ufr info
unitSDG = pd.read_csv(source_folder + 'res_umr_all&info.csv', sep=';')

# replace nan by fail
unitSDG = unitSDG.fillna('fail')

    ## Calculate the likelihood

    ## SDG mapper

# the empty list of strings of all units
likelihood_list_sdgm = []

# cycle through each unit
for unit in range(len(unitSDG)):

    # the empty string of each unit
    unit_likelihood_string = ''

    # set to zero if there's no data (afterwards the found ones are >0)
    if unitSDG['SDG_mapper_counts'][unit] in ('fail', 'nodoc', 'comment'):
        likelihood_list_sdgm.append('0')
    else:

        # for each count cycle through each goal and fill in the likelihood
        for count in unitSDG['SDG_mapper_counts'][unit].split('|'):

            # Preal = 100 - Prand
            sdg_likelihood = 100 - 100/float(count)

            # add the likelihood to the list plus the separator
            unit_likelihood_string = unit_likelihood_string +\
                                     str(sdg_likelihood) + '|'

        # remove the last unnecessary separator
        unit_likelihood_string = unit_likelihood_string[:-1]

        # add to the list of strings which will go into the dataset
        likelihood_list_sdgm.append(unit_likelihood_string)

# make the dataframe with all the likelihoods
likelihood_column = pd.DataFrame({'SDGM_likelihood' : likelihood_list_sdgm},index = range(len(likelihood_list_sdgm)))

# merge the likelihood dataframe with the initial one
unitSDG_sdgm = pd.concat([unitSDG,likelihood_column], axis=1)

    ## Aukland
'''
in this method we have to first reestablish counts
Q is the count of least occuring goal
so if an item with Q=x has a score=y
its count per score is y/x
so, if the biggest score is z, it has z*y/x occurences
'''
# the empty list of strings of all units
likelihood_list_auk = []

# cycle through each unit
for unit in range(len(unitSDG)):

    # set to zero if there's no data (afterwards the found ones are >0)
    if unitSDG['Auk_scores'][unit] in ('fail', 'nodoc', 'comment'):
        likelihood_list_auk.append('0')
    else:

        # the empty string of each unit
        unit_likelihood_string = ''

        # for each sdg cycle through each goal
        # to first restore its count and then cauculate its likelihood
        for score in unitSDG['Auk_scores'][unit].split('|'):

            # the least score is
            least = float(unitSDG['Auk_scores'][unit].split('|')[-1])

            # count, and round it
            count = float(score)*float(unitSDG['Auk_Q'][unit])/least
            count = round(count,0)

            # Preal = 100 - Prand
            sdg_likelihood = 100 - 100/count

            # add the likelihood to the list plus the separator
            unit_likelihood_string = unit_likelihood_string +\
                                     str(sdg_likelihood) + '|'

        # remove the last unnecessary separator
        unit_likelihood_string = unit_likelihood_string[:-1]

        # add to the list of strings which will go into the dataset
        likelihood_list_auk.append(unit_likelihood_string)

# make the dataframe with all the likelihoods
likelihood_column = pd.DataFrame({'Auk_likelihood' : likelihood_list_auk},index = range(len(likelihood_list_auk)))

# merge the likelihood dataframe with the initial one
unitSDG_sdgm_auk = pd.concat([unitSDG_sdgm,likelihood_column], axis=1)

    ## OA
'''
the same method as with Auk because there are Q instead of counts
'''
# the empty list of strings of all units
likelihood_list_oa = []

# cycle through each unit
for unit in range(len(unitSDG)):

    # set to zero if there's no data (afterwards the found ones are >0)
    if unitSDG['oa_goals'][unit] == 'fail':
        likelihood_list_oa.append('0')
    else:

        # the empty string of each unit
        unit_likelihood_string = ''

        # for each sdg cycle through each goal
        # to first restore its count and then cauculate its likelihood
        for score in unitSDG['oa_scores'][unit].split('|'):

            # the least score is
            least = float(unitSDG['oa_scores'][unit].split('|')[-1])

            # count, and round it
            count = float(score)*float(unitSDG['oa_q'][unit])/least
            count = round(count,0)

            # Preal = 100 - Prand
            sdg_likelihood = 100 - 100/count

            # add the likelihood to the list plus the separator
            unit_likelihood_string = unit_likelihood_string +\
                                     str(sdg_likelihood) + '|'

        # remove the last unnecessary separator
        unit_likelihood_string = unit_likelihood_string[:-1]

        # add to the list of strings which will go into the dataset
        likelihood_list_oa.append(unit_likelihood_string)

# make the dataframe with all the likelihoods
likelihood_column_oa = pd.DataFrame({'oa_likelihood' : likelihood_list_oa},
                       index = range(len(likelihood_list_oa)))

# merge the likelihood dataframe with the initial one
unitSDG_all = pd.concat([unitSDG_sdgm_auk,likelihood_column_oa], axis=1)

    ## Export the output
unitSDG_all.to_csv(output_folder + f'{type}_likelihood.csv', sep=';', index = False)
