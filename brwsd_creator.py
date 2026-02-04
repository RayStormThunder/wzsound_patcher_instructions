import os
import struct
import shutil
import re

from PySide6.QtWidgets import QApplication

_AUDIO_LINE_RE = re.compile(r'^\s*Audio\[(\d+)\]\s*:\s*(.+?)\s*$')

def pad_to_multiple_of(value, multiple):
    """Pads a value to the next multiple of 'multiple'."""
    remainder = value % multiple
    return value if remainder == 0 else value + (multiple - remainder)

def write_rwar_header(brwsd_file, tabl_size, data_offset, rwav_total_size):
    """Writes the RWAR header to the brwsd file."""
    brwsd_file.write(b'RWAR')  # 0x0 to 0x3
    brwsd_file.write(struct.pack('>I', 0xFEFF0100))  # 0x4 to 0x7 (constant value)
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x8 to 0xB (total file size)
    brwsd_file.write(struct.pack('>I', 0x200002))  # 0xC to 0xF (constant value)

    brwsd_file.write(struct.pack('>I', 0x20))  # 0x10 to 0x13 (fixed number 20)
    tabl_size = (tabl_size + 15) // 16 * 16 #PATCH 1.3.3 - Didn't take in to account padding to fill to a clean number eg. 0x10
    brwsd_file.write(struct.pack('>I', tabl_size))  # 0x14 to 0x17 (length of the TABL section)
    brwsd_file.write(struct.pack('>I', tabl_size + 0x20))  # 0x18 to 0x1B (TABL length + 0x20)
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x1C to 0x1F (RWAV section size)

def write_tabl_header(brwsd_file, rwav_files_info):
    """Writes the TABL section header."""
    brwsd_file.write(b'TABL')  # 0x0 to 0x3
    tabl_size = 0x10 + len(rwav_files_info) * 12  # Each RWAV adds 12 bytes to TABL
    tabl_size = (tabl_size + 15) // 16 * 16 #PATCH 1.3.3 - Didn't take in to account padding to fill to a clean number eg. 0x10
    brwsd_file.write(struct.pack('>I', tabl_size))  # 0x4 to 0x7 (Table size)
    brwsd_file.write(struct.pack('>I', len(rwav_files_info)))  # 0x8 to 0xB (RWAV count)

    # Write the [01000000], offset, and size for each RWAV
    for rwav_info in rwav_files_info:
        brwsd_file.write(b'\x01\x00\x00\x00')  # Constant value [01000000]
        brwsd_file.write(struct.pack('>I', rwav_info['offset']))  # Offset
        brwsd_file.write(struct.pack('>I', rwav_info['size']))  # Size

    # Pad the TABL section to be a multiple of 16 bytes
    current_pos = brwsd_file.tell()
    padded_size = pad_to_multiple_of(current_pos, 16)
    padding_needed = padded_size - current_pos
    if padding_needed > 0:
        brwsd_file.write(b'\x00' * padding_needed)
    brwsd_file.write(b'\00' * (0x10))  # 0x20 - 8 already written bytes

def write_data_section(brwsd_file, rwav_total_size):
    """Writes the DATA section to the brwsd file."""
    brwsd_file.write(b'DATA')  # 0x0 to 0x3
    brwsd_file.write(struct.pack('>I', rwav_total_size))  # 0x4 to 0x7 (RWAV total size)

def append_and_replace_base_blank(base_blank_file, original_file):
    """Appends the original file's data to BaseBlankFile.brwsd and replaces the original."""
    # First, copy the BaseBlankFile.brwsd to the folder where the combined file is
    temp_base_blank = original_file + "_temp"
    shutil.copy(base_blank_file, temp_base_blank)
    
    # Append original file's data to the temp copy of BaseBlankFile.brwsd
    with open(temp_base_blank, 'ab') as blank_file:
        with open(original_file, 'rb') as orig_file:
            blank_file.write(orig_file.read())

    # Delete the original combined file
    os.remove(original_file)

    # Rename the temporary BaseBlankFile.brwsd to the original file name
    os.rename(temp_base_blank, original_file)

