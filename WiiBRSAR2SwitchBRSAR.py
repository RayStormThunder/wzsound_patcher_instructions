import os
import shutil

VERSION = "1.0.1"

def copy_brsar_file():
    """Copies Switch_WZSound.brsar to WZSound.brsar in the current folder."""
    src_file = "Unmod_Switch_WZSound.brsar"
    dst_file = "Modified_Switch_WZSound.brsar"
    
    if not os.path.exists(src_file):
        print(f"Source file {src_file} not found.")
        return False
    
    shutil.copyfile(src_file, dst_file)
    print(f"Copied {src_file} to {dst_file}.")
    return True

def read_file_bytes(file_path):
    """Reads a file and returns its byte content."""
    with open(file_path, 'rb') as f:
        return f.read()

def replace_rwav_in_brsar(brsar_file, switch_rwav_folder, wii_rwav_folder):
    """Replaces RWAV files in the .brsar file with corresponding data from Wii_WZSound_Extract_RWAV."""
    with open(brsar_file, 'r+b') as brsar:
        brsar_data = brsar.read()

        # Go through each RWAV file in Switch_WZSound_Extract_RWAV
        for rwav_file in os.listdir(switch_rwav_folder):
            switch_rwav_path = os.path.join(switch_rwav_folder, rwav_file)
            wii_rwav_path = os.path.join(wii_rwav_folder, rwav_file)
            
            # Ensure both files exist
            if not os.path.exists(wii_rwav_path):
                print(f"Corresponding file {wii_rwav_path} not found, skipping.")
                continue
            
            # Get file sizes for comparison
            switch_rwav_size = os.path.getsize(switch_rwav_path)
            wii_rwav_size = os.path.getsize(wii_rwav_path)
            
            # Skip replacement if the Wii file is larger
            if wii_rwav_size > switch_rwav_size:
                print(f"Skipping {rwav_file}: Wii RWAV file is larger ({wii_rwav_size} bytes) than the Switch RWAV file ({switch_rwav_size} bytes).")
                continue
            
            # Read the Switch and Wii RWAV file data
            switch_rwav_data = read_file_bytes(switch_rwav_path)
            wii_rwav_data = read_file_bytes(wii_rwav_path)
            
            # Search for all occurrences of the Switch RWAV data in the brsar file
            match_pos = brsar_data.find(switch_rwav_data)
            if match_pos == -1:
                print(f"No match found for {rwav_file} in {brsar_file}.")
                continue

            # Replace all occurrences of the Switch RWAV data with the Wii RWAV data
            while match_pos != -1:
                brsar.seek(match_pos)
                brsar.write(wii_rwav_data)
                print(f"Replaced data for {rwav_file} at position {match_pos}.")
                
                # Search for the next occurrence
                match_pos = brsar_data.find(switch_rwav_data, match_pos + 1)

    print(f"Finished replacing RWAV files in {brsar_file}.")

def main():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    switch_rwav_folder = os.path.join(current_folder, "Unmod_Switch_WZSound_Extract_RWAV")
    wii_rwav_folder = os.path.join(current_folder, "Modified_Wii_WZSound_Extract_RWAV")
    brsar_file = os.path.join(current_folder, "Modified_Switch_WZSound.brsar")
    
    # Copy the brsar file first
    if not copy_brsar_file():
        return
    
    # Replace RWAV data in the copied WZSound.brsar file
    replace_rwav_in_brsar(brsar_file, switch_rwav_folder, wii_rwav_folder)

if __name__ == "__main__":
    main()