import os
import struct
import shutil  # Import for file copying

VERSION = "1.3.3"

def create_combine_folder(base_name, folder_path):
    """Creates the {BaseName}_Combine_BRWSD folder."""
    combine_folder = os.path.join(folder_path, f"{base_name}_Combine_BRWSD")
    if not os.path.exists(combine_folder):
        os.makedirs(combine_folder)
        print(f"Created folder: {combine_folder}")
    return combine_folder

def pad_to_multiple_of(value, multiple):
    """Pads a value to the next multiple of 'multiple'."""
    remainder = value % multiple
    return value if remainder == 0 else value + (multiple - remainder)

def write_rwar_header(brwsd_file, tabl_size, data_offset, rwav_total_size):
    """Writes the RWAR header to the brwsd file."""
    brwsd_file.write(b'RWAR')  # 0x0 to 0x3
    brwsd_file.write(struct.pack('>I', 0xFEFF0100))  # 0x4 to 0x7 (constant value)
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x8 to 0xB (total file size)
    brwsd_file.write(struct.pack('>I', 0x200002))  # 0xC to 0xF (constant value)

    brwsd_file.write(struct.pack('>I', 0x20))  # 0x10 to 0x13 (fixed number 20)
    tabl_size = (tabl_size + 15) // 16 * 16 #PATCH 1.3.3 - Didn't take in to account padding to fill to a clean number eg. 0x10
    brwsd_file.write(struct.pack('>I', tabl_size))  # 0x14 to 0x17 (length of the TABL section)
    brwsd_file.write(struct.pack('>I', tabl_size + 0x20))  # 0x18 to 0x1B (TABL length + 0x20)
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x1C to 0x1F (RWAV section size)

def write_tabl_header(brwsd_file, rwav_files_info):
    """Writes the TABL section header."""
    brwsd_file.write(b'TABL')  # 0x0 to 0x3
    tabl_size = 0x10 + len(rwav_files_info) * 12  # Each RWAV adds 12 bytes to TABL
    tabl_size = (tabl_size + 15) // 16 * 16 #PATCH 1.3.3 - Didn't take in to account padding to fill to a clean number eg. 0x10
    brwsd_file.write(struct.pack('>I', tabl_size))  # 0x4 to 0x7 (Table size)
    brwsd_file.write(struct.pack('>I', len(rwav_files_info)))  # 0x8 to 0xB (RWAV count)

    # Write the [01000000], offset, and size for each RWAV
    for rwav_info in rwav_files_info:
        brwsd_file.write(b'\x01\x00\x00\x00')  # Constant value [01000000]
        brwsd_file.write(struct.pack('>I', rwav_info['offset']))  # Offset
        brwsd_file.write(struct.pack('>I', rwav_info['size']))  # Size

    # Pad the TABL section to be a multiple of 16 bytes
    current_pos = brwsd_file.tell()
    padded_size = pad_to_multiple_of(current_pos, 16)
    padding_needed = padded_size - current_pos
    if padding_needed > 0:
        brwsd_file.write(b'\x00' * padding_needed)
    brwsd_file.write(b'\00' * (0x10))  # 0x20 - 8 already written bytes  #PATCH 1.3.3

def write_data_section(brwsd_file, rwav_total_size):
    """Writes the DATA section to the brwsd file."""
    brwsd_file.write(b'DATA')  # 0x0 to 0x3
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x4 to 0x7 (RWAV total size)
    #PATCH 1.3.3 - Removed the writing of 00 for 24 bytes. 
    #This was redundent because it is already done by something else and thus was creating EXTRA padding

