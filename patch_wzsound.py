import os
import shutil
from PySide6.QtWidgets import QApplication

def apply_wzsound_patch(working_directory, project_name, progress_ui=None, cancel_flag=None):
	# Base folders
	programdata_dir = os.path.join(working_directory, "ProgramData")
	source_wzsound = os.path.join(programdata_dir, "WZSound.brsar")

	target_root = os.path.join(working_directory, "Projects", project_name, "ModifiedWZSoundSD")
	patch_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")

	os.makedirs(target_root, exist_ok=True)

	# Find .patch file
	patch_file_path = None
	for file in os.listdir(patch_folder):
		if file.lower().endswith(".patch"):
			patch_file_path = os.path.join(patch_folder, file)
			break

	if not patch_file_path or not os.path.isfile(patch_file_path):
		print(f"[ERROR] No .patch file found in {patch_folder}")
		return False

	# Load lines
	with open(patch_file_path, "r", encoding="utf-8") as patch_file:
		raw_lines = [line.strip() for line in patch_file if line.strip()]

	# Parse lines: target_rel|OFFSET:RWAV
	parsed = []
	for line in raw_lines:
		if "|" not in line or ":" not in line:
			continue
		target_rel, rest = line.split("|", 1)
		offset_hex, rwav_filename = rest.split(":", 1)
		target_rel = target_rel.strip().replace("/", os.sep).replace("\\", os.sep)
		offset_hex = offset_hex.strip()
		rwav_filename = rwav_filename.strip()
		if not target_rel or not offset_hex or not rwav_filename:
			continue
		parsed.append((target_rel, offset_hex, rwav_filename))

	if not parsed:
		print("[ERROR] Patch file had no valid lines.")
		return False

	# Group by target_rel so we can copy/open each target once
	by_target = {}
	for target_rel, offset_hex, rwav_filename in parsed:
		by_target.setdefault(target_rel, []).append((offset_hex, rwav_filename))

	# Ensure base target files exist (copy from ProgramData into project output)
	def ensure_target_copied(target_rel: str) -> str | None:
		"""
		Returns absolute path to the project copy that will be patched.
		Copies from ProgramData/<target_rel> into Projects/<project>/ModifiedWZSoundSD/<target_rel>.
		"""
		src = os.path.join(programdata_dir, target_rel)
		dst = os.path.join(target_root, target_rel)

		# Make parent folder (handles demo/)
		os.makedirs(os.path.dirname(dst), exist_ok=True)

		if not os.path.isfile(src):
			print(f"[ERROR] Missing source target file: {src}")
			return None

		# Always refresh copy (overwrite)
		shutil.copy2(src, dst)
		return dst

	# Copy all needed targets first (WZSound + demo files)
	target_map = {}
	for target_rel in by_target.keys():
		dst_path = ensure_target_copied(target_rel)
		if dst_path:
			target_map[target_rel] = dst_path

	if not target_map:
		print("[ERROR] No target files could be copied.")
		return False

	# Progress tracking across all patches
	total_patches = sum(len(v) for v in by_target.values())
	processed = 0

	# Apply patches per target file
	for target_rel, patches in by_target.items():
		if cancel_flag and cancel_flag.get("cancelled"):
			print("[CANCELLED] Patch operation aborted by user.")
			return False

		target_brsar = target_map.get(target_rel)
		if not target_brsar:
			continue

		# Sort by offset (nice/consistent)
		patches.sort(key=lambda x: int(x[0], 16))

		with open(target_brsar, "rb+") as brsar_file:
			for offset_hex, rwav_filename in patches:
				if cancel_flag and cancel_flag.get("cancelled"):
					print("[CANCELLED] Patch operation aborted by user.")
					return False

				try:
					offset = int(offset_hex, 16)
				except ValueError:
					continue

				rwav_path = os.path.join(patch_folder, rwav_filename)
				if not os.path.isfile(rwav_path):
					print(f"[WARNING] RWAV file not found: {rwav_path}, skipping.")
					continue

				with open(rwav_path, "rb") as rwav_file:
					rwav_data = rwav_file.read()

				brsar_file.seek(offset)
				brsar_file.write(rwav_data)

				processed += 1
				if progress_ui:
					percent = int((processed / total_patches) * 100) if total_patches else 0
					progress_ui.progressBar.setValue(percent)
					if hasattr(progress_ui, "label_status"):
						# show the target too
						progress_ui.label_status.setText(
							f"Patching {processed} of {total_patches}: {os.path.basename(target_rel)} | {rwav_filename}"
						)
					QApplication.processEvents()

	print(f"[SUCCESS] Patch applied. Output folder:\n{target_root}")
	return True
