import os
import shutil
from PySide6.QtWidgets import QApplication

def create_patch_file(working_directory, project_name, too_big_list, exact_match_list, progress_ui=None, cancel_flag=None):
	instructions = []

	def clean_filename(name):
		return name.split(" ")[0]

	unmod_folder = os.path.join(working_directory, "Projects", project_name, "UnmodifiedRwavsSD")
	mod_folder = os.path.join(working_directory, "Projects", project_name, "ModifiedRwavs")

	programdata_dir = os.path.join(working_directory, "ProgramData")
	wzsound_path = os.path.join(programdata_dir, "WZSound.brsar")
	demo_dir = os.path.join(programdata_dir, "demo")

	output_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")
	output_file = os.path.join(output_folder, "wzsound_instructions.patch")

	# Build list of target brsar files to search
	target_files = []
	if os.path.exists(wzsound_path):
		target_files.append(wzsound_path)

	if os.path.isdir(demo_dir):
		for fn in os.listdir(demo_dir):
			if fn.lower().endswith(".brsar"):
				target_files.append(os.path.join(demo_dir, fn))

	if not target_files:
		print("No target .brsar files found in ProgramData (WZSound.brsar or ProgramData/demo/*.brsar).")
		return False

	# Prepare which RWAVs to search for
	skip_files = {clean_filename(name) for name in too_big_list}
	files_to_search = [f for f in sorted(os.listdir(unmod_folder)) if f.lower().endswith(".rwav") and f not in skip_files]

	# Preload all RWAV chunks (so we don't re-open RWAV files per target brsar)
	chunks = []
	for filename in files_to_search:
		unmod_path = os.path.join(unmod_folder, filename)
		if not os.path.isfile(unmod_path):
			continue
		with open(unmod_path, "rb") as f:
			chunks.append((filename, f.read()))

	if not chunks:
		print("No unmodified RWAVs to search (after filtering too_big_list).")
		return False

	# Progress total = (#targets * #chunks)
	total_steps = len(target_files) * len(chunks)
	done_steps = 0

	for target_path in target_files:
		if cancel_flag and cancel_flag.get('cancelled'):
			print("Operation cancelled by user.")
			return False

		# Read brsar data once
		try:
			with open(target_path, "rb") as f:
				target_data = f.read()
		except Exception as e:
			print(f"Failed to read target: {target_path} -> {e}")
			continue

		# Store relative path inside ProgramData so patch is portable
		# e.g. "WZSound.brsar" or "demo\\CutsceneA.brsar"
		target_rel = os.path.relpath(target_path, programdata_dir)

		for filename, chunk in chunks:
			if cancel_flag and cancel_flag.get('cancelled'):
				print("Operation cancelled by user.")
				return False

			start = 0
			while True:
				index = target_data.find(chunk, start)
				if index == -1:
					break
				hex_index = f"{index:08X}"
				instructions.append((target_rel, hex_index, filename))
				start = index + 1

			done_steps += 1
			if progress_ui:
				percent = int((done_steps / total_steps) * 100) if total_steps else 0
				progress_ui.progressBar.setValue(percent)
				if hasattr(progress_ui, "label_status"):
					progress_ui.label_status.setText(f"Searching: {os.path.basename(target_path)} | {filename}")
				QApplication.processEvents()

	# Sort: target then offset
	instructions.sort(key=lambda x: (x[0].lower(), int(x[1], 16)))

	os.makedirs(output_folder, exist_ok=True)

	# Cleanup old .rwav and .patch files
	for file in os.listdir(output_folder):
		if file.endswith(".rwav") or file.endswith(".patch"):
			try:
				os.remove(os.path.join(output_folder, file))
			except Exception as e:
				print(f"Failed to remove {file}: {e}")

	# Copy modified RWAVs (only if smaller than unmodified)
	for filename in sorted(os.listdir(mod_folder)):
		mod_path = os.path.join(mod_folder, filename)
		unmod_path = os.path.join(unmod_folder, filename)

		if not os.path.isfile(mod_path) or not os.path.isfile(unmod_path):
			continue

		if os.path.getsize(mod_path) < os.path.getsize(unmod_path):
			shutil.copy2(mod_path, os.path.join(output_folder, filename))

	# Write patch file with target included
	with open(output_file, "w", encoding="utf-8") as out_file:
		for target_rel, hex_index, filename in instructions:
			# Only write lines for RWAVs we actually copied into output_folder
			if os.path.exists(os.path.join(output_folder, filename)):
				out_file.write(f"{target_rel}|{hex_index}:{filename}\n")

	return True
