import rasterio
from rasterio.transform import from_origin

def b8ab4_calculation(path, input_image, output_data):
    # Open the TIFF file
    with rasterio.open(path+input_image) as src:
        red_band = src.read(4)  # Replace with the actual band numbers or names
        B8A_band = src.read(9)
        profile = src.profile  # Get the profile of the source raster
        left, bottom, right, top = src.bounds
        xsize = src.width
        ysize = src.height

    # Calculate B8AB4
    B8AB4 = (B8A_band - red_band) / (B8A_band + red_band)

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
    # Save the B8AB4 result to a new TIFF file with georeferencing information
    with rasterio.open(output_data+input_image[4:], 'w', **profile) as dst:
        dst.write(B8AB4, 1)
