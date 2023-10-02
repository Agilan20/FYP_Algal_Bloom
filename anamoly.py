import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate standardized anomalies
def calculate_standardized_anomaly(image, baseline_mean, baseline_std):
    anomalies = (image - baseline_mean) / baseline_std
    return anomalies

# Create subplots for visualizing all anomalies
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
axs = axs.ravel()

# Visualize and save anomalies for each index
def visualize_and_save_anomalies(image, anomalies, threshold_positive, threshold_negative, output_filename, title, i):
    # Create masks for positive and negative anomalies
    positive_anomalies = np.where(anomalies > threshold_positive, 1, 0)
    negative_anomalies = np.where(anomalies < threshold_negative, 1, 0)

    # Visualize positive anomalies in green and negative anomalies in red
    axs[i].imshow(positive_anomalies, cmap='Greens', alpha=0.7)
    axs[i].imshow(negative_anomalies, cmap='Reds', alpha=0.7)
    axs[i].set_title(title)

    # Save the anomalies as a new TIFF file
    with rasterio.open(output_filename, 'w', driver='GTiff', width=image.width,
                       height=image.height, count=1, dtype='float32') as dst:
        dst.write(anomalies, 1)
        dst.update_tags(ns='TIFF', description=output_filename)


def anamoly_calculation(ndvi, ndci, b8ab4, b3b2, input, output_path, combined_output_path):
    # Load the TIFF images for NDVI, NDCI, NDBI, and NDWI
    ndvi_image = rasterio.open(ndvi+input)
    ndci_image = rasterio.open(ndci+input)
    ndbi_image = rasterio.open(b8ab4+input)
    ndwi_image = rasterio.open(b3b2+input)

    # Define baseline means and standard deviations for each index (replace with actual values)
    baseline_ndvi_mean = 0.5
    baseline_ndvi_std = 0.1
    baseline_ndci_mean = 0.2
    baseline_ndci_std = 0.05
    baseline_ndbi_mean = 0.1
    baseline_ndbi_std = 0.03
    baseline_ndwi_mean = 0.3
    baseline_ndwi_std = 0.08

    # Calculate standardized anomalies for each index
    ndvi_anomalies = calculate_standardized_anomaly(ndvi_image.read(1), baseline_ndvi_mean, baseline_ndvi_std)
    ndci_anomalies = calculate_standardized_anomaly(ndci_image.read(1), baseline_ndci_mean, baseline_ndci_std)
    ndbi_anomalies = calculate_standardized_anomaly(ndbi_image.read(1), baseline_ndbi_mean, baseline_ndbi_std)
    ndwi_anomalies = calculate_standardized_anomaly(ndwi_image.read(1), baseline_ndwi_mean, baseline_ndwi_std)

    # Define threshold values for anomalies (e.g., +/- 2 standard deviations)
    threshold_positive = 2
    threshold_negative = -2
    # Visualize and save anomalies for each index
    visualize_and_save_anomalies(ndvi_image, ndvi_anomalies, threshold_positive, threshold_negative, output_path+'ndvi\\'+'ndvi_anomalies_'+input, 'NDVI Anomalies', 0)
    visualize_and_save_anomalies(ndci_image, ndci_anomalies, threshold_positive, threshold_negative, output_path+'ndci\\'+'ndci_anomalies_'+input, 'NDCI Anomalies', 1)
    visualize_and_save_anomalies(ndbi_image, ndbi_anomalies, threshold_positive, threshold_negative, output_path+'ndbi\\'+'ndbi_anomalies_'+input, 'NDBI Anomalies', 2)
    visualize_and_save_anomalies(ndwi_image, ndwi_anomalies, threshold_positive, threshold_negative, output_path+'ndwi\\'+'ndwi_anomalies_'+input, 'NDWI Anomalies', 3)

    # Save the combined subplot as a separate file
    new_string = input.replace(".tif", ".png")
    combined_output_path_url = combined_output_path+'combined_anomalies_subplot_'+new_string
    plt.savefig(combined_output_path_url, dpi=300, bbox_inches='tight')
    plt.show()

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

anamoly_calculation(
    ndvi_output_data+'_output_image_',
    ndci_output_data+'_output_image_',
    b8ab4_output_data+'_output_image_',
    b3b2_output_data+'_output_image_',
    'Sentinel2_Composite_2016-08-16.tif',
    'C:\\Users\\Agilan B\\fyp\\Algal-bloom\\template\\output\\anamoly_output\\',
    'C:\\Users\\Agilan B\\fyp\\Algal-bloom\\template\\output\\anamoly_output\\combined_anamoly\\'
)