def combine_rwav_files_to_brwsd(rwav_folder, output_file):
    """Combines all RWAV files in the folder into a single .brwsd file with a header."""
    rwav_files = sorted(
        [f for f in os.listdir(rwav_folder) if os.path.isfile(os.path.join(rwav_folder, f))],
        key=lambda x: int(x.split("_")[-1])
    )

    rwav_files_info = []
    current_offset = 0x20 #PATCH 1.3.3 - Lowered from 0x40

    # Calculate RWAV sizes and offsets before writing any data
    rwav_total_size = 0
    for rwav_file in rwav_files:
        rwav_file_path = os.path.join(rwav_folder, rwav_file)
        rwav_size = os.path.getsize(rwav_file_path)
        rwav_files_info.append({
            'offset': current_offset,
            'size': rwav_size
        })
        current_offset += rwav_size
        rwav_total_size += rwav_size
    rwav_total_size += 32 #PATCH 1.3.3 - Was not present of previous versions
    tabl_size = 0x10 + len(rwav_files_info) * 12
    data_offset = pad_to_multiple_of(0x40 + tabl_size, 16) #PATCH 1.3.3 - Lowered from 0x60 to 0x40

    with open(output_file, 'wb') as brwsd_file:
        # Write the headers first
        write_rwar_header(brwsd_file, tabl_size, data_offset, rwav_total_size)  # RWAR header
        write_tabl_header(brwsd_file, rwav_files_info)  # TABL header
        write_data_section(brwsd_file, rwav_total_size)  # DATA section

        # Move to the position after the headers to append RWAV data
        brwsd_file.seek(data_offset)

        # Now write RWAV data
        for rwav_file in rwav_files:
            rwav_file_path = os.path.join(rwav_folder, rwav_file)
            with open(rwav_file_path, 'rb') as f:
                data = f.read()
                brwsd_file.write(data)

        print(f"Created {output_file} with combined RWAV files and headers.")

def append_and_replace_base_blank(base_blank_file, original_file):
    """Appends the original file's data to BaseBlankFile.brwsd and replaces the original."""
    # First, copy the BaseBlankFile.brwsd to the folder where the combined file is
    temp_base_blank = original_file + "_temp"
    shutil.copy(base_blank_file, temp_base_blank)
    
    # Append original file's data to the temp copy of BaseBlankFile.brwsd
    with open(temp_base_blank, 'ab') as blank_file:
        with open(original_file, 'rb') as orig_file:
            blank_file.write(orig_file.read())

    # Delete the original combined file
    os.remove(original_file)

    # Rename the temporary BaseBlankFile.brwsd to the original file name
    os.rename(temp_base_blank, original_file)
    print(f"Appended {original_file} to BaseBlankFile.brwsd and renamed it to {original_file}")

def create_project_folders(folder_path):
    """Creates two folders: '1-Project-Unmodified' and '0-Project-Modified' if they don't exist."""
    unmodified_folder = os.path.join(folder_path, "1-Project-Unmodified")
    modified_folder = os.path.join(folder_path, "0-Project-Modified")

    if not os.path.exists(unmodified_folder):
        os.makedirs(unmodified_folder)
        print(f"Created folder: {unmodified_folder}")
    
    if not os.path.exists(modified_folder):
        os.makedirs(modified_folder)
        print(f"Created folder: {modified_folder}")

def main():
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Create "1-Project-Unmodified" and "0-Project-Modified" folders
    create_project_folders(current_folder)

    # Find all folders ending with "_Extract_RWAV"
    rwav_folders = [f for f in os.listdir(current_folder) if f.endswith("_Extract_RWAV") and os.path.isdir(os.path.join(current_folder, f))]

    for rwav_folder in rwav_folders:
        base_name = rwav_folder.replace("_Extract_RWAV", "")
        rwav_folder_path = os.path.join(current_folder, rwav_folder)

        # Create the {BaseName}_Combine_BRWSD folder
        combine_folder = create_combine_folder(base_name, current_folder)

        # Create the output .brwsd file in the {BaseName}_Combine_BRWSD folder
        output_file = os.path.join(combine_folder, f"{base_name}.brwsd")
        combine_rwav_files_to_brwsd(rwav_folder_path, output_file)

        # Handle BaseBlankFile.brwsd logic
        base_blank_file = os.path.join(current_folder, "BaseBlankFile.brwsd")
        if os.path.exists(base_blank_file):
            # Copy the base blank file and append the combined data
            append_and_replace_base_blank(base_blank_file, output_file)

if __name__ == "__main__":
    main()
