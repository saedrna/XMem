import cv2
import glob
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize mask')
    parser.add_argument('-s', '--source_directory', type=str, required=True, help='Source directory')
    parser.add_argument('-t', '--target_directory', type=str, required=True, help='Target directory')
    parser.add_argument('-w', '--target_size', type=str, required=True, help='Target size, e.g., (2000, 1000)')
    args = parser.parse_args()

    # Make sure target directory exists, if not, create it
    os.makedirs(args.target_directory, exist_ok=True)

    # parse target size as tuple of ints
    target_size = tuple(map(int, args.target_size.strip('()').split(',')))

    # Get list of all image files
    image_files = glob.glob(os.path.join(args.source_directory, '*'))

    for image_file in image_files:
        # Read image
        img = cv2.imread(image_file)

        # Resize image
        img_resized = cv2.resize(img, target_size)

        # Use only red channel
        red_channel = img_resized[:, :, 2]

        # Convert pixel intensities from 128 to 255
        red_channel[red_channel >= 128] = 255

        # Save image to new directory
        base_name = os.path.basename(image_file)
        file_name, _ = os.path.splitext(base_name)
        target_file_path = os.path.join(args.target_directory, f"{file_name}_mask.tif")
        cv2.imwrite(target_file_path, red_channel)
