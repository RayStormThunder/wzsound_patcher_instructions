import os
import shutil

# --- Part 1: Extract RWAV files from .brwsd files ---

def find_brwsd_file(project_folder):
    """Search for .brwsd file in the given project folder."""
    for file_name in os.listdir(project_folder):
        if file_name.endswith(".brwsd"):
            return os.path.join(project_folder, file_name)
    return None

def create_output_folder(output_folder):
    """Create the output folder if it doesn't exist."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def extract_rwav_sections(brwsd_path, output_folder):
    """Search for RWAV sections and extract them."""
    rwav_signature = b'RWAV'  # RWAV signature in bytes
    audio_count = 0

    with open(brwsd_path, 'rb') as brwsd_file:
        data = brwsd_file.read()
        position = 0
        
        while True:
            # Search for the next occurrence of RWAV
            rwav_start = data.find(rwav_signature, position)
            if rwav_start == -1:
                break  # No more RWAV sections
            
            # Extract the RWAV section
            rwav_end = data.find(rwav_signature, rwav_start + len(rwav_signature))
            if rwav_end == -1:
                rwav_end = len(data)  # Last RWAV section goes until the end of the file

            # Extract the RWAV file and save it
            rwav_data = data[rwav_start:rwav_end]
            output_file_path = os.path.join(output_folder, f"Audio{audio_count}.rwav")
            with open(output_file_path, 'wb') as audio_file:
                audio_file.write(rwav_data)
            
            print(f"Extracted {output_file_path}")
            audio_count += 1
            position = rwav_end  # Move to the end of the current RWAV section

def process_project(project_folder, output_folder):
    """Process a project folder to extract RWAV sections."""
    brwsd_file_path = find_brwsd_file(project_folder)
    if brwsd_file_path is None:
        print(f"No .brwsd file found in the '{project_folder}' folder.")
        return
    
    print(f"Found .brwsd file: {brwsd_file_path}")
    
    # Create the output folder
    create_output_folder(output_folder)
    
    # Extract RWAV sections
    extract_rwav_sections(brwsd_file_path, output_folder)

# --- Part 2: Copy brsar and replace RWAV files ---

def copy_brsar_file():
    """Copies Unmod_Wii_WZSound.brsar to Modified_Wii_WZSound.brsar in the 5-WZSound-Output folder."""
    src_file = "Unmod_Wii_WZSound.brsar"
    output_folder = "5-WZSound-Output"
    dst_file = os.path.join(output_folder, "Modified_Wii_WZSound.brsar")
    
    # Ensure the source file exists
    if not os.path.exists(src_file):
        print(f"Source file {src_file} not found.")
        return False
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    shutil.copyfile(src_file, dst_file)
    print(f"Copied {src_file} to {dst_file}.")
    return dst_file

def read_file_bytes(file_path):
    """Reads a file and returns its byte content."""
    with open(file_path, 'rb') as f:
        return f.read()

def replace_rwav_in_brsar(brsar_file, modified_rwav_folder, unmodified_rwav_folder):
    """Replaces RWAV files in the .brsar file with corresponding data from 3-RWAV-Modified."""
    with open(brsar_file, 'r+b') as brsar:
        brsar_data = brsar.read()

        # Go through each RWAV file in 4-RWAV-Unmodified
        for rwav_file in os.listdir(unmodified_rwav_folder):
            unmodified_rwav_path = os.path.join(unmodified_rwav_folder, rwav_file)
            modified_rwav_path = os.path.join(modified_rwav_folder, rwav_file)
            
            # Ensure both files exist
            if not os.path.exists(modified_rwav_path):
                print(f"Corresponding modified file {modified_rwav_path} not found, skipping.")
                continue
            
            # Get file sizes for comparison
            unmodified_rwav_size = os.path.getsize(unmodified_rwav_path)
            modified_rwav_size = os.path.getsize(modified_rwav_path)
            
            # Skip replacement if the modified file is larger
            if modified_rwav_size > unmodified_rwav_size:
                print(f"Skipping {rwav_file}: Modified RWAV file is larger ({modified_rwav_size} bytes) than the unmodified RWAV file ({unmodified_rwav_size} bytes).")
                continue
            
            # Read the unmodified and modified RWAV file data
            unmodified_rwav_data = read_file_bytes(unmodified_rwav_path)
            modified_rwav_data = read_file_bytes(modified_rwav_path)
            
            # Search for all occurrences of the unmodified RWAV data in the brsar file
            match_pos = brsar_data.find(unmodified_rwav_data)
            if match_pos == -1:
                print(f"No match found for {rwav_file} in {brsar_file}.")
                continue

            # Replace all occurrences of the unmodified RWAV data with the modified RWAV data
            while match_pos != -1:
                brsar.seek(match_pos)
                brsar.write(modified_rwav_data)
                print(f"Replaced data for {rwav_file} at position {match_pos}.")
                
                # Search for the next occurrence
                match_pos = brsar_data.find(unmodified_rwav_data, match_pos + 1)

    print(f"Finished replacing RWAV files in {brsar_file}.")

# --- Main program to combine both parts ---

def main():
    # Part 1: Process two projects and extract RWAVs
    process_project("0-Project-Modified", "3-RWAV-Modified")
    process_project("1-Project-Unmodified", "4-RWAV-Unmodified")
    
    # Part 2: Create the 5-WZSound-Output folder and copy the brsar file
    brsar_file = copy_brsar_file()
    if not brsar_file:
        return
    
    # Replace RWAV data in the copied brsar file
    replace_rwav_in_brsar(brsar_file, "3-RWAV-Modified", "4-RWAV-Unmodified")

if __name__ == "__main__":
    main()
