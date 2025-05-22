import os
import struct
import hashlib

from PySide6.QtWidgets import QApplication

def extract_rwar_files(input_file, output_filepath, target_folder="Indexes", progress_ui=None, cancel_flag=None):
	output_folder = os.path.join(output_filepath, target_folder)
	os.makedirs(output_folder, exist_ok=True)

	with open(input_file, "rb") as f:
		data = f.read()

	# Count how many RWARs total (for progress bar)
	total_rwars = data.count(b'RWAR')
	if total_rwars == 0:
		total_rwars = 1  # Avoid division by zero

	index = 0
	file_id = 0
	total_found = 0
	processed = 0

	while index < len(data):
		if cancel_flag and cancel_flag.get("cancelled"):
			print("RWAR extraction cancelled by user.")
			return

		index = data.find(b'RWAR', index)
		if index == -1:
			break

		size_offset = index + 8
		if size_offset + 4 > len(data):
			print(f"Reached end of file while reading size for RWAR at {index}")
			break

		file_size = struct.unpack(">I", data[size_offset:size_offset + 4])[0]
		end_offset = index + file_size
		if end_offset > len(data):
			print(f"File size at {index} exceeds file bounds. Skipping.")
			index += 4
			continue

		chunk = data[index:end_offset]
		rwav_count = chunk.count(b'RWAV')

		if rwav_count > 0:
			filename = f"Index_{file_id:03}_{rwav_count:03}.brwsd"
			output_path = os.path.join(output_folder, filename)
			with open(output_path, "wb") as out_file:
				out_file.write(chunk)
			print(f"Extracted: {filename} with {rwav_count} RWAV(s)")
			file_id += 1
			total_found += 1
		else:
			print(f"Skipped RWAR at {index} (no RWAV found)")

		index = end_offset
		processed += 1

		if progress_ui:
			progress = int((processed / total_rwars) * 100)
			progress_ui.progressBar.setValue(progress)
			QApplication.processEvents()

	print(f"\nTotal RWAR files with RWAV extracted: {total_found}")

	# Reset progress before duplicate check
	if progress_ui:
		progress_ui.progressBar.setValue(0)
		if hasattr(progress_ui, "generated_text"):
			progress_ui.generated_text.setText("Removing duplicate RWAR files...")
		QApplication.processEvents()

	remove_duplicate_files(output_folder, progress_ui, cancel_flag)

def remove_duplicate_files(folder, progress_ui=None, cancel_flag=None):
	print("\nChecking for duplicate files...")
	hash_map = {}
	deleted = 0

	all_files = [f for f in os.listdir(folder) if f.endswith(".brwsd")]
	total = len(all_files)
	processed = 0

	for filename in all_files:
		if cancel_flag and cancel_flag.get("cancelled"):
			print("Duplicate cleanup cancelled by user.")
			return

		full_path = os.path.join(folder, filename)

		with open(full_path, "rb") as f:
			file_data = f.read()
			file_hash = hashlib.md5(file_data).hexdigest()

		if file_hash in hash_map:
			print(f"Duplicate found: {filename} is a copy of {hash_map[file_hash]}. Deleting...")
			os.remove(full_path)
			deleted += 1
		else:
			hash_map[file_hash] = filename

		processed += 1
		if progress_ui:
			percent = int((processed / total) * 100)
			progress_ui.progressBar.setValue(percent)
			if hasattr(progress_ui, "label_status"):
				progress_ui.label_status.setText(f"Checking: {filename}")
			QApplication.processEvents()

	print(f"Duplicate removal complete. {deleted} files deleted.")

