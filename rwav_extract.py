import os
import struct
import yaml

def read_project_instructions(filepath, folder_name):
	# Build the path to instructions.yaml
	instructions_path = os.path.join(filepath, "Projects", folder_name, "instructions.yaml")

	# Check if the file exists
	if not os.path.exists(instructions_path):
		print(f"File not found: {instructions_path}")
		return []

	# Read and return the YAML content
	try:
		with open(instructions_path, "r", encoding="utf-8") as f:
			data = yaml.safe_load(f)
			return data if isinstance(data, list) else []
	except Exception as e:
		print(f"Error reading {instructions_path}: {e}")
		return []


def read_instructions_file(folder_path):
    """Reads the Program_Instructions.txt file and parses the RWSD and RWAV extraction instructions."""
    instructions_file = os.path.join(folder_path, "Program_Instructions.txt")
    if not os.path.exists(instructions_file):
        print(f"Instructions file {instructions_file} not found.")
        return None
    
    with open(instructions_file, 'r') as file:
        lines = file.readlines()
    
    instructions = {}
    current_rwsd = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            current_rwsd = line[:-1]
            instructions[current_rwsd] = []
        elif line == "All":
            instructions[current_rwsd] = "All"
        else:
            if current_rwsd:
                # Support ranges like "0 - 6"
                if '-' in line:
                    start, end = map(int, line.split('-'))
                    instructions[current_rwsd].extend(range(start, end + 1))
                else:
                    instructions[current_rwsd].append(int(line))
    
    return instructions

def gather_rwav_offsets(rwsd_file_data):
    """Gathers the offsets of all RWAV files in the RWSD file."""
    rwav_signature = b'RWAV'
    rwav_offsets = []
    offset = 0

    while offset < len(rwsd_file_data):
        pos = rwsd_file_data.find(rwav_signature, offset)
        if pos == -1:
            break
        rwav_offsets.append(pos)
        offset = pos + 4

    return rwav_offsets

def extract_rwav_files(rwsd_file_data, rwav_offsets, extract_all=False, rwav_indices=None):
    """Extracts the specified RWAV files based on the instructions."""
    extracted_files = []

    if extract_all:
        rwav_indices = range(len(rwav_offsets))

    for index in rwav_indices:
        if index < len(rwav_offsets):
            start_offset = rwav_offsets[index]
            end_offset = rwav_offsets[index + 1] if index + 1 < len(rwav_offsets) else len(rwsd_file_data)
            rwav_data = rwsd_file_data[start_offset:end_offset]

            extracted_files.append((index, rwav_data))
        else:
            print(f"RWAV index {index} out of range, skipping.")

    return extracted_files

def delete_existing_rwav_files(output_folder):
    """Deletes all files that start with RWSD in the output folder."""
    if os.path.exists(output_folder):
        for file_name in os.listdir(output_folder):
            if file_name.startswith("RWSD"):
                file_path = os.path.join(output_folder, file_name)
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

def save_rwav_files(output_folder, rwsd_file_number, rwav_files):
    """Saves extracted RWAV files to disk without an extension."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, rwav_data in rwav_files:
        output_filename = os.path.join(output_folder, f"{rwsd_file_number}_Audio_{index}")
        with open(output_filename, 'wb') as out_file:
            out_file.write(rwav_data)
        print(f"Extracted RWAV file: {output_filename}")

def find_rwsd_file_by_prefix(folder_path, rwsd_file_prefix):
    """Finds a file in the folder that starts with the given RWSD file prefix followed by an underscore."""
    for file_name in os.listdir(folder_path):
        if file_name.startswith(rwsd_file_prefix + "_") and file_name.endswith((".brwsd")):
            return os.path.join(folder_path, file_name)
    return None

def process_rwsd_file(rwsd_file_path, rwav_instructions, extract_all):
    """Processes a single RWSD file according to the instructions."""
    with open(rwsd_file_path, 'rb') as f:
        rwsd_data = f.read()

    rwav_offsets = gather_rwav_offsets(rwsd_data)
    print(f"Found {len(rwav_offsets)} RWAV files in {rwsd_file_path}.")

    rwav_files = extract_rwav_files(rwsd_data, rwav_offsets, extract_all, rwav_instructions)
    return rwav_files

def delete_duplicate_rwav_files(output_folder):
    """Deletes RWAV files that are duplicates (same size and byte-for-byte match)."""
    files_by_size = {}
    duplicates_to_delete = []

    # Group files by size
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        file_size = os.path.getsize(file_path)
        if file_size not in files_by_size:
            files_by_size[file_size] = []
        files_by_size[file_size].append(file_path)

    # Check for duplicates by comparing file content
    for file_list in files_by_size.values():
        if len(file_list) > 1:
            # Compare each file with all others in the same size group
            for i in range(len(file_list)):
                for j in range(i + 1, len(file_list)):
                    if files_match(file_list[i], file_list[j]):
                        duplicates_to_delete.append(file_list[j])

    # Delete all duplicates except one
    unique_files = set()
    for duplicate in duplicates_to_delete:
        if duplicate not in unique_files:
            try:
                os.remove(duplicate)
                print(f"Deleted duplicate file: {duplicate}")
            except FileNotFoundError:
                print(f"File {duplicate} not found, possibly already deleted.")
            unique_files.add(duplicate)

def files_match(file1, file2):
    """Checks if two files match byte-for-byte."""
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

def setup_extraction(working_directory, current_project):
	# Read instructions from instructions.yaml file
	entries = read_project_instructions(working_directory, current_project)
	print(entries)

	# Create test.txt at the working_directory
	test_file_path = os.path.join(working_directory, "test.txt")
	try:
		with open(test_file_path, "w", encoding="utf-8") as f:
			f.write("This is a test file.\n")
			f.write(f"Loaded instructions: {entries}\n")
		print(f"test.txt created at: {test_file_path}")
	except Exception as e:
		print(f"Failed to create test.txt: {e}")