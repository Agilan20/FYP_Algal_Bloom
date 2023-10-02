import rasterio
from rasterio.transform import from_origin

def ndci_calculation(path, input_image, output_data):
    try:
        with rasterio.open(path + input_image) as src:
            red_band = src.read(4)
            red_edge1_band = src.read(5)
            profile = src.profile
            left, bottom, right, top = src.bounds
            xsize = src.width
            ysize = src.height

        ndci = (red_edge1_band - red_band) / (red_edge1_band + red_band)

        left = left
        top = right
        xsize = xsize
        ysize = ysize

        transform = from_origin(left, top, xsize, ysize)

        profile.update(
            dtype=rasterio.float32,
            count=1,
            transform=transform,
            driver='GTiff'
        )
        # Saving new TIFF file with georeferencing information
        with rasterio.open(output_data + input_image[4:], 'w', **profile) as dst:
            dst.write(ndci, 1)
    except Exception as e:
        print(f"An error occurred: {e}")

