import os
from siac import *
from ndvi import *
from ndci import *
from b8ab4 import *
from b3b2 import *
from anamoly import *

# Specify the directory path containing the datasets(TIF files)
origin_path = r'C:\\Users\\Agilan B\\fyp\\Algal-bloom\\template\\'
dataset_path = r'datasets\\'
siac_output_path = r'output\\siac_output'
ndvi_output_path = r'output\\ndvi_output'
ndci_output_path = r'output\\ndci_output'
b8ab4_output_path = r'output\\b8ab4_output'
b3b2_output_path = r'output\\b3b2_output'
siac_data = origin_path+siac_output_path+'\\'
ndvi_output_data = origin_path+ndvi_output_path+'\\ndvi'
ndci_output_data = origin_path+ndci_output_path+'\\ndci'
b8ab4_output_data = origin_path+b8ab4_output_path+'\\b8ab4'
b3b2_output_data = origin_path+b3b2_output_path+'\\b3b2'

anamoly = 'C:\\Users\\Agilan B\\fyp\\Algal-bloom\\template\\output\\anamoly_output\\'
combined_anamoly = 'C:\\Users\\Agilan B\\fyp\\Algal-bloom\\template\\output\\anamoly_output\\combined_anamoly\\'

# Use os.listdir() to get a list of all files in the directory
files = os.listdir(origin_path+dataset_path)

# for outputing siac data
for file in files:
    siac_calculation(origin_path,
                 file,
                 dataset_path,
                 siac_output_path
                 )

    
#for outputing ndvi images
files = os.listdir(origin_path+siac_output_path)

# for outputing siac data
for file in files:
    ndvi_calculation(siac_data, file, ndvi_output_data)
    ndci_calculation(siac_data, file, ndci_output_data)
    b8ab4_calculation(siac_data, file, b8ab4_output_data)
    b3b2_calculation(siac_data, file, b3b2_output_data)

files = os.listdir(origin_path+dataset_path)

# for outputing anamoly corrected data
for file in files:
    anamoly_calculation(
        ndvi_output_data+'_output_image_',
        ndci_output_data+'_output_image_',
        b8ab4_output_data+'_output_image_',
        b3b2_output_data+'_output_image_',
        file,
        anamoly,
        combined_anamoly
    )

