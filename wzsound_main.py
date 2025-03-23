import yaml
import os
import sys
import shutil

from PySide6.QtWidgets import QApplication
from GUI.ui_form import Ui_WZSPI_MainWindow

from GUI.wzspi_mainwindow import WZSPI_MainWindow  # Assuming this is your main window class

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
bundled_folders = ["Instructions"]

def get_yaml_version(game_name):
	yaml_path = os.path.join(INSTRUCTIONS_FOLDER, "program_data.yaml")
	try:
		with open(yaml_path, "r", encoding="utf-8") as file:
			versions = yaml.safe_load(file).get("Versions", {})
			return versions.get(game_name, "Unknown Version")
	except FileNotFoundError:
		return "Version File Not Found"
	except yaml.YAMLError:
		return "Invalid YAML Format"

def change_yaml_version(game_name, new_version):
	yaml_path = os.path.join(INSTRUCTIONS_FOLDER, "program_data.yaml")
	try:
		if os.path.exists(yaml_path):
			with open(yaml_path, "r", encoding="utf-8") as file:
				data = yaml.safe_load(file) or {}
		else:
			data = {}

		if "Versions" not in data or not isinstance(data["Versions"], dict):
			data["Versions"] = {}

		data["Versions"][game_name] = new_version

		with open(yaml_path, "w", encoding="utf-8") as file:
			yaml.safe_dump(data, file, allow_unicode=True)

		return True
	except yaml.YAMLError:
		return False

def extract_folders():
	for folder in bundled_folders:
		source = os.path.join(sys._MEIPASS, folder) if getattr(sys, 'frozen', False) else folder
		destination = os.path.join(working_directory, folder)
		shutil.copytree(source, destination, dirs_exist_ok=True)

def main():
	version_last = get_yaml_version("WZSound Main")
	version_current = (f"{VERSION} {COMMIT_ID}")

	if version_last != version_current:
		extract_folders()

	change_yaml_version("WZSound Main", version_current)
	print(f"WZSound Main - {VERSION} - {COMMIT_ID}")

	# Initialize and launch the UI
	app = QApplication(sys.argv)
	window = WZSPI_MainWindow()
	window.setWindowTitle(f"WZSound Main - {VERSION} - {COMMIT_ID}")
	window.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
