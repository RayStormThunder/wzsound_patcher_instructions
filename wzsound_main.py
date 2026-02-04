import yaml
import os
import sys
import shutil

from PySide6.QtGui import QIcon
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

def check_or_create_version_txt() -> tuple[bool, str]:
	"""
	Returns (force_copy, old_version_for_backup).
	force_copy = version.txt missing OR version mismatch.
	old_version_for_backup = version from txt, or '1.0.0' if missing.
	Also writes ProgramData/version.txt with current VERSION when force_copy is True.
	"""
	program_data_dir = os.path.join(working_directory, "ProgramData")
	os.makedirs(program_data_dir, exist_ok=True)

	version_txt_path = os.path.join(program_data_dir, "version.txt")

	old_version = None
	if os.path.exists(version_txt_path):
		try:
			with open(version_txt_path, "r", encoding="utf-8") as f:
				old_version = f.read().strip()
		except Exception:
			old_version = None

	# If txt didn't exist (or unreadable), assume it WAS 1.0.0
	old_version_for_backup = old_version if old_version else "1.0.0"

	force_copy = (old_version != VERSION)

	# If missing OR mismatch, write current version
	if force_copy:
		try:
			with open(version_txt_path, "w", encoding="utf-8") as f:
				f.write(VERSION)
				print(f"DETECTED UPDATE. EXTRACTING ANY UPDATED INSTRUCTIONS. ALSO BACKING UP PREVIOUS ONES")
		except Exception as e:
			print(f"[WARN] Failed to write version.txt: {e}")

	return force_copy, old_version_for_backup

def backup_instructions(old_version_for_backup: str) -> None:
	"""
	COPIES existing Instructions/* (except Instructions/Backup) into:
	Instructions/Backup/<old_version_for_backup>/
	Leaves the originals in place.
	"""
	instructions_dir = os.path.join(working_directory, "Instructions")
	if not os.path.isdir(instructions_dir):
		return

	backup_root = os.path.join(instructions_dir, "Backup")
	version_backup_dir = os.path.join(backup_root, old_version_for_backup)
	os.makedirs(version_backup_dir, exist_ok=True)

	for name in os.listdir(instructions_dir):
		if name == "Backup":
			continue

		src = os.path.join(instructions_dir, name)
		dst = os.path.join(version_backup_dir, name)

		# If destination already exists, replace it
		if os.path.exists(dst):
			if os.path.isdir(dst):
				shutil.rmtree(dst)
			else:
				os.remove(dst)

		try:
			if os.path.isdir(src):
				shutil.copytree(src, dst, dirs_exist_ok=True)
			else:
				shutil.copy2(src, dst)

			print(f"Backed up: {name} -> Instructions/Backup/{old_version_for_backup}/")
		except Exception as e:
			print(f"[WARN] Failed to backup {name}: {e}")

def extract_folders(force_copy: bool = False):
	for folder in bundled_folders:
		source_folder = os.path.join(sys._MEIPASS, folder) if getattr(sys, "frozen", False) else folder
		dest_folder = os.path.join(working_directory, folder)

		# Ensure destination folder exists
		if not os.path.exists(dest_folder):
			os.makedirs(dest_folder)

		# Copy files/folders
		for item in os.listdir(source_folder):
			source_path = os.path.join(source_folder, item)
			dest_path = os.path.join(dest_folder, item)

			# If we're forcing, overwrite existing content
			if force_copy and os.path.exists(dest_path):
				if os.path.isdir(dest_path):
					shutil.rmtree(dest_path)

			# Normal mode: only copy if missing
			if (not force_copy) and os.path.exists(dest_path):
				continue

			if os.path.isdir(source_path):
				# dirs_exist_ok=True allows overwrite if destination exists (Python 3.8+)
				shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
				print(f"Copied folder: {item} -> {folder}")
			else:
				# copy2 overwrites files by default
				shutil.copy2(source_path, dest_path)
				print(f"Copied file: {item} -> {folder}")


def check_wzsound_file(error_window):
	program_data_dir = os.path.join(working_directory, "ProgramData")
	wzsound_path = os.path.join(program_data_dir, "WZSound.brsar")

	if not os.path.exists(wzsound_path):
		print("WZSound.brsar not found. Prompting user to locate it...")
		dialog = MissingBrsarDialog(program_data_dir, error_window)
		result = dialog.exec()
		if result != QDialog.Accepted:
			QMessageBox.critical(error_window, "Missing File", "WZSound.brsar is required to continue.")
			sys.exit(0)
		else:
			extract_rwar_files(wzsound_path, working_directory)

def get_icon_path() -> str | None:
	candidates: list[str] = []

	if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
		candidates.append(os.path.join(sys._MEIPASS, "WZ.ico"))

	candidates.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "WZ.ico"))
	candidates.append(os.path.join(working_directory, "WZ.ico"))

	for p in candidates:
		if p and os.path.isfile(p):
			return p
	return None

def main():
	# Check version BEFORE extracting bundled folders
	force_copy, old_version_for_backup = check_or_create_version_txt()

	# If we are overriding, back up existing Instructions first
	if force_copy:
		backup_instructions(old_version_for_backup)

	# Extract folders (force overwrite on version change)
	extract_folders(force_copy=force_copy)

	# Start Qt app
	app = QApplication(sys.argv)

	# Set icon (app-wide + window)
	icon_path = get_icon_path()
	if icon_path:
		icon = QIcon(icon_path)
		app.setWindowIcon(icon)

	window = WZSPI_MainWindow(working_directory)

	if icon_path:
		window.setWindowIcon(QIcon(icon_path))

	window = WZSPI_MainWindow(working_directory)
	window.setWindowTitle(f"WZSound Main - {VERSION} - {COMMIT_ID}")
	if VERSION == "":
		window.setWindowTitle(f"WZSound Main - LOCAL - {COMMIT_ID}")
	window.show()

	check_wzsound_file(window)
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
