import os
import struct
import yaml
import time
from collections import defaultdict
import hashlib

def delete_duplicate_rwavs(output_folder):
    """Deletes duplicate .rwav files based on exact byte match."""
    seen = {}
    duplicates_to_delete = []

    for filename in os.listdir(output_folder):
        if not filename.endswith(".rwav"):
            continue
        file_path = os.path.join(output_folder, filename)

        with open(file_path, 'rb') as f:
            data = f.read()
            hash_digest = hashlib.md5(data).hexdigest()

            if hash_digest in seen:
                duplicates_to_delete.append(file_path)
                print(f"Marked duplicate: {filename} (same as {seen[hash_digest]})")
            else:
                seen[hash_digest] = filename

    # All files are closed at this point and safe to delete
    removed = 0
    for file_path in duplicates_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted duplicate: {os.path.basename(file_path)}")
            removed += 1
        except PermissionError:
            print(f"Could not delete (locked): {os.path.basename(file_path)}")

    if removed == 0:
        print("No duplicates removed.")
    else:
        print(f"Removed {removed} duplicate RWAV files.")

def parse_instruction_value(value):
  if value == 'All':
    return 'All'
  if '-' in value:
    start, end = map(int, value.split('-'))
    return list(range(start, end + 1))
  return [int(value)]

def extract_rwav_from_instructions(working_directory, project_folder, instructions, target_path, output="UnmodifiedRwavs"):
  # Indexes folder path
  index_folder = target_path

  # Output folder
  output_folder = os.path.join(working_directory, "Projects", project_folder, output)
  os.makedirs(output_folder, exist_ok=True)

  # Delete all existing .rwav files
  for f in os.listdir(output_folder):
    if f.endswith(".rwav"):
      os.remove(os.path.join(output_folder, f))

  for index_key, rule_list in instructions.items():
    index_number = index_key.split("_")[1].zfill(3)

    # Match files like Index_015_001.brwsd
    for file_name in os.listdir(index_folder):
      if file_name.startswith(f"Index_{index_number}_") and file_name.endswith(".brwsd"):
        full_path = os.path.join(index_folder, file_name)
        with open(full_path, 'rb') as f:
          data = f.read()

        # Find all RWAV headers
        rwav_offsets = []
        pos = 0
        while pos < len(data):
          pos = data.find(b'RWAV', pos)
          if pos == -1:
            break
          rwav_offsets.append(pos)
          pos += 4

        if not rwav_offsets:
          continue

        # Build list of audio numbers to extract
        extract_indices = set()
        for rule in rule_list:
          if rule == 'All':
            extract_indices = set(range(1, len(rwav_offsets) + 1))  # 1-based indexing
            break
          extract_indices.update(i + 1 for i in parse_instruction_value(rule))

        for i, offset in enumerate(rwav_offsets):
          audio_number = i + 1
          if audio_number not in extract_indices:
            continue

          size_offset = offset + 8
          if size_offset + 4 > len(data):
            continue

          rwav_size = struct.unpack(">I", data[size_offset:size_offset + 4])[0]
          extracted_data = data[offset:offset + rwav_size]

          # Save with audio_number - 1
          out_filename = f"Audio_{index_number}_{str(audio_number - 1).zfill(3)}.rwav"
          out_path = os.path.join(output_folder, out_filename)

          with open(out_path, 'wb') as out_f:
            out_f.write(extracted_data)

          print(f"Extracted {out_filename}")

def parse_range(value):
    if isinstance(value, int):
        return [value]
    if isinstance(value, str):
        if '-' in value:
            start, end = map(int, value.split('-'))
            return list(range(start, end + 1))
        else:
            return [int(value)]
    return []

def compress_range(nums):
    if 'All' in nums:
        return ['All']
    nums = sorted(set(nums))
    ranges = []
    start = end = nums[0]

    for n in nums[1:]:
        if n == end + 1:
            end = n
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start} - {end}")
            start = end = n

    # Append last
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start} - {end}")

    return ranges

