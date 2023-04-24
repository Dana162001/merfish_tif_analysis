import os
import argparse
import glob
import tifffile
import numpy as np


def split_tiff_channels(input_dir, output_dir):
    tif_files = glob.glob(os.path.join(input_dir, "*.tif"))
    for tif_file in tif_files:
        with tifffile.TiffFile(tif_file) as tif:
            # Read the TIFF file and get the number of pages (images)
            pages = tif.pages
            num_pages = len(pages)

            # Extract the number from the original file name
            file_name = os.path.splitext(os.path.basename(tif_file))[0]
            number = file_name.split("_")[-1]

            # Loop through each page and extract the data
            for i in range(num_pages):
                # Read the page data
                page_data = pages[i].asarray()

                # Save the page data as a separate TIFF file with number in the file name
                output_path = os.path.join(output_dir, f"channel_{i + 1}_{number}.tif")  # Output file name
                tifffile.imwrite(output_path, page_data)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split channels of multi-page TIFF images into separate TIFF files.")
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="Input directory containing TIFF files.")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Output directory to save the split TIFF channels.")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    split_tiff_channels(input_dir, output_dir)