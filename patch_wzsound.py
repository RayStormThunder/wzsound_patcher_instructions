import os
import shutil

def apply_wzsound_patch(working_directory, project_name):
	# Paths
	source_brsar = os.path.join(working_directory, "ProgramData", "WZSound.brsar")
	target_folder = os.path.join(working_directory, "Projects", project_name, "WZSound")
	target_brsar = os.path.join(target_folder, "WZSound.brsar")
	patch_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")
	patch_file_path = None

	# Ensure destination folder exists
	os.makedirs(target_folder, exist_ok=True)

	# Copy the original BRSAR file
	if not os.path.isfile(source_brsar):
		print(f"[ERROR] Missing source file: {source_brsar}")
		return
	shutil.copy2(source_brsar, target_brsar)
	print(f"[INFO] Copied WZSound.brsar to: {target_brsar}")

	# Find the .patch file
	for file in os.listdir(patch_folder):
		if file.endswith(".patch"):
			patch_file_path = os.path.join(patch_folder, file)
			break

	if not patch_file_path or not os.path.isfile(patch_file_path):
		print(f"[ERROR] No .patch file found in {patch_folder}")
		return

	# Read the patch file and apply patches
	with open(target_brsar, "rb+") as brsar_file:
		with open(patch_file_path, "r") as patch_file:
			for line in patch_file:
				line = line.strip()
				if not line or ":" not in line:
					continue

				offset_hex, rwav_filename = line.split(":")
				offset = int(offset_hex, 16)
				rwav_path = os.path.join(patch_folder, rwav_filename)

				if not os.path.isfile(rwav_path):
					print(f"[WARNING] RWAV file not found: {rwav_path}, skipping.")
					continue

				with open(rwav_path, "rb") as rwav_file:
					rwav_data = rwav_file.read()

				# Insert data at offset
				brsar_file.seek(offset)
				brsar_file.write(rwav_data)
				print(f"[INFO] Inserted {rwav_filename} at {offset_hex}")

	print("[SUCCESS] Patch applied to WZSound.brsar")
