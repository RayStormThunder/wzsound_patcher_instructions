import os
import shutil

from PySide6.QtWidgets import QApplication

def create_patch_file(working_directory, project_name, too_big_list, exact_match_list, progress_ui=None, cancel_flag=None):
	import os
	instructions = []

	def clean_filename(name):
		return name.split(" ")[0]

	unmod_folder = os.path.join(working_directory, "Projects", project_name, "UnmodifiedRwavsSD")
	mod_folder = os.path.join(working_directory, "Projects", project_name, "ModifiedRwavs")
	wzsound_path = os.path.join(working_directory, "ProgramData", "WZSound.brsar")
	output_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")
	output_file = os.path.join(output_folder, "wzsound_instructions.patch")

	if not os.path.exists(wzsound_path):
		print(f"Missing file: {wzsound_path}")
		return

	with open(wzsound_path, "rb") as wz_file:
		wz_data = wz_file.read()

	skip_files = {clean_filename(name) for name in too_big_list}
	files_to_search = [f for f in sorted(os.listdir(unmod_folder)) if f not in skip_files]
	files_total = len(files_to_search)
	files_done = 0

	for filename in files_to_search:
		if cancel_flag and cancel_flag.get('cancelled'):
			print("Operation cancelled by user.")
			return False  # Indicate cancelled

		unmod_path = os.path.join(unmod_folder, filename)
		if not os.path.isfile(unmod_path):
			continue

		with open(unmod_path, "rb") as f:
			chunk = f.read()

		start = 0
		while True:
			index = wz_data.find(chunk, start)
			if index == -1:
				break
			hex_index = f"{index:08X}"
			instructions.append((hex_index, filename))
			start = index + 1

		files_done += 1

		if progress_ui:
			percent = int((files_done / files_total) * 100)
			progress_ui.progressBar.setValue(percent)
			QApplication.processEvents()

	instructions.sort(key=lambda x: int(x[0], 16))
	os.makedirs(output_folder, exist_ok=True)

	with open(output_file, "w") as out_file:
		for hex_index, filename in instructions:
			out_file.write(f"{hex_index}:{filename}\n")

	print(f"WZSound patch instructions saved to: {output_file}")

	# Only copy modified files that:
	# 1. Exist in unmodified folder
	# 2. Are smaller than the corresponding unmodified file
	for filename in sorted(os.listdir(mod_folder)):
		mod_path = os.path.join(mod_folder, filename)
		unmod_path = os.path.join(unmod_folder, filename)

		if not os.path.isfile(mod_path) or not os.path.isfile(unmod_path):
			continue

		if os.path.getsize(mod_path) < os.path.getsize(unmod_path):
			dst_path = os.path.join(output_folder, filename)
			shutil.copy2(mod_path, dst_path)

	print(f"Filtered ModifiedRwavs copied to: {output_folder}")
	return True  # Indicate completed successfully
