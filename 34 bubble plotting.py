'''
Hello. I have data in a csv file with a semicolon as a separator. In the column 'SDG_description' I have the data I need to plot on a 2d plane using matplotlib.

The data in the 'SDG_description' column are additionnally subdivided as follows. 'first SDG:x coordinate:y coordinate|second SDG:x coordinate:y coordinate' and so on.

For example, 'SDG03:100.0:96.67|SDG04:100.0:90.0|SDG08:100.0:90.0|SDG09:50.0:83.33|SDG10:50.0:75.0'. That is, the SDG03 has the x coordinate of 100.0 and the y coordinate of 96.67

So I need to generate the code that will allow me to plot bubbles labelled and coloured according to their SDG number (see below). Could you help me with that?

The colour palette in R G B is as follows.
SDG01 R 229 G 36 B 59
SDG02 R 221 G 166 B 58
SDG03 R 76 G 159 B 56
SDG04 R 197 G 25 B 45
SDG05 R 255 G 58 B 33
SDG06 R 38 G 189 B 226
SDG07 R 252 G 195 B 11
SDG08 R 162 G 25 B 66
SDG09 R 253 G 105 B 37
SDG10 R 221 G 19 B 103
SDG11 R 253 G 157 B 36
SDG12 R 191 G 139 B 46
SDG13 R 63 G 126 B 68
SDG14 R 10 G 151 B 217
SDG15 R 86 G 192 B 43
SDG16 R 0 G 104 B 157
SDG17 R 25 G 72 B 106

SDG names are as follows
SDG01 No poverty
SDG02 Zero hunger
SDG03 Good health and well-being
SDG04 Quality education
SDG05 Gender equality
SDG06 Clean water and sanitation
SDG07 Affordable and clean energy
SDG08 Decent work and economic growth
SDG09 Industry, innovation and infrastructure
SDG10 Reduced inequalities
SDG11 Sustainable cities and communities
SDG12 Responsible consumption & production
SDG13 Climate action
SDG14 Life below water
SDG15 Life on land
SDG16 Feace, justice and strong institutions
SDG17 Partnerships for the goals

As for coordinates, the maximum value of x is 100, while the minimum is 33.
The maximum value of y is 100, while the minimum is 50.


'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

    ## 0 Import the data
# data source
data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/'

out_data_folder = '/Users/nikolaicheplagin/Documents/Sociologie/Doctorat/_mission expertise/quality indicators/plots/'

type = 'UMR'

# create the dataframe
unitSDG = pd.read_csv(data_folder + f'{type}_description.csv', sep=';',
                        na_values='no common SDGs found')

unitSDG = unitSDG.dropna(subset=['SDG_list'])

# set the colours
# R, G, B to 0-1 scale for matplotlib
sdg_colors = {
    'SDG01': (229/255, 36/255, 59/255),
    'SDG02': (221/255, 166/255, 58/255),
    'SDG03': (76/255, 159/255, 56/255),
    'SDG04': (197/255, 25/255, 45/255),
    'SDG05': (255/255, 58/255, 33/255),
    'SDG06': (38/255, 189/255, 226/255),
    'SDG07': (252/255, 195/255, 11/255),
    'SDG08': (162/255, 25/255, 66/255),
    'SDG09': (253/255, 105/255, 37/255),
    'SDG10': (221/255, 19/255, 103/255),
    'SDG11': (253/255, 157/255, 36/255),
    'SDG12': (191/255, 139/255, 46/255),
    'SDG13': (63/255, 126/255, 68/255),
    'SDG14': (10/255, 151/255, 217/255),
    'SDG15': (86/255, 192/255, 43/255),
    'SDG16': (0/255, 104/255, 157/255),
    'SDG17': (25/255, 72/255, 106/255)
}

# Define SDG names
# sdg_names = {
#     'SDG01': 'No poverty', 'SDG02': 'Zero hunger',
#     'SDG03': 'Good health and well-being',
#     'SDG04': 'Quality education', 'SDG05': 'Gender equality',
#     'SDG06': 'Clean water and sanitation',
#     'SDG07': 'Affordable and clean energy',
#     'SDG08': 'Decent work and economic growth',
#     'SDG09': 'Industry, innovation and infrastructure',
#     'SDG10': 'Reduced inequalities',
#     'SDG11': 'Sustainable cities and communities',
#     'SDG12': 'Responsible consumption & production',
#     'SDG13': 'Climate action', 'SDG14': 'Life below water',
#     'SDG15': 'Life on land',
#     'SDG16': 'Peace, justice and strong institutions',
#     'SDG17': 'Partnerships for the goals'
# }

sdg_names = {
    'SDG01': '', 'SDG02': '',
    'SDG03': '',
    'SDG04': '', 'SDG05': '',
    'SDG06': '',
    'SDG07': '',
    'SDG08': '',
    'SDG09': '',
    'SDG10': '',
    'SDG11': '',
    'SDG12': '',
    'SDG13': '', 'SDG14': '',
    'SDG15': '',
    'SDG16': '',
    'SDG17': '',
}

# Initialize lists for SDG data
sdg_labels, x_coords, y_coords, colors = [], [], [], []

## Plot en masse (composed by chatGPT)
# Iterate over each row to create separate plots
for index, unit in unitSDG.iterrows():
    sdg_labels, x_coords, y_coords, colors, sizes = [], [], [], [], []
    seen_x, seen_y = {}, {}

    # set a plot title
    title = unit['unit_name']
    code  = unit['acronym']

    # Split multiple SDGs
    items = unit['SDG_description'].split('|')

    for item in items:
        sdg, x, y = item.split(':')
        x, y = float(x), float(y)

        # Offset bubbles if they share the same X or Y coordinate
        if x in seen_x:
            x += np.random.uniform(-25, 1)
        if y in seen_y:
            y += np.random.uniform(-5, 5)
        seen_x[x] = True
        seen_y[y] = True

        x_coords.append(x)
        y_coords.append(y)
        sdg_labels.append(sdg)
        # Default to black if SDG not found
        colors.append(sdg_colors.get(sdg, (0, 0, 0)))
        # Scale bubble size based on mean value and enlarge by factor of 10
        sizes.append(((x + y) / 2) * 5 * 10)

    # Plot data
    plt.figure(figsize=(6, 6))
    plt.scatter(x_coords, y_coords,
                c=colors, s=sizes, alpha=0.7, edgecolors='black')

    # Add labels outside each bubble
    for sdg, x, y in zip(sdg_labels, x_coords, y_coords):
        plt.text(x, y + 5, sdg_names.get(sdg, sdg),
                fontsize=10, ha='center', va='bottom',
                color=sdg_colors.get(sdg, sdg),
                # color = 'black',
                weight='bold')
        plt.text(x, y, sdg, fontsize=8, ha='center',
                 weight='extra bold', va='center',
                 color=sdg_colors.get(sdg, sdg))

    # Customize plot
    plt.xlabel('Confidence')
    plt.ylabel('Likelihood')
    plt.title(f'{title}')
    # plt.grid(True, linestyle='--', alpha=0.6)

    # Remove grid
    plt.grid(False)

# Adjust x-axis ticks for three methods
    # plt.xticks([33.3,66.6], ['33,3', '66,6'])
    plt.xticks([33.3,66.6], ['', ''])
    plt.xticks([16.3,50,76.3], ['Low', 'Medium','High'])
    plt.axvline(x=33.3, color='grey', linestyle='dashed')
    plt.axvline(x=66.6, color='grey', linestyle='dashed')

    # Adjust x-axis ticks for three methods
    plt.yticks([0,20,40,60,80,100], ['0','20','40','60','80','100'])
    plt.axhline(y=0, color='grey', linestyle='dashed')
    plt.axhline(y=100, color='grey', linestyle='dashed')

    # Adjust axis limits to accommodate larger bubbles
    plt.xlim(min(x_coords) - 20, max(x_coords) + 20)
    plt.ylim(min(y_coords) - 20, max(y_coords) + 20)

    # Save the figure as an SVG file
    output_path = out_data_folder + f'{code}_plot_{index}.svg'
    plt.savefig(output_path, format='svg')
    plt.close()