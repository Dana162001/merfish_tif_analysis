import argparse
import os
import numpy as np
import tifffile

def merge_tif_images(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through each TIFF image in the input directory
    for file in os.listdir(input_dir):
        if file.endswith(".tif"):
            # Extract the channel number from the file name
            num = file.split("_")[-1].split(".")[0]

            # Construct the full file paths for each channel
            image_path1 = os.path.join(input_dir, f"channel_1_{num}.tif")
            image_path2 = os.path.join(input_dir, f"channel_2_{num}.tif")
            image_path3 = os.path.join(input_dir, f"channel_3_{num}.tif")
            image_path4 = os.path.join(input_dir, f"channel_4_{num}.tif")

            # Read the input images
            image1 = tifffile.imread(image_path1)
            image2 = tifffile.imread(image_path2)
            image3 = tifffile.imread(image_path3)
            image4 = tifffile.imread(image_path4)

            # Resize or pad the input images to have the same shape
            max_height = max(image1.shape[0], image2.shape[0], image3.shape[0], image4.shape[0])
            max_width = max(image1.shape[1], image2.shape[1], image3.shape[1], image4.shape[1])

            image1 = np.pad(image1, ((0, max_height - image1.shape[0]), (0, max_width - image1.shape[1])),
                            mode='constant')
            image2 = np.pad(image2, ((0, max_height - image2.shape[0]), (0, max_width - image2.shape[1])),
                            mode='constant')
            image3 = np.pad(image3, ((0, max_height - image3.shape[0]), (0, max_width - image3.shape[1])),
                            mode='constant')
            image4 = np.pad(image4, ((0, max_height - image4.shape[0]), (0, max_width - image4.shape[1])),
                            mode='constant')

            # Create a blank multichannel image with the same shape as the input images
            multichannel_image = np.zeros((max_height, max_width, 4), dtype=np.uint16)

            # Assign each input image to a separate channel in the multichannel image
            multichannel_image[..., 0] = image1  # Red channel
            multichannel_image[..., 1] = image3  # Green channel
            multichannel_image[..., 2] = image4  # Blue channel
            multichannel_image[..., 3] = image2  # Alpha channel (optional)

            # Save the multichannel TIFF image
            output_path = os.path.join(output_dir, f"merged_{num}.tif")
            tifffile.imwrite(output_path, multichannel_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge TIFF images into a multichannel image")
    parser.add_argument("-i", "--input_dir", type=str, help="Input directory containing TIFF images")
    parser.add_argument("-o", "--output_dir", type=str, help="Output directory to save merged TIFF images")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    merge_tif_images(input_dir, output_dir)