def sanitize_yaml_tabs(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    # Replace tabs with 4 spaces
    lines = [line.replace('\t', '    ') for line in lines]

    with open(path, 'w') as f:
        f.writelines(lines)


def merge_yaml_rules(filepath, filenames):
    merged = defaultdict(set)

    for raw_name in filenames:
        # Convert "Map Rules 1" → "Map_Rules_1.yaml"
        clean_name = raw_name.replace(" ", "_") + ".yaml"
        full_path = os.path.join(filepath, "Instructions", clean_name)

        if not os.path.exists(full_path):
            print(f"Warning: {clean_name} not found at {full_path}")
            continue

        sanitize_yaml_tabs(full_path)
        with open(full_path, 'r') as f:
            data = yaml.safe_load(f) or {}

        for key, values in data.items():
            if 'All' in values:
                merged[key] = {'All'}
            elif 'All' not in merged[key]:
                for v in values:
                    merged[key].update(parse_range(v))

    # Compress into ranges
    final_merged = {}
    for key, values in merged.items():
        final_merged[key] = compress_range(values)

    # Sort Index_# keys by number
    final_sorted = dict(sorted(
        final_merged.items(),
        key=lambda x: int(x[0].split('_')[1])
    ))
    return final_sorted


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

def setup_extraction(working_directory, current_project):
    # Read instructions from instructions.yaml file
    entries = read_project_instructions(working_directory, current_project)
    print(entries)
      
    instructions = merge_yaml_rules(working_directory, entries)
    print(instructions)
    
    index_folder = os.path.join(working_directory, "Indexes")

    extract_rwav_from_instructions(working_directory, current_project, instructions, index_folder)

    output_folder = os.path.join(working_directory, "Projects", current_project, "UnmodifiedRwavs")
    delete_duplicate_rwavs(output_folder)

def setup_extraction_converted(working_directory, current_project):
    # Read instructions from instructions.yaml file
    entries = read_project_instructions(working_directory, current_project)
    print(entries)
      
    instructions = merge_yaml_rules(working_directory, entries)
    print(instructions)

    index_folder = os.path.join(working_directory, "Projects", current_project, "Indexes")

    extract_rwav_from_instructions(working_directory, current_project, instructions, index_folder, "ModifiedRwavs")

def adjust_instructions_for_extras(instructions: dict) -> dict:
	# Map of Index_XYZ to list of extra RWAVs to remove
	extras = {
		"Index_013": [158, 192],
		"Index_025": [159, 193],
	}

	adjusted = {}

	for key, ranges in instructions.items():
		extra_list = extras.get(key, [])
		if not extra_list:
			adjusted[key] = ranges
			continue

		flattened = []

		# Flatten all ranges into a list of integers
		for r in ranges:
			if isinstance(r, int):
				flattened.append(r)
			elif isinstance(r, str) and " - " in r:
				start, end = map(int, r.split(" - "))
				flattened.extend(range(start, end + 1))
			else:
				flattened.append(int(r))

		flattened = sorted(flattened)
		new_values = []

		for i, val in enumerate(flattened):
			# Skip if val is one of the extras
			if val in extra_list:
				continue

			# Count how many extras came before this value
			offset = sum(1 for e in extra_list if e <= val)
			new_values.append(val + offset)

		# Re-group into ranges
		grouped = []
		if new_values:
			start = prev = new_values[0]
			for val in new_values[1:]:
				if val == prev + 1:
					prev = val
				else:
					if start == prev:
						grouped.append(start)
					else:
						grouped.append(f"{start} - {prev}")
					start = prev = val
			# Add final group
			if start == prev:
				grouped.append(start)
			else:
				grouped.append(f"{start} - {prev}")

		adjusted[key] = grouped

	return adjusted

def setup_extraction_HD(working_directory, current_project):
	# Step 1: Read instructions
	entries = read_project_instructions(working_directory, current_project)
	print(entries)

	# Step 2: Merge YAML rules
	instructions = merge_yaml_rules(working_directory, entries)
	print(instructions)

	# Step 3: Adjust instructions for known RWAV offsets
	instructions = adjust_instructions_for_extras(instructions)

	# Step 4: Extract based on fixed instructions
	index_folder = os.path.join(working_directory, "IndexesHD")
	extract_rwav_from_instructions(working_directory, current_project, instructions, index_folder, "UnmodifiedRwavsHD")

	# Step 5: Cleanup
	output_folder = os.path.join(working_directory, "Projects", current_project, "UnmodifiedRwavsHD")
	delete_duplicate_rwavs(output_folder)
