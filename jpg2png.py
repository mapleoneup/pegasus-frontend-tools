from PIL import Image
import os
import sys

def convert_jpg_to_png(input_path, output_path):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Convert the image to 'P' mode (paletted)
            img = img.convert('P', palette=Image.ADAPTIVE, colors=254)
            # Save the image as PNG with optimized compression
            img.save(output_path, 'PNG', optimize=True)
        print(f"Converted: {input_path} -> {output_path}")
        # Remove the original JPG file
        os.remove(input_path)
        print(f"Deleted: {input_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def convert_all_jpg_to_png(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".jpg"):
                jpg_path = os.path.join(root, file)
                png_path = jpg_path[:-4] + ".png"  # Replace extension with .png
                convert_jpg_to_png(jpg_path, png_path)

if __name__ == "__main__":
    default_directory = "downloaded_media"
    
    if len(sys.argv) == 1:
        directory_path = default_directory
    elif len(sys.argv) == 2:
        directory_path = sys.argv[1]
    else:
        print("Usage: python script_name.py [directory_path]")
        sys.exit(1)

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    convert_all_jpg_to_png(directory_path)
