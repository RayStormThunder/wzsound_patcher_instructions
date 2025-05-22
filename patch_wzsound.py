import os
import shutil

from PySide6.QtWidgets import QApplication

def apply_wzsound_patch(working_directory, project_name, progress_ui=None, cancel_flag=None):
	import os

	# Paths
	source_brsar = os.path.join(working_directory, "ProgramData", "WZSound.brsar")
	target_folder = os.path.join(working_directory, "Projects", project_name, "ModifiedWZSoundSD")
	target_brsar = os.path.join(target_folder, "WZSound.brsar")
	patch_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")
	patch_file_path = None

	os.makedirs(target_folder, exist_ok=True)

	if not os.path.isfile(source_brsar):
		print(f"[ERROR] Missing source file: {source_brsar}")
		return

	shutil.copy2(source_brsar, target_brsar)
	print(f"[INFO] Copied WZSound.brsar to: {target_brsar}")

	# Find .patch file
	for file in os.listdir(patch_folder):
		if file.endswith(".patch"):
			patch_file_path = os.path.join(patch_folder, file)
			break

	if not patch_file_path or not os.path.isfile(patch_file_path):
		print(f"[ERROR] No .patch file found in {patch_folder}")
		return

	# Load all lines first so we can track progress
	with open(patch_file_path, "r") as patch_file:
		lines = [line.strip() for line in patch_file if line.strip() and ":" in line]

	total_lines = len(lines)
	processed = 0

	with open(target_brsar, "rb+") as brsar_file:
		for line in lines:
			if cancel_flag and cancel_flag.get('cancelled'):
				print("[CANCELLED] Patch operation aborted by user.")
				return False

			offset_hex, rwav_filename = line.split(":")
			offset = int(offset_hex, 16)
			rwav_path = os.path.join(patch_folder, rwav_filename)

			if not os.path.isfile(rwav_path):
				print(f"[WARNING] RWAV file not found: {rwav_path}, skipping.")
				continue

			with open(rwav_path, "rb") as rwav_file:
				rwav_data = rwav_file.read()

			brsar_file.seek(offset)
			brsar_file.write(rwav_data)
			print(f"[INFO] Inserted {rwav_filename} at {offset_hex}")

			# Update progress
			processed += 1
			if progress_ui:
				percent = int((processed / total_lines) * 100)
				progress_ui.progressBar.setValue(percent)
				if hasattr(progress_ui, "label_status"):
					progress_ui.label_status.setText(f"Patching {processed} of {total_lines}: {rwav_filename}")
				QApplication.processEvents()

	print("[SUCCESS] Patch applied to WZSound.brsar")
	return True
