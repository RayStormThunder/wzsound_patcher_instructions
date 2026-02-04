import os
import re
import struct
from PySide6.QtWidgets import QApplication  # type: ignore

_AUDIO_LINE_RE = re.compile(r'^\s*Audio\[(\d+)\]\s*:\s*(.+?)\s*$')

def load_audio_map(txt_path: str) -> list[str]:
	"""
	Parses lines like:
	Audio[0]:Audio_006_000.rwav

	Returns a list where index i is the filename for Audio[i].
	Raises ValueError if indexes are missing or duplicated.
	"""
	if not os.path.isfile(txt_path):
		raise FileNotFoundError(f"Audio map not found: {txt_path}")

	index_to_name: dict[int, str] = {}

	with open(txt_path, "r", encoding="utf-8") as f:
		for raw in f:
			line = raw.strip()
			if not line:
				continue

			m = _AUDIO_LINE_RE.match(line)
			if not m:
				# Ignore junk lines (headers/comments) safely
				continue

			i = int(m.group(1))
			name = m.group(2)

			if i in index_to_name:
				raise ValueError(f"Duplicate Audio[{i}] in map: {txt_path}")

			index_to_name[i] = name

	if not index_to_name:
		raise ValueError(f"No Audio[...] lines found in map: {txt_path}")

	max_i = max(index_to_name.keys())

	# Ensure 0..max_i all exist (prevents silent shift)
	missing = [i for i in range(max_i + 1) if i not in index_to_name]
	if missing:
		raise ValueError(f"Missing Audio indices in map: {missing}")

	return [index_to_name[i] for i in range(max_i + 1)]

def extract_rwavs(file_path, project_name, progress_ui=None, cancel_flag=None):
	project_folder = os.path.join(file_path, "Projects", project_name)
	brwsd_path = os.path.join(project_folder, "your_project.brwsd")
	mod_rwav_folder = os.path.join(project_folder, "ModifiedRwavs")

	# Your map file: same stem as BRWSD in my earlier suggestion
	# If yours is named differently, change this one line.
	audio_map_path = os.path.join(project_folder, "your_project_AudioMap.txt")

	if not os.path.exists(brwsd_path):
		print(f"BRWSD file not found: {brwsd_path}")
		return

	try:
		mapped_names = load_audio_map(audio_map_path)
	except Exception as e:
		print(f"[ERROR] Failed to load audio map: {e}")
		return

	os.makedirs(mod_rwav_folder, exist_ok=True)

	with open(brwsd_path, "rb") as f:
		data = f.read()

	offset = 0
	index = 0
	total = len(mapped_names)

	while offset < len(data) and index < total:
		if cancel_flag and cancel_flag.get("cancelled"):
			print("RWAV extraction cancelled.")
			return

		if data[offset:offset+4] == b'RWAV':
			size_offset = offset + 8
			if size_offset + 4 > len(data):
				break

			size = struct.unpack(">I", data[size_offset:size_offset+4])[0]
			if size <= 0 or offset + size > len(data):
				print(f"[WARN] Bad RWAV size at offset 0x{offset:X}: {size}")
				break

			rwav_data = data[offset:offset+size]

			output_filename = mapped_names[index]
			out_path = os.path.join(mod_rwav_folder, output_filename)
			os.makedirs(os.path.dirname(out_path), exist_ok=True)  # just in case names contain subfolders

			with open(out_path, "wb") as out_f:
				out_f.write(rwav_data)

			index += 1
			offset += size
		else:
			offset += 1

		if progress_ui:
			progress_ui.progressBar.setValue(int((index / total) * 100))
			progress_ui.generated_text.setText("Extracting RWAVs")
			QApplication.processEvents()

	if index < total:
		print(f"Warning: Only {index} RWAV(s) found, expected {total}")

def check_modified_vs_unmodified(file_path, project_name):
	project_folder = os.path.join(file_path, "Projects", project_name)
	unmod_folder = os.path.join(project_folder, "UnmodifiedRwavsSD")
	mod_folder = os.path.join(project_folder, "ModifiedRwavs")
	audio_map_path = os.path.join(project_folder, "your_project_AudioMap.txt")

	too_big = []
	exact_match = []

	mapped_names = load_audio_map(audio_map_path)

	for audio_index, filename in enumerate(mapped_names):
		unmod_path = os.path.join(unmod_folder, filename)
		mod_path = os.path.join(mod_folder, filename)

		# If the unmodified file doesn't exist, skip gracefully
		if not os.path.exists(unmod_path):
			continue

		if not os.path.exists(mod_path):
			continue

		unmod_size = os.path.getsize(unmod_path)
		mod_size = os.path.getsize(mod_path)

		display_name = f"{filename} (Audio {audio_index})"

		if mod_size > unmod_size:
			too_big.append(display_name)
		else:
			with open(unmod_path, "rb") as f1, open(mod_path, "rb") as f2:
				if f1.read() == f2.read():
					exact_match.append(display_name)

	return too_big, exact_match
