import yaml
import os
import sys
import shutil

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from GUI.ui_form import Ui_WZSPI_MainWindow
from rwar_extract import extract_rwar_files
from rwav_extract import setup_extraction
from play_audio import play_pcm_audio

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
        source = os.path.join(sys._MEIPASS, folder) if getattr(sys, 'frozen', False) else folder
        destination = os.path.join(working_directory, folder)

        if not os.path.exists(destination):
            shutil.copytree(source, destination)
            print(f"Extracted folder: {folder}")
        else:
            print(f"Skipped existing folder: {folder}")

def check_wzsound_file(error_window):
    program_data_dir = os.path.join(working_directory, 'ProgramData')
    wzsound_path = os.path.join(program_data_dir, 'WZSound.brsar')

    if os.path.exists(wzsound_path):
        print(f"WZSound.brsar found at: {wzsound_path}")
    else:
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
    window.show()
    check_wzsound_file(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

