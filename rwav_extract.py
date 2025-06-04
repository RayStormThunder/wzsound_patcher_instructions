import os
import struct
import yaml
import time
from collections import defaultdict
import hashlib

from PySide6.QtWidgets import QApplication

def delete_duplicate_rwavs(output_folder, progress_ui=None, cancel_flag=None):
	seen = {}
	duplicates_to_delete = []
	all_files = [f for f in os.listdir(output_folder) if f.endswith(".rwav")]
	total = len(all_files)
	processed = 0
	removed = 0

	for filename in all_files:
		if cancel_flag and cancel_flag.get("cancelled"):
			print("Duplicate cleanup cancelled by user.")
			return

		file_path = os.path.join(output_folder, filename)
		with open(file_path, 'rb') as f:
			data = f.read()
			hash_digest = hashlib.md5(data).hexdigest()

			if hash_digest in seen:
				duplicates_to_delete.append(file_path)
			else:
				seen[hash_digest] = filename

		processed += 1
		if progress_ui:
			percent = int((processed / total) * 100)
			progress_ui.progressBar.setValue(percent)
			if hasattr(progress_ui, "label_status"):
				progress_ui.label_status.setText(f"Checking for duplicates: {filename}")
			QApplication.processEvents()

	for file_path in duplicates_to_delete:
		try:
			os.remove(file_path)
			removed += 1
		except PermissionError:
			print(f"Could not delete (locked): {os.path.basename(file_path)}")

def parse_instruction_value(value):
  if value == 'All':
    return 'All'
  if '-' in value:
    start, end = map(int, value.split('-'))
    return list(range(start, end + 1))
  return [int(value)]

def extract_rwav_from_instructions(
	working_directory, project_folder, instructions, target_path, output="UnmodifiedRwavsSD",
	progress_ui=None, cancel_flag=None
):
	index_folder = target_path
	output_folder = os.path.join(working_directory, "Projects", project_folder, output)
	os.makedirs(output_folder, exist_ok=True)

	# Delete existing .rwav files
	for f in os.listdir(output_folder):
		if f.endswith(".rwav"):
			os.remove(os.path.join(output_folder, f))

	total_items = sum(
		1 for index_key in instructions for file_name in os.listdir(index_folder)
		if file_name.startswith(f"Index_{index_key.split('_')[1].zfill(3)}_") and file_name.endswith(".brwsd")
	)
	if total_items == 0:
		total_items = 1  # prevent division by zero

	progress = 0
	processed = 0

	for index_key, rule_list in instructions.items():
		index_number = index_key.split("_")[1].zfill(3)

		for file_name in os.listdir(index_folder):
			if not file_name.startswith(f"Index_{index_number}_") or not file_name.endswith(".brwsd"):
				continue

			if cancel_flag and cancel_flag.get("cancelled"):
				print("Extraction cancelled by user.")
				return

			full_path = os.path.join(index_folder, file_name)
			with open(full_path, 'rb') as f:
				data = f.read()

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

			extract_indices = set()
			for rule in rule_list:
				if rule == 'All':
					extract_indices = set(range(1, len(rwav_offsets) + 1))
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

				out_filename = f"Audio_{index_number}_{str(audio_number - 1).zfill(3)}.rwav"
				out_path = os.path.join(output_folder, out_filename)

				with open(out_path, 'wb') as out_f:
					out_f.write(extracted_data)

			processed += 1
			if progress_ui:
				progress = int((processed / total_items) * 100)
				progress_ui.progressBar.setValue(progress)
				if hasattr(progress_ui, "label_status"):
					progress_ui.label_status.setText(f"Extracting: {file_name}")
				QApplication.processEvents()


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

def setup_extraction(working_directory, current_project, progress_ui=None, cancel_flag=None):
	entries = read_project_instructions(working_directory, current_project)
	instructions = merge_yaml_rules(working_directory, entries)
	index_folder = os.path.join(working_directory, "IndexesSD")
	extract_rwav_from_instructions(working_directory, current_project, instructions, index_folder, progress_ui=progress_ui, cancel_flag=cancel_flag)

	if progress_ui:
		progress_ui.generated_text.setText("Removing duplicates...")
		progress_ui.progressBar.setValue(0)
		QApplication.processEvents()

	output_folder = os.path.join(working_directory, "Projects", current_project, "UnmodifiedRwavsSD")
	delete_duplicate_rwavs(output_folder, progress_ui=progress_ui, cancel_flag=cancel_flag)

def setup_extraction_converted(working_directory, current_project, progress_ui=None, cancel_flag=None):
	if progress_ui:
		progress_ui.generated_text.setText("Reading patch instructions (Converted)...")
		QApplication.processEvents()

	entries = read_project_instructions(working_directory, current_project)
	instructions = merge_yaml_rules(working_directory, entries)

	if progress_ui:
		progress_ui.generated_text.setText("Extracting RWAVs from Modified Indexes...")
		progress_ui.progressBar.setValue(0)
		QApplication.processEvents()

	index_folder = os.path.join(working_directory, "Projects", current_project, "Indexes")
	extract_rwav_from_instructions(
		working_directory,
		current_project,
		instructions,
		index_folder,
		output="ModifiedRwavs",
		progress_ui=progress_ui,
		cancel_flag=cancel_flag
	)

	# Cleanup step
	unmodified_path = os.path.join(working_directory, "Projects", current_project, "UnmodifiedRwavsSD")
	modified_path = os.path.join(working_directory, "Projects", current_project, "ModifiedRwavs")

	try:
		unmodified_files = set(os.listdir(unmodified_path))
		for filename in os.listdir(modified_path):
			if filename not in unmodified_files:
				file_to_delete = os.path.join(modified_path, filename)
				os.remove(file_to_delete)
	except Exception as e:
		print(f"[ERROR] During cleanup of ModifiedRwavs: {e}")

	if progress_ui:
		progress_ui.generated_text.setText("Converted extraction complete.")
		progress_ui.progressBar.setValue(100)
		QApplication.processEvents()



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

def setup_extraction_HD(working_directory, current_project, progress_ui=None, cancel_flag=None):
	entries = read_project_instructions(working_directory, current_project)

	if progress_ui and hasattr(progress_ui, "generated_text"):
		progress_ui.generated_text.setText("Merging instructions for HD extraction...")
		QApplication.processEvents()

	instructions = merge_yaml_rules(working_directory, entries)

	instructions = adjust_instructions_for_extras(instructions)

	index_folder = os.path.join(working_directory, "IndexesHD")

	if progress_ui and hasattr(progress_ui, "generated_text"):
		progress_ui.generated_text.setText("Extracting RWAV files from HD indexes...")
		QApplication.processEvents()

	extract_rwav_from_instructions(
		working_directory,
		current_project,
		instructions,
		index_folder,
		"UnmodifiedRwavsHD",
		progress_ui=progress_ui,
		cancel_flag=cancel_flag
	)

	if progress_ui and hasattr(progress_ui, "generated_text"):
		progress_ui.generated_text.setText("Removing duplicate RWAV files...")
		if hasattr(progress_ui, "progressBar"):
			progress_ui.progressBar.setValue(0)
		QApplication.processEvents()

	output_folder = os.path.join(working_directory, "Projects", current_project, "UnmodifiedRwavsHD")
	delete_duplicate_rwavs(output_folder, progress_ui=progress_ui, cancel_flag=cancel_flag)


