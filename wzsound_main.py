import yaml
import os
import sys
import shutil

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from GUI.ui_form import Ui_WZSPI_MainWindow
from rwar_extract import extract_rwar_files
from rwav_extract import setup_extraction
from GUI.wzspi_mainwindow import WZSPI_MainWindow, MissingBrsarDialog  # Assuming this is your main window class

# Import version information
try:
    from version import VERSION, COMMIT_ID
except ImportError:
    VERSION, COMMIT_ID = "v0.0.0", "badcafe"

# EXE location
working_directory = os.path.dirname(sys.executable)

# File/Folder Paths
INSTRUCTIONS_FOLDER = os.path.join(working_directory, "Instructions")

# Folders that need to be extracted
bundled_folders = ["Instructions", "ProgramData"]

def extract_folders():
	for folder in bundled_folders:
		source_folder = os.path.join(sys._MEIPASS, folder) if getattr(sys, 'frozen', False) else folder
		dest_folder = os.path.join(working_directory, folder)

		# Ensure destination folder exists
		if not os.path.exists(dest_folder):
			os.makedirs(dest_folder)

		# Copy individual files if they don't already exist
		for item in os.listdir(source_folder):
			source_path = os.path.join(source_folder, item)
			dest_path = os.path.join(dest_folder, item)

			if not os.path.exists(dest_path):
				if os.path.isdir(source_path):
					shutil.copytree(source_path, dest_path)
					print(f"Copied folder: {item} -> {folder}")
				else:
					shutil.copy2(source_path, dest_path)
					print(f"Copied file: {item} -> {folder}")

def check_wzsound_file(error_window):
    program_data_dir = os.path.join(working_directory, 'ProgramData')
    wzsound_path = os.path.join(program_data_dir, 'WZSound.brsar')

    if not os.path.exists(wzsound_path):
        print("WZSound.brsar not found. Prompting user to locate it...")
        dialog = MissingBrsarDialog(program_data_dir, error_window)
        result = dialog.exec()
        if result != QDialog.Accepted:
            QMessageBox.critical(error_window, "Missing File", "WZSound.brsar is required to continue.")
            sys.exit(0)
        else:
            extract_rwar_files(wzsound_path, working_directory)

def main():
    # Extract folders if needed
    extract_folders()

    # Start Qt app
    app = QApplication(sys.argv)

    window = WZSPI_MainWindow(working_directory)
    window.setWindowTitle(f"WZSound Main - {VERSION} - {COMMIT_ID}")
    if VERSION == "":
        window.setWindowTitle(f"WZSound Main - LOCAL - {COMMIT_ID}")
    window.show()
    check_wzsound_file(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

