#!/bin/bash

# Check if both root folder arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <first_root_folder> <second_root_folder>"
    exit 1
fi

# Define the root folders
first_root_folder="$1"
second_root_folder="$2"

# Check if the first root folder exists
if [ ! -d "$first_root_folder" ]; then
    echo "Error: First root folder not found."
    exit 1
fi

# Check if the second root folder exists
if [ ! -d "$second_root_folder" ]; then
    echo "Error: Second root folder not found."
    exit 1
fi

# Iterate over subdirectories in the first root folder
for subfolder_first in "$first_root_folder"/*/; do
    if [ -d "$subfolder_first" ]; then
        # Get the subfolder name
        subfolder_name=$(basename "$subfolder_first")

        # Check if the counterpart subfolder exists in the second root folder
        subfolder_second="$second_root_folder/$subfolder_name"
        if [ -d "$subfolder_second" ]; then
            # Rename the subfolder in the first root folder to "assets"
            mv "$subfolder_first" "$first_root_folder/assets"

            # Create a new folder in the first root folder with the original name
            mkdir "$first_root_folder/$subfolder_name"

            # Move the "assets" folder to the new folder
            mv "$first_root_folder/assets" "$first_root_folder/$subfolder_name/assets"

            # Move metadata.txt file from second to first root folder
            metadata_file="$subfolder_second/metadata.txt"
            if [ -f "$metadata_file" ]; then
                mv "$metadata_file" "$first_root_folder/$subfolder_name/"
                echo "Moved metadata.txt from $subfolder_second to $first_root_folder/$subfolder_name"
            else
                echo "Error: metadata.txt not found in $subfolder_second"
            fi

            echo "Processed subfolder: $subfolder_first"
            echo "Created new folder: $first_root_folder/$subfolder_name"
        else
            echo "Error: Corresponding subfolder $subfolder_second not found in the second root folder."
        fi
    fi
done

# Delete the second root folder
rm -r "$second_root_folder"
echo "Deleted second root folder: $second_root_folder"

# Rename the first root folder to "Games"
mv "$first_root_folder" "$(dirname "$first_root_folder")/Games"
echo "Renamed first root folder to Games."

echo "Script completed."