def combine_rwav_files_to_brwsd(rwav_folder, mod_folder, output_file):
	"""Combines RWAV files, using modified versions from mod_folder if available.
	Sort order matches _list_rwavs_in_build_order(): natural filename order.
	"""
	rwav_files = [
		f for f in os.listdir(rwav_folder)
		if os.path.isfile(os.path.join(rwav_folder, f)) and f.lower().endswith(".rwav")
	]
	rwav_files.sort(key=_natural_key)

	rwav_files_info = []
	current_offset = 0x20
	rwav_total_size = 0

	# Calculate offsets and sizes
	for rwav_file in rwav_files:
		# Prefer modified version if it exists
		modified_path = os.path.join(mod_folder, rwav_file)
		original_path = os.path.join(rwav_folder, rwav_file)
		file_path = modified_path if os.path.isfile(modified_path) else original_path

		rwav_size = os.path.getsize(file_path)
		rwav_files_info.append({
			'name': rwav_file,
			'offset': current_offset,
			'size': rwav_size,
			'path': file_path
		})
		current_offset += rwav_size
		rwav_total_size += rwav_size

	rwav_total_size += 32
	tabl_size = 0x10 + len(rwav_files_info) * 12
	data_offset = pad_to_multiple_of(0x40 + tabl_size, 16)

	with open(output_file, 'wb') as brwsd_file:
		# Write headers
		write_rwar_header(brwsd_file, tabl_size, data_offset, rwav_total_size)
		write_tabl_header(brwsd_file, rwav_files_info)
		write_data_section(brwsd_file, rwav_total_size)

		# Move to data offset
		brwsd_file.seek(data_offset)

		# Write RWAV data in the exact same order
		for rwav_info in rwav_files_info:
			with open(rwav_info['path'], 'rb') as f:
				brwsd_file.write(f.read())

	print(f"Created {output_file}")

def _natural_key(s: str):
	# Sort like: 1,2,10 instead of 1,10,2 (falls back gracefully)
	return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def _list_rwavs_in_build_order(unmod_folder: str, mod_folder: str):
	unmod_names = [
		f for f in os.listdir(unmod_folder)
		if os.path.isfile(os.path.join(unmod_folder, f)) and f.lower().endswith((".rwav", ".brwav", ".wav"))
	]
	unmod_names.sort(key=_natural_key)

	result = []
	for i, name in enumerate(unmod_names):
		mod_path = os.path.join(mod_folder, name)
		unmod_path = os.path.join(unmod_folder, name)

		if os.path.isfile(mod_path):
			used_path = mod_path
			source = "Modified"
		else:
			used_path = unmod_path
			source = "Unmodified"

		result.append({
			"index": i,
			"used_path": used_path,
			"display_name": name,
			"source": source,
		})

	return result

def _write_audio_manifest_txt(manifest_path: str, build_list):
	os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

	with open(manifest_path, "w", encoding="utf-8") as f:
		for entry in build_list:
			f.write(f'Audio[{entry["index"]}]:{entry["display_name"]}\n')

def build_brwsd_from_unmodified_rwavs(working_directory, project_folder, progress_ui=None, cancel_flag=None):
	unmod_folder = os.path.join(working_directory, "Projects", project_folder, "UnmodifiedRwavsSD")
	mod_folder = os.path.join(working_directory, "Projects", project_folder, "ModifiedRwavs")
	output_brwsd = os.path.join(working_directory, "Projects", project_folder, "your_project.brwsd")
	base_blank = os.path.join(working_directory, "ProgramData", "BaseBlankFile.brwsd")

	# Put the txt right next to the brwsd (you can rename if you want)
	manifest_txt = os.path.splitext(output_brwsd)[0] + "_AudioMap.txt"

	if not os.path.exists(unmod_folder) or not os.path.exists(base_blank):
		return

	# Build + write the manifest BEFORE combining, so it matches the exact planned order
	build_list = _list_rwavs_in_build_order(unmod_folder, mod_folder)
	_write_audio_manifest_txt(manifest_txt, build_list)

	if progress_ui:
		progress_ui.generated_text.setText("Combining RWAVs into BRWSD...")
		progress_ui.progressBar.setMaximum(0)
		QApplication.processEvents()

	combine_rwav_files_to_brwsd(unmod_folder, mod_folder, output_brwsd)

	if progress_ui:
		progress_ui.generated_text.setText("Finalizing BRWSD file...")
		QApplication.processEvents()

	append_and_replace_base_blank(base_blank, output_brwsd)

	if progress_ui:
		progress_ui.progressBar.setMaximum(100)
		progress_ui.progressBar.setValue(100)
