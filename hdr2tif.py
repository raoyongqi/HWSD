import rasterio
from rasterio.transform import from_origin
import numpy as np
import os

def convert_envi_to_tiff(hdr_file, bil_file, output_tiff):
    # Read the header file to get metadata
    with open(hdr_file, 'r') as hdr:
        header_lines = hdr.readlines()
    
    metadata = {}
    for line in header_lines:
        if '=' in line:
            key, value = line.strip().split('=')
            metadata[key.strip()] = value.strip()

    # Extract relevant metadata
    width = int(metadata.get('samples', 0))
    height = int(metadata.get('lines', 0))
    bands = int(metadata.get('bands', 1))
    data_type = metadata.get('data type', '0')

    # Data type mapping (ENVI data types to numpy dtypes)
    data_type_map = {
        '0': 'uint8',
        '1': 'int16',
        '2': 'int32',
        '3': 'float32',
        '4': 'float64'
    }

    dtype = data_type_map.get(data_type, 'uint8')

    # Read the binary raster data
    with open(bil_file, 'rb') as bil:
        data = np.fromfile(bil, dtype=dtype).reshape((bands, height, width))

    # Define transform (assuming the .blw file is available for world file info)
    transform = from_origin(
        float(metadata.get('map info', '0').split(',')[3]),  # x-coordinate of upper-left corner
        float(metadata.get('map info', '0').split(',')[4]),  # y-coordinate of upper-left corner
        float(metadata.get('map info', '0').split(',')[1]),  # pixel width
        float(metadata.get('map info', '0').split(',')[2])   # pixel height
    )

    # Write to TIFF
    with rasterio.open(
        output_tiff, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=bands,
        dtype=dtype,
        crs='EPSG:4326',  # You may need to update the CRS based on your data
        transform=transform
    ) as dst:
        for i in range(bands):
            dst.write(data[i, :, :], i + 1)

# Example usage
hdr_file = 'path_to_your_file.hdr'
bil_file = 'path_to_your_file.bil'
output_tiff = 'OUTPUT/output_file.tif'

convert_envi_to_tiff(hdr_file, bil_file, output_tiff)
