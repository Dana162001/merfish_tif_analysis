import os
import glob
import argparse
import tifffile as tiff

def extract_images(input_dir, output_dir):
    # Get list of TIFF files in input directory
    tif_files = glob.glob(os.path.join(input_dir, 'stack_0_*.tif'))

    for tif_file in tif_files:
        # Extract file name and corresponding prestain file name
        tif_filename = os.path.basename(tif_file)
        prestain_filename = tif_filename.replace('stack_0_', 'stack_prestain_')

        # Extract individual images from the TIF stack
        tif_s = tiff.imread(tif_file)
        tif_p = tiff.imread(os.path.join(input_dir, prestain_filename))

        image1 = tif_s[3]
        image2 = tif_s[10]
        image3 = tif_s[17]
        image_dapi = tif_p[18]

        # Construct output file names using original numbers
        output_filename = 'extracted_images_{}.tif'.format(tif_filename.split('_')[2])
        output_path = os.path.join(output_dir, output_filename)

        # Save extracted images to output file
        tiff.imwrite(output_path, image1)
        tiff.imwrite(output_path, image2, append=True)
        tiff.imwrite(output_path, image3, append=True)
        tiff.imwrite(output_path, image_dapi, append=True)

    print('Extraction complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract images from TIFF files.')
    parser.add_argument('--i', dest='input_dir', type=str, required=True, help='Input directory containing TIFF files')
    parser.add_argument('--o', dest='output_dir', type=str, required=True, help='Output directory to save extracted images')
    args = parser.parse_args()

    extract_images(args.input_dir, args.output_dir)
