import os
import struct

def extract_rwavs(file_path, project_name):
	# Build paths
	project_folder = os.path.join(file_path, "Projects", project_name)
	brwsd_path = os.path.join(project_folder, "your_project.brwsd")
	unmod_rwav_folder = os.path.join(project_folder, "UnmodifiedRwavs")
	mod_rwav_folder = os.path.join(project_folder, "ModifiedRwavs")

	# Check if BRWSD file exists
	if not os.path.exists(brwsd_path):
		print(f"BRWSD file not found: {brwsd_path}")
		return

	# Get list of filenames from UnmodifiedRwavs
	unmodified_names = sorted([
		f for f in os.listdir(unmod_rwav_folder)
		if os.path.isfile(os.path.join(unmod_rwav_folder, f))
	])

	# Create ModifiedRwavs folder if it doesn't exist
	os.makedirs(mod_rwav_folder, exist_ok=True)

	with open(brwsd_path, "rb") as f:
		data = f.read()

	offset = 0
	index = 0

	while offset < len(data) and index < len(unmodified_names):
		# Look for RWAV header
		if data[offset:offset+4] == b'RWAV':
			# Go forward 8 bytes from header
			size_offset = offset + 8
			if size_offset + 4 > len(data):
				print("Incomplete size data, skipping...")
				break

			size = struct.unpack(">I", data[size_offset:size_offset+4])[0]  # Big-endian uint32
			rwav_data = data[offset:offset+size]

			# Write the RWAV data to file
			output_filename = unmodified_names[index]
			output_path = os.path.join(mod_rwav_folder, output_filename)
			with open(output_path, "wb") as out_f:
				out_f.write(rwav_data)

			print(f"Extracted {output_filename} ({size} bytes)")
			index += 1
			offset += size  # Move to the next RWAV after this chunk
		else:
			offset += 1  # Move forward and keep searching

	if index < len(unmodified_names):
		print(f"Warning: Only {index} RWAV(s) found, but {len(unmodified_names)} files expected.")
	else:
		print("RWAV extraction completed.")

def check_modified_vs_unmodified(file_path, project_name):
	project_folder = os.path.join(file_path, "Projects", project_name)
	unmod_folder = os.path.join(project_folder, "UnmodifiedRwavs")
	mod_folder = os.path.join(project_folder, "ModifiedRwavs")

	too_big = []
	exact_match = []

	# Sort the list to maintain consistent order
	file_list = sorted(os.listdir(unmod_folder))
	audio_index = 0

	for filename in file_list:
		unmod_path = os.path.join(unmod_folder, filename)
		mod_path = os.path.join(mod_folder, filename)

		if not os.path.exists(mod_path):
			continue  # Skip if there's no modified version

		unmod_size = os.path.getsize(unmod_path)
		mod_size = os.path.getsize(mod_path)

		# Format: filename (Audio N)
		display_name = f"{filename} (Audio {audio_index})"

		if mod_size > unmod_size:
			too_big.append(display_name)
		else:
			with open(unmod_path, "rb") as f1, open(mod_path, "rb") as f2:
				if f1.read() == f2.read():
					exact_match.append(display_name)

		audio_index += 1

	return too_big, exact_match

