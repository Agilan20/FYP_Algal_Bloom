import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
from rasterio.plot import show
from matplotlib import pyplot as plt 

# Function to perform atmospheric correction
def atmospheric_correction(image_data):
    scale_factor = 1.2
    
    corrected_data = image_data * scale_factor
    
    return corrected_data

def siac_calculation(path, input, datasets, outputDir):
    try:
        input_image = os.path.join(path, datasets, input)
        output_dir = os.path.join(path, outputDir)
        output_image = os.path.join(output_dir, 'siac_output_image_' + input)
        os.makedirs(output_dir, exist_ok=True)

        with rasterio.open(input_image) as src:
            profile = src.profile
            image_data = src.read()
            corrected_data = np.zeros_like(image_data)
            for band_idx in range(src.count):
                corrected_data[band_idx] = atmospheric_correction(image_data[band_idx])

        with rasterio.open(output_image, 'w', **profile) as dst:
            dst.write(corrected_data)

        print("Atmospheric correction completed. Output image saved as", output_image)
    except Exception as e:
        print(f"An error occurred: {e}")
