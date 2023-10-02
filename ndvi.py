import rasterio
from rasterio.transform import from_origin

def ndvi_calculation(path, input_image, output_data):
    # Open the TIFF file
    with rasterio.open(path+input_image) as src:
        red_band = src.read(4)  # Replace with the actual band numbers or names
        nir_band = src.read(8)
        profile = src.profile  # Get the profile of the source raster
        left, bottom, right, top = src.bounds
        xsize = src.width
        ysize = src.height

    # Calculate NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)

    # Replace these values with the spatial extent information you obtained
    left = left
    top = right
    xsize = xsize
    ysize = ysize

    # Calculate the transform
    transform = from_origin(left, top, xsize, ysize)

    # Update the profile with the georeferencing information
    profile.update(
        dtype=rasterio.float32,
        count=1,
        transform=transform,
        driver='GTiff'
    )
    # Save the NDVI result to a new TIFF file with georeferencing information
    with rasterio.open(output_data+input_image[4:], 'w', **profile) as dst:
        dst.write(ndvi, 1)
