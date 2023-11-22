import sys
import os
import xml.etree.ElementTree as ET

def process_xml(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Extract the folder path and create the output path in the same folder
    folder_path = os.path.dirname(input_file)
    output_path = os.path.join(folder_path, output_file)

    # Open the output file for writing
    with open(output_path, 'w', encoding='utf-8') as output:
        # Iterate through each 'game' element in the XML
        for game in root.findall('game'):
            name = game.find('name').text.strip() if game.find('name') is not None else "N/A"
            path = game.find('path').text.strip() if game.find('path') is not None else "N/A"
            developer = game.find('developer').text.strip() if game.find('developer') is not None else "N/A"
            publisher = game.find('publisher').text.strip() if game.find('publisher') is not None else "N/A"
            genre = game.find('genre').text.strip() if game.find('genre') is not None else "N/A"
            
            # Concatenate paragraphs within the <desc> tag and remove empty lines
            desc = ' '.join(p.strip() for p in game.find('desc').itertext() if p.strip()) if game.find('desc') is not None else "N/A"
            
            releasedate = game.find('releasedate').text.strip() if game.find('releasedate') is not None else "N/A"
            players = game.find('players').text.strip() if game.find('players') is not None else "N/A"
            rating = game.find('rating').text.strip() if game.find('rating') is not None else "N/A"

            # Extract the filename and extension
            filename, extension = os.path.splitext(os.path.basename(path))
            
            # Format the output with additional items under 'file' section
            output.write(f"game: {name}\n"
                         f"file: {path}\n"
                         f"assets.boxFront: assets/covers/{filename}.png\n"
                         f"assets.boxBack: assets/backcovers/{filename}.png\n"
                         f"assets.screenshot: assets/screenshots/{filename}.png\n"
                         f"assets.titlescreen: assets/titlescreens/{filename}.png\n"
                         f"assets.banner: assets/fanart/{filename}.png\n"
                         f"assets.cartridge: assets/physicalmedia/{filename}.png\n"
                         f"assets.boxFull: assets/miximages/{filename}.png\n"
                         f"assets.marquee: assets/marquees/{filename}.png\n"
                         f"assets.video: assets/videos/{filename}.mp4\n"
                         f"developer: {developer}\npublisher: {publisher}\n"
                         f"genre: {genre}\ndescription: {desc}\nrelease: {releasedate[:4]}-{releasedate[4:6]}-{releasedate[6:8]}\n"
                         f"players: {players}\nrating: {rating}%\n\n")

def process_and_delete_folder(root_folder):
    # Iterate through subfolders in the root folder
    for subdir, _, files in os.walk(root_folder):
        # Check if there's a gamelist.xml file in the current subfolder
        if 'gamelist.xml' in files:
            input_file = os.path.join(subdir, 'gamelist.xml')
            output_file = 'metadata.txt'
            
            # Process the XML file and save the output in the same subfolder
            process_xml(input_file, output_file)

            # Delete the gamelist.xml file
            os.remove(input_file)

if __name__ == "__main__":
    # Set the default root folder to 'gamelists' in the same directory as the script
    default_root_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gamelists')

    # Check if a root folder is provided as a command-line argument, otherwise use the default
    root_folder = sys.argv[1] if len(sys.argv) > 1 else default_root_folder

    # Process the subfolders and delete gamelist.xml files
    process_and_delete_folder(root_folder)

    print("Conversion completed.")
