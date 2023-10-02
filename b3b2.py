import rasterio
from rasterio.transform import from_origin

def b3b2_calculation(path, input_image, output_data):
    # Open the TIFF file
    with rasterio.open(path+input_image) as src:
        green_band = src.read(3)  # Replace with the actual band numbers or names
        blue_band = src.read(2)
        profile = src.profile  # Get the profile of the source raster
        left, bottom, right, top = src.bounds
        xsize = src.width
        ysize = src.height

    # Calculate B3B2
    B3B2 = (green_band - blue_band) / (green_band + blue_band)

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
    # Save the B3B2 result to a new TIFF file with georeferencing information
    with rasterio.open(output_data+input_image[4:], 'w', **profile) as dst:
        dst.write(B3B2, 1)