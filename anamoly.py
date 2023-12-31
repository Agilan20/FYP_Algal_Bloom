import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate standardized anomalies
def calculate_standardized_anomaly(image, baseline_mean, baseline_std):
    anomalies = (image - baseline_mean) / baseline_std
    return anomalies

# Visualizing all anomalies
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
axs = axs.ravel()

def visualize_and_save_anomalies(image, anomalies, threshold_positive, threshold_negative, output_filename, title, i):
    try:
        # Create masks for positive and negative anomalies
        positive_anomalies = np.where(anomalies > threshold_positive, 1, 0)
        negative_anomalies = np.where(anomalies < threshold_negative, 1, 0)

        axs[i].imshow(positive_anomalies, cmap='Greens', alpha=0.7)
        axs[i].imshow(negative_anomalies, cmap='Reds', alpha=0.7)
        axs[i].set_title(title)

        with rasterio.open(output_filename, 'w', driver='GTiff', width=image.width,
                           height=image.height, count=1, dtype='float32') as dst:
            dst.write(anomalies, 1)
            dst.update_tags(ns='TIFF', description=output_filename)
    except Exception as e:
        print(f"An error occurred while processing {title}: {e}")

def anamoly_calculation(ndvi, ndci, b8ab4, b3b2, input, output_path, combined_output_path):
    try:
        ndvi_image = rasterio.open(ndvi + input)
        ndci_image = rasterio.open(ndci + input)
        ndbi_image = rasterio.open(b8ab4 + input)
        ndwi_image = rasterio.open(b3b2 + input)

        # Define baseline means and standard deviations for each index
        baseline_ndvi_mean = 0.5
        baseline_ndvi_std = 0.1
        baseline_ndci_mean = 0.2
        baseline_ndci_std = 0.05
        baseline_ndbi_mean = 0.1
        baseline_ndbi_std = 0.03
        baseline_ndwi_mean = 0.3
        baseline_ndwi_std = 0.08

        ndvi_anomalies = calculate_standardized_anomaly(ndvi_image.read(1), baseline_ndvi_mean, baseline_ndvi_std)
        ndci_anomalies = calculate_standardized_anomaly(ndci_image.read(1), baseline_ndci_mean, baseline_ndci_std)
        ndbi_anomalies = calculate_standardized_anomaly(ndbi_image.read(1), baseline_ndbi_mean, baseline_ndbi_std)
        ndwi_anomalies = calculate_standardized_anomaly(ndwi_image.read(1), baseline_ndwi_mean, baseline_ndwi_std)

        # Define threshold values for anomalies (e.g., +/- 2 standard deviations)
        threshold_positive = 2
        threshold_negative = -2

        visualize_and_save_anomalies(ndvi_image, ndvi_anomalies, threshold_positive, threshold_negative,output_path + 'ndvi\\' + 'ndvi_anomalies_' + input, 'NDVI Anomalies', 0)
        visualize_and_save_anomalies(ndci_image, ndci_anomalies, threshold_positive, threshold_negative,output_path + 'ndci\\' + 'ndci_anomalies_' + input, 'NDCI Anomalies', 1)
        visualize_and_save_anomalies(ndbi_image, ndbi_anomalies, threshold_positive, threshold_negative,output_path + 'ndbi\\' + 'ndbi_anomalies_' + input, 'NDBI Anomalies', 2)
        visualize_and_save_anomalies(ndwi_image, ndwi_anomalies, threshold_positive, threshold_negative,output_path + 'ndwi\\' + 'ndwi_anomalies_' + input, 'NDWI Anomalies', 3)

        new_string = input.replace(".tif", ".png")
        combined_output_path_url = combined_output_path + 'combined_anomalies_subplot_' + new_string
        plt.savefig(combined_output_path_url, dpi=300, bbox_inches='tight')
        # plt.show()
    except Exception as e:
        print(f"An error occurred in the anomaly calculation process: {e}")
