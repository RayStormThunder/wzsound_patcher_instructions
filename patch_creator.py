import os
import shutil

from PySide6.QtWidgets import QApplication

def create_patch_file(working_directory, project_name, too_big_list, exact_match_list, progress_ui=None):
    def clean_filename(name):
        """Remove everything from the first space onward."""
        return name.split(" ")[0]

    # Paths
    unmod_folder = os.path.join(working_directory, "Projects", project_name, "UnmodifiedRwavs")
    mod_folder = os.path.join(working_directory, "Projects", project_name, "ModifiedRwavs")
    wzsound_path = os.path.join(working_directory, "ProgramData", "WZSound.brsar")
    output_folder = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions")
    output_file = os.path.join(output_folder, "wzsound_instructions.patch")

    # Ensure WZSound.brsar exists
    if not os.path.exists(wzsound_path):
        print(f"Missing file: {wzsound_path}")
        return

    # Read WZSound.brsar into memory
    with open(wzsound_path, "rb") as wz_file:
        wz_data = wz_file.read()

    # Prepare skip list
    skip_files = {clean_filename(name) for name in too_big_list}

    # Count total files to search
    unfiltered = sorted([
        f for f in os.listdir(unmod_folder)
        if os.path.isfile(os.path.join(unmod_folder, f))
    ])
    files_to_search = [f for f in unfiltered if f not in skip_files]
    files_total = len(files_to_search)
    files_done = 0

    # Collect matches
    instructions = []

    for filename in files_to_search:
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
            progress_ui.label.setText(f"Processing {filename}")
            progress_ui.progressBar.setValue(int((files_done / files_total) * 100))
            QApplication.processEvents()
        files_remaining = files_total - files_done
        print(f"Searching for: {filename} | Done: {files_done} / {files_total} | Remaining: {files_remaining}")

    # Sort results
    instructions.sort(key=lambda x: int(x[0], 16))

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Write instructions
    with open(output_file, "w") as out_file:
        for hex_index, filename in instructions:
            out_file.write(f"{hex_index}:{filename}\n")

    print(f"WZSound patch instructions saved to: {output_file}")

    # Copy all ModifiedRwavs to output folder
    for filename in sorted(os.listdir(mod_folder)):
        src_path = os.path.join(mod_folder, filename)
        dst_path = os.path.join(output_folder, filename)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
    print(f"Copied all ModifiedRwavs to: {output_folder}")