# This Python file uses the following encoding: utf-8
import sys
import os
import re
import struct
import hashlib
import yaml
import shutil
import subprocess

<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QMainWindow, QMessageBox, QInputDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QTimer, QStringListModel, Signal

# Try importing ui_form from current directory or GUI folder
try:
        from ui_form import Ui_WZSPI_MainWindow
except ImportError:
        try:
                from GUI.ui_form import Ui_WZSPI_MainWindow
        except ImportError as e:
                raise ImportError("Could not import Ui_WZSPI_MainWindow from ui_form or GUI.ui_form") from e

# Try importing ui_missing_brsar_dialog from current directory or GUI folder
try:
        from ui_missing_brsar_dialog import Ui_Dialog
except ImportError:
        try:
                from GUI.ui_missing_brsar_dialog import Ui_Dialog
        except ImportError as e:
                raise ImportError("Could not import Ui_Dialog from ui_missing_brsar_dialog or GUI.ui_missing_brsar_dialog") from e

# Try importing ui_report from current directory or GUI folder
try:
        from ui_report import Ui_Dialog_Report
except ImportError:
        try:
                from GUI.ui_report import Ui_Dialog_Report
        except ImportError as e:
                raise ImportError("Could not import Ui_Dialog_Report from ui_report or GUI.ui_report") from e

# Try importing ui_success from current directory or GUI folder
try:
        from ui_success import Ui_Dialog_Success
except ImportError:
        try:
                from GUI.ui_success import Ui_Dialog_Success
        except ImportError as e:
                raise ImportError("Could not import Ui_Dialog_Success from ui_success or GUI.ui_success") from e

# Try importing ui_progress from current directory or GUI folder
try:
        from ui_progress import Ui_Dialog_Progress
except ImportError:
        try:
                from GUI.ui_progress import Ui_Dialog_Progress
        except ImportError as e:
                raise ImportError("Could not import Ui_Dialog_Progress from ui_progress or GUI.ui_progress") from e

# Try importing ui_convert from current directory or GUI folder
try:
        from ui_convert import Ui_Dialog_Convert
except ImportError:
        try:
                from GUI.ui_convert import Ui_Dialog_Convert
        except ImportError as e:
                raise ImportError("Could not import Ui_Dialog_Convert from ui_convert or GUI.ui_convert") from e

try:
<<<<<<< HEAD
        from rwav_extract import setup_extraction, setup_extraction_converted, setup_extraction_HD
=======

        from rwav_extract import setup_extraction, setup_extraction_converted, setup_extraction_HD

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
        print("imported rwav_extract")
except ImportError as e:
        print("failed to import rwav_extract")
        pass

try:
<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
        from rwar_extract import extract_rwar_files
        print("imported rwar_extract")
except ImportError as e:
        print("failed to import rwar_extract")
        pass

try:
<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
        from brwsd_creator import build_brwsd_from_unmodified_rwavs
        print("imported brwsd_creator")
except ImportError as e:
        print("failed to import brwsd_creator")
        pass

try:
        from extract_brwsd import extract_rwavs, check_modified_vs_unmodified
        print("imported extract_brwsd")
except ImportError as e:
        print("failed to import extract_brwsd")
        pass

try:
        from patch_creator import create_patch_file
        print("imported patch_creator")
except ImportError as e:
        print("failed to import patch_creator")
        pass

try:
        from patch_wzsound import apply_wzsound_patch
        print("imported patch_wzsound")
except ImportError as e:
        print("failed to import patch_wzsound")
        pass

<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
def extract_differences_and_create_instruction(
    modified_folder, original_folder, output_directory, instruction_filename
):
        def read_rwav_values(file_path):
                with open(file_path, "rb") as f:
                        data = f.read()

                index = 0
                values = []

                while index < len(data):
                        index = data.find(b"RWAV", index)
                        if index == -1 or index + 12 > len(data):
                                break

                        # Read the 4 bytes at offset 0x8 from RWAV
                        value = data[index + 8:index + 12]
                        values.append(value)

                        # Skip this RWAV chunk (move forward by 12 at least)
                        index += 12

                return values

        def compare_rwav_values(modified_path, original_path):
                modified_values = read_rwav_values(modified_path)
                original_values = read_rwav_values(original_path)

                diffs = []
                for i, (m, o) in enumerate(zip(modified_values, original_values)):
                        if m != o:
                                diffs.append(i)

                return diffs

        instruction_data = {}

        for file_name in os.listdir(modified_folder):
                if not file_name.endswith(".brwsd"):
                        continue

                original_path = os.path.join(original_folder, file_name)
                modified_path = os.path.join(modified_folder, file_name)

                if not os.path.exists(original_path):
                        continue

                with open(original_path, "rb") as f1, open(modified_path, "rb") as f2:
                        if f1.read() == f2.read():
                                continue

                diff_indices = compare_rwav_values(modified_path, original_path)
                if not diff_indices:
                        continue

                # Format RWAV index ranges
                grouped = []
                start = prev = diff_indices[0]

                for idx in diff_indices[1:]:
                        if idx == prev + 1:
                                prev = idx
                        else:
                                if start == prev:
                                        grouped.append(start)
                                else:
                                        grouped.append(f"{start} - {prev}")
                                start = prev = idx

                if start == prev:
                        grouped.append(start)
                else:
                        grouped.append(f"{start} - {prev}")

                # Extract Index number like Index_025 from Index_025_621.brwsd
                base_name = os.path.splitext(file_name)[0]
                parts = base_name.split("_")
                if len(parts) >= 2:
                        key = f"{parts[0]}_{parts[1]}"
                        if key not in instruction_data:
                                instruction_data[key] = []
                        instruction_data[key].extend(grouped)

        # Write YAML output with clean formatting (no quotes on integers)
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, instruction_filename)

        with open(output_path, "w") as f:
                yaml.dump(
                        instruction_data,
                        f,
                        sort_keys=True,
                        default_flow_style=False,
                        allow_unicode=True,
                )

        return output_path

def format_name(name: str) -> str:
        parts = name.replace(" ", "_").split("_")
        formatted_parts = [part.capitalize() for part in parts if part]
        return "_".join(formatted_parts)


<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
class ConvertDialog(QDialog):
        def __init__(self, working_directory, project_name, parent=None):
                super().__init__(parent)
                self.ui = Ui_Dialog_Convert()
                self.ui.setupUi(self)

                self.working_directory = working_directory
                self.project_name = project_name
                print(f"ConvertDialog received project name: {self.project_name}")

                # Enable pushButton_4 only if project_name is valid and ModifiedRwavs folder exists
                if self.project_name:
                        modified_rwavs_path = os.path.join(
                                self.working_directory, "Projects", self.project_name, "ModifiedRwavs"
                        )
                        self.ui.pushButton_4.setEnabled(os.path.isdir(modified_rwavs_path))
                else:
                        self.ui.pushButton_3.setEnabled(False)
                        self.ui.pushButton_4.setEnabled(False)


                # Connect pushButton_3 to run_patch
                self.ui.pushButton_3.clicked.connect(self.run_patch)

                # Connect pushButton_4 to the custom logic
                self.ui.pushButton_4.clicked.connect(self.handle_pushbutton_4_click)

                self.ui.ConvertModified.clicked.connect(self.open_modified_input_dialog)

        def convert_modified(self, project_name, instruction_file):
                project_name = format_name(project_name)
                project_dir = os.path.join(self.working_directory, "Projects", project_name)
                instruction_file = format_name(instruction_file)

                # Step 1: Create the folder if it doesn't exist
                try:
                        os.makedirs(project_dir, exist_ok=True)
                        print(f"[INFO] Created or found existing folder: {project_dir}")
                except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to create project folder:\n{e}")
                        return

                # Step 2: Ask user to provide the modified WZSound.brsar
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Modified WZSound.brsar", "", "BRSAR Files (*.brsar)")
                if not file_path:
                        QMessageBox.information(self, "Cancelled", "No file selected.")
                        return

                # Step 3: Copy the selected file into the project folder
                try:
                        modified_dir = os.path.join(project_dir, "ModifiedWZSound")
                        os.makedirs(modified_dir, exist_ok=True)

                        # Copy to ModifiedWZSound/WZSound.brsar
                        dest_path = os.path.join(modified_dir, "WZSound.brsar")
                        shutil.copy(file_path, dest_path)
                        print(f"[INFO] Copied modified WZSound to: {dest_path}")

                        target_folder = os.path.join("Projects", project_name, "Indexes")
                        extract_rwar_files(dest_path, self.working_directory, target_folder=target_folder)
                except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to copy file:\n{e}")
                        return

                # Step 4: You can store the instruction file name, or continue processing here
                print(f"[SUCCESS] Project setup complete for '{project_name}' with instruction file '{instruction_file}'")

                # Step 5: Compare Indexes and generate instruction YAML
                modified_indexes = os.path.join(project_dir, "Indexes")
                original_indexes = os.path.join(self.working_directory, "Indexes")
                instruction_output_dir = os.path.join(self.working_directory, "Instructions")

                instruction_path = extract_differences_and_create_instruction(
                        modified_folder=modified_indexes,
                        original_folder=original_indexes,
                        output_directory=instruction_output_dir,
                        instruction_filename=f"{instruction_file}.yaml"
                )

                print(f"[SUCCESS] Instruction file created at: {instruction_path}")

                # Step 6: Write 'instructions.yaml' in the project folder
                instruction_list_path = os.path.join(project_dir, "instructions.yaml")
                instruction_name_without_ext = instruction_file  # because we never added .yaml to this variable

                try:
                        with open(instruction_list_path, "w") as f:
                                yaml.dump([instruction_name_without_ext], f, default_flow_style=False)
                        print(f"[INFO] Wrote instructions.yaml to: {instruction_list_path}")
                except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to write instructions.yaml:\n{e}")
                        return

                # Step 7: Generate converted BRWSD using final project name
                self.create_brwsd_converted(project_name)

        def create_brwsd_converted(self, project_name):
                extract_rwavs(self.working_directory, project_name)
                setup_extraction(self.working_directory, project_name)
                setup_extraction_converted(self.working_directory, project_name)
                build_brwsd_from_unmodified_rwavs(self.working_directory, project_name)
                print("Create BRWSD clicked")

                # Show the report dialog
                dialog = SuccessDialog(self.working_directory, project_name, self)
                dialog.exec()

        def open_modified_input_dialog(self):
                dialog = QDialog(self)
                dialog.setWindowTitle("Convert Modified")

                layout = QVBoxLayout(dialog)

                project_input = QLineEdit()
                project_input.setPlaceholderText("Enter project name")
                instruction_input = QLineEdit()
                instruction_input.setPlaceholderText("Enter instruction file name")

                submit_button = QPushButton("Submit")

                layout.addWidget(QLabel("Project Name:"))
                layout.addWidget(project_input)
                layout.addWidget(QLabel("Instruction File:"))
                layout.addWidget(instruction_input)
                layout.addWidget(QLabel("Submit an SD WZSound file that IS MODIFIED with sound effects already replaced in it"))
                layout.addWidget(submit_button)

                def on_submit():
                        project_name = project_input.text().strip()
                        instruction_file = instruction_input.text().strip()

                        if not project_name or not instruction_file:
                                QMessageBox.warning(dialog, "Missing Input", "Both fields must be filled.")
                                return

                        dialog.accept()

                        # Call your logic here using project_name and instruction_file
                        print(f"Submitted project: {project_name}, instruction file: {instruction_file}")
                        self.convert_modified(project_name, instruction_file)

                submit_button.clicked.connect(on_submit)

                dialog.exec()


        def handle_pushbutton_4_click(self):
                indexes_hd_path = os.path.join(self.working_directory, "IndexesHD")
                if not os.path.exists(indexes_hd_path):
                        dialog = MissingBrsarHDDialog(self.working_directory, self)
                        if dialog.exec() != QDialog.Accepted:
                                print("User cancelled HD WZSound selection.")
                                return  # Skip rest if user cancels
                        else:
                                print("HD WZSound provided.")

                # Proceed with the actual HD patch logic
                self.run_hd_patch()

        def run_hd_patch(self):
                # Replace with your actual logic
                print("Running HD patch logic...")
                project_name = self.project_name
                setup_extraction_HD(self.working_directory, project_name)
                self.patch_hd_wzsound(self.working_directory, self.project_name)


        def patch_hd_wzsound(self, working_directory, project_name):
                def find_all_occurrences(data: bytes, pattern: bytes) -> list:
                        indices = []
                        start = 0
                        while True:
                                index = data.find(pattern, start)
                                if index == -1:
                                        break
                                indices.append(index)
                                start = index + 1
                        return indices

                project_folder = os.path.join(working_directory, "Projects", project_name)

                # Step 1: Create "WZSoundHD" folder inside the project folder
                hd_output_folder = os.path.join(project_folder, "WZSoundHD")
                os.makedirs(hd_output_folder, exist_ok=True)

                # Step 2: Copy original HD WZSound.brsar into that folder
                source_brsar = os.path.join(working_directory, "ProgramData", "WZSoundHD.brsar")
                patched_brsar = os.path.join(hd_output_folder, "WZSound.brsar")
                shutil.copy(source_brsar, patched_brsar)
                print(f"[INFO] Copied WZSoundHD.brsar to {patched_brsar}")

                # Step 3: Patch RWAVs
                unmodified_folder = os.path.join(project_folder, "UnmodifiedRwavsHD")
                modified_folder = os.path.join(project_folder, "ModifiedRwavs")

                # Load file into memory
                with open(patched_brsar, "rb") as f:
                        data = bytearray(f.read())

                # Prepare list of RWAVs to patch
                rwav_files = [f for f in os.listdir(unmodified_folder) if f.endswith(".rwav")]
                total = len(rwav_files)
                processed = 0

                # Show progress dialog
                progress_dialog = ProgressDialog(self)
                progress_dialog.setWindowTitle("Patching RWAV Files...")
                progress_dialog.ui.progressBar.setMaximum(total)
                progress_dialog.show()
                QApplication.processEvents()

                for filename in rwav_files:
                        processed += 1

                        if hasattr(progress_dialog.ui, "label_status"):
                                progress_dialog.ui.label_status.setText(f"Patching {processed} of {total}: {filename}")
                        if hasattr(progress_dialog.ui, "progressBar"):
                                progress_dialog.ui.progressBar.setValue(processed)
                        QApplication.processEvents()

                        unmod_path = os.path.join(unmodified_folder, filename)
                        mod_path = os.path.join(modified_folder, filename)

                        if not os.path.exists(mod_path):
                                continue  # No modified version exists

                        with open(unmod_path, "rb") as f_unmod:
                                unmod_data = f_unmod.read()
                        with open(mod_path, "rb") as f_mod:
                                mod_data = f_mod.read()

                        if len(mod_data) > len(unmod_data):
                                print(f"[SKIPPED] Modified RWAV '{filename}' is larger than original. Cannot safely replace.")
                                continue

                        occurrences = find_all_occurrences(data, unmod_data)

                        if not occurrences:
                                print(f"[WARNING] Could not find unmodified RWAV: {filename}")
                                continue

                        for index in occurrences:
                                data[index:index + len(mod_data)] = mod_data
                                remaining = len(unmod_data) - len(mod_data)
                                data[index + len(mod_data):index + len(unmod_data)] = b'\x00' * remaining
                                print(f"[PATCHED] Replaced RWAV: {filename} at offset {index}")

                progress_dialog.close()

                # Save patched file
                with open(patched_brsar, "wb") as f:
                        f.write(data)

                print("[SUCCESS] WZSound.brsar HD patching complete.")

<<<<<<< HEAD


=======
>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
        def run_patch(self):
            apply_wzsound_patch(self.working_directory, self.project_name)
            self.close()
            self.show_confirmation()

        def show_confirmation(self):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("WZSound Patch Applied")
            msg_box.setText("Successfully applied WZSound patch.")

            open_button = msg_box.addButton("Open WZSound Location", QMessageBox.AcceptRole)
            close_button = msg_box.addButton("Close", QMessageBox.RejectRole)

            msg_box.exec()

            if msg_box.clickedButton() == open_button:
                wzsound_folder = os.path.join(self.working_directory, "Projects", self.project_name, "WZSound")
                if os.path.exists(wzsound_folder):
                    subprocess.Popen(f'explorer "{wzsound_folder}"')  # Windows only
                else:
                    QMessageBox.warning(self, "Folder Not Found", f"Folder does not exist:\n{wzsound_folder}")



class ProgressDialog(QDialog):
        cancelled = Signal()  # Custom signal emitted if the window is closed by user

        def __init__(self, parent=None):
            super().__init__(parent)
            self.ui = Ui_Dialog_Progress()
            self.ui.setupUi(self)

        def closeEvent(self, event):
            # Emit the custom signal on close
            self.cancelled.emit()
            event.accept()

class MissingBrsarDialog(QDialog):
        def __init__(self, program_data_dir, parent=None):
                super().__init__(parent)
                self.ui = Ui_Dialog()
                self.ui.setupUi(self)

                self.program_data_dir = program_data_dir
                self.wzsound_path = os.path.join(self.program_data_dir, 'WZSound.brsar')

                self.ui.button_error.clicked.connect(self.browse_file)

        def browse_file(self):
                file_path, _ = QFileDialog.getOpenFileName(self, "Select WZSound.brsar", "", "BRSAR Files (*.brsar)")
                if file_path:
                        try:
                                if not os.path.exists(self.program_data_dir):
                                        os.makedirs(self.program_data_dir)
                                shutil.copy(file_path, self.wzsound_path)
                                print(f"Copied WZSound.brsar to: {self.wzsound_path}")
                                self.accept()
                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to copy file:\n{e}")

class MissingBrsarHDDialog(QDialog):
        def __init__(self, program_data_dir, parent=None):
                super().__init__(parent)
                self.ui = Ui_Dialog()
                self.ui.setupUi(self)

                self.program_data_dir = os.path.join(program_data_dir, 'ProgramData')
                self.hd_wzsound_path = os.path.join(self.program_data_dir, 'WZSoundHD.brsar')

                self.ui.button_error.setText("Browse HD File")
                self.ui.label_error.setText("Please select the HD version of WZSound.brsar")

                self.ui.button_error.clicked.connect(self.browse_file)

        def browse_file(self):
                file_path, _ = QFileDialog.getOpenFileName(self, "Select HD WZSound.brsar", "", "BRSAR Files (*.brsar)")
                if file_path:
                        try:
                                if not os.path.exists(self.program_data_dir):
                                        os.makedirs(self.program_data_dir)

                                shutil.copy(file_path, self.hd_wzsound_path)
                                print(f"Copied HD WZSound.brsar to: {self.hd_wzsound_path}")

                                # Now call the extractor
                                working_directory = os.path.dirname(sys.executable)
                                extract_rwar_files(self.hd_wzsound_path, working_directory, target_folder="IndexesHD")

                                self.accept()
                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to copy or extract file:\n{e}")



class ReportDialog(QDialog):
        def __init__(self, file_path, project_name, too_big_list, exact_match_list, parent=None):
                super().__init__(parent)
                self.ui = Ui_Dialog_Report()
                self.ui.setupUi(self)

                self.too_big_list = too_big_list
                self.project_name = project_name
                self.working_directory = file_path  # Alias for clarity

                # Set lists
                model1 = QStringListModel()
                model1.setStringList(exact_match_list)
                self.ui.listView.setModel(model1)

                model2 = QStringListModel()
                model2.setStringList(too_big_list)
                self.ui.listView_2.setModel(model2)

                # Disable reset button if there are no "too big" files
                if not too_big_list:
                        self.ui.button_reset.setEnabled(False)

                # Connect buttons
                self.ui.button_close.clicked.connect(self.close)
                self.ui.button_explorer.clicked.connect(self.open_folder)
                self.ui.button_reset.clicked.connect(self.reset_modified_files)

                # Set release and project paths
                self.release_path = os.path.join(file_path, "Releases", project_name)
                self.projects_path = os.path.join(file_path, "Projects", project_name)

        def open_folder(self):
                if os.path.exists(self.release_path):
                        subprocess.Popen(f'explorer "{self.release_path}"')  # Windows
                else:
                        QMessageBox.warning(self, "Folder Not Found", f"The path does not exist:\n{self.release_path}")

        def reset_modified_files(self):
                mod_folder = os.path.join(self.projects_path, "ModifiedRwavs")

                files_deleted = []

                for entry in self.too_big_list:
                        # Extract base filename before first space
                        base_name = entry.split(" ")[0]

                        mod_file_path = os.path.join(mod_folder, base_name)

                        if os.path.exists(mod_file_path):
                                try:
                                        os.remove(mod_file_path)
                                        files_deleted.append(base_name)
                                except Exception as e:
                                        QMessageBox.warning(self, "Error", f"Failed to delete {base_name}:\n{e}")

                # Update label_6 and disable reset button
                if files_deleted:
                        self.ui.label_6.setText("These files have been reset")

                        # Rebuild BRWSD after reset
                        setup_extraction(self.working_directory, self.project_name)
                        build_brwsd_from_unmodified_rwavs(self.working_directory, self.project_name)

                        QMessageBox.information(self, "Reset Complete", f"Deleted {len(files_deleted)} file(s) from ModifiedRwavs and rebuilt BRWSD.")
                else:
                        QMessageBox.information(self, "No Files Reset", "No matching files were found to delete.")

                # Disable reset button after use
                self.ui.button_reset.setEnabled(False)

class SuccessDialog(QDialog):
        def __init__(self, file_path, project_name, parent=None):
                super().__init__(parent)
                self.ui = Ui_Dialog_Success()
                self.ui.setupUi(self)

                # Connect buttons
                self.ui.pushButton.clicked.connect(self.close)
                self.ui.pushButton_2.clicked.connect(self.open_folder)

                self.success_path = os.path.join(file_path, "Projects", project_name)


        def open_folder(self):
                if os.path.exists(self.success_path):
                        subprocess.Popen(f'explorer "{self.success_path}"')  # Windows
                else:
                        QMessageBox.warning(self, "Folder Not Found", f"The path does not exist:\n{self.release_path}")


class YamlHighlighter(QSyntaxHighlighter):
        def __init__(self, parent):
                super().__init__(parent)

                # Key format (e.g., RWSD_4)
                self.key_format = QTextCharFormat()
                self.key_format.setForeground(QColor(100, 200, 255))

                # Symbol format (e.g., ":" and "-")
                self.symbol_format = QTextCharFormat()
                self.symbol_format.setForeground(QColor("white"))

                # Value format (e.g., numbers, ranges, or the word "All")
                self.value_format = QTextCharFormat()
                self.value_format.setForeground(QColor("orange"))

                # Comment format (e.g., # Comment)
                self.comment_format = QTextCharFormat()
                self.comment_format.setForeground(QColor(144, 238, 144))  # Light green

        def highlightBlock(self, text):
                # Highlight comments
                comment_match = re.search(r'#.*', text)
                if comment_match:
                        self.setFormat(comment_match.start(), len(text) - comment_match.start(), self.comment_format)
                        return

                # Highlight keys at the beginning of the line (before colon)
                for match in re.finditer(r'^\s*[\w\-]+(?=\s*:)', text):
                        self.setFormat(match.start(), match.end() - match.start(), self.key_format)

                # Highlight symbols (":" and "-")
                for match in re.finditer(r'[:\-]', text):
                        self.setFormat(match.start(), match.end() - match.start(), self.symbol_format)

                # Highlight numeric values, ranges, and the word "All"
                for match in re.finditer(r'\b(?:\d+(?:\s*-\s*\d+)?|All)\b', text):
                        self.setFormat(match.start(), match.end() - match.start(), self.value_format)

class WZSPI_MainWindow(QMainWindow):
        def __init__(self, working_directory, parent=None):
                super().__init__(parent)
<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
                self.working_directory = working_directory  # Store for later use
                self.ui = Ui_WZSPI_MainWindow()
                self.ui.setupUi(self)

                # Setup font and appearance
                font = self.ui.text_yaml_edit.font()
                font.setFamily("Segoue monospace")
                self.ui.text_yaml_edit.setFont(font)
                self.ui.text_yaml_edit.setTabChangesFocus(False)

                self.ui.text_yaml_edit.setStyleSheet("""
                        QTextEdit {
                                background-color: #121212;
                                color: white;
                        }
                """)

                # Connect all buttons to functions
                self.ui.button_convert_project.clicked.connect(self.convert_project)
                self.ui.button_load_project.clicked.connect(self.load_project)
                self.ui.button_create_project.clicked.connect(self.create_project)
                self.ui.button_create_instructions.clicked.connect(self.create_instructions)
                self.ui.button_edit_instructions.clicked.connect(self.edit_instructions)
                self.ui.button_move.clicked.connect(self.move)
                self.ui.button_cancel_changes.clicked.connect(self.cancel_changes)
                self.ui.button_save_changes.clicked.connect(self.save_changes)
                self.ui.button_create_brwsd.clicked.connect(self.create_brwsd)
                self.ui.button_create_wzsound.clicked.connect(self.create_wzsound)

<<<<<<< HEAD
=======

>>>>>>> c614fd41d2ea76a9c12c68e252abd5161018ce81
                self.ui.list_options.itemSelectionChanged.connect(lambda: self.ui.list_project.clearSelection())
                self.ui.list_project.itemSelectionChanged.connect(lambda: self.ui.list_options.clearSelection())

                # Set up the project name and disable buttons by default
                self.project_name = None
                self.update_project_buttons_state()

                # Timer to update button state every second
                self.project_state_timer = QTimer(self)
                self.project_state_timer.timeout.connect(self.update_project_buttons_state)
                self.project_state_timer.start(250)  # 1000 ms = 1 second


                self.ui.list_options.setStyleSheet("""
                        QListWidget {
                                background-color: #1e1e1e;
                                alternate-background-color: #2c2c2c;
                                color: white;
                        }
                """)

                self.ui.list_project.setStyleSheet("""
                        QListWidget {
                                background-color: #1e1e1e;
                                alternate-background-color: #2c2c2c;
                                color: white;
                        }
                """)


                # Syntax highlighter
                self.highlighter = YamlHighlighter(self.ui.text_yaml_edit.document())

                if hasattr(self.ui, "validateButton"):
                        self.ui.validateButton.clicked.connect(self.validate_yaml)


        def convert_project(self):
                print("Convert Project clicked")
                self.convert_window = ConvertDialog(self.working_directory, self.project_name, self)
                self.convert_window.exec()  # Use .show() if you want it non-modal


        def load_project(self):
                print("Load Project clicked")

                # Path to the Projects folder
                projects_dir = os.path.join(self.working_directory, "Projects")

                # Ensure the Projects folder exists
                if not os.path.exists(projects_dir):
                        QMessageBox.information(self, "No Projects", "No projects found. Create one first.")
                        return

                # Get list of project folders
                project_folders = [
                        name for name in os.listdir(projects_dir)
                        if os.path.isdir(os.path.join(projects_dir, name))
                ]

                if not project_folders:
                        QMessageBox.information(self, "No Projects", "No project folders found in the Projects directory.")
                        return

                # Map formatted names (with spaces) to real folder names
                project_map = {folder.replace("_", " "): folder for folder in project_folders}
                formatted_names = list(project_map.keys())

                # Ask user to select a project
                selected_name, ok = QInputDialog.getItem(
                        self,
                        "Load Project",
                        "Select a project:",
                        formatted_names,
                        editable=False
                )

                if ok and selected_name:
                        # Set the original folder name
                        self.project_name = project_map[selected_name]
                        self.ui.label_project.setText(self.project_name.replace("_", " ").title())
                        self.setup_project()
                        print(f"Loaded project: {self.project_name}")
                else:
                        print("Project loading canceled.")

        def create_project(self):
                print("Create Project clicked")

                # Prompt the user to enter a project name
                name, ok = QInputDialog.getText(self, "Create Project", "Enter a name for the project:")

                if ok and name.strip():
                        # Format: Capitalize first letter of each word, replace spaces with underscores
                        formatted_name = name.strip().title().replace(" ", "_")
                        project_title = name.strip().title()
                        self.project_name = formatted_name  # Save for later use

                        # Create Projects directory if it doesn't exist
                        projects_dir = os.path.join(self.working_directory, "Projects")
                        project_path = os.path.join(projects_dir, self.project_name)

                        self.ui.label_project.setText(project_title)

                        try:
                                os.makedirs(project_path, exist_ok=True)
                                print(f"Project folder created at: {project_path}")
                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to create project folder:\n{e}")
                        self.setup_project()
                else:
                        print("Project creation canceled or empty input.")

        def create_instructions(self):
                print("Create Instructions clicked")

                # Prompt the user to enter a name
                name, ok = QInputDialog.getText(self, "Create Instructions", "Enter a name for this set of instructions. \nIt should explain what sound effects it is trying to export.")

                if ok and name.strip():
                        self.instruction_name = name.strip()  # Save it for later use if needed
                        print(f"Instruction name set to: {self.instruction_name}")

                        # Set the instructional template text
                        template_text = (
                                "#Start by writing the BRWSD file name followed by a colon\n"
                                "#Indent the Audio line followed by a dash, number, range of numbers, or all\n\n"
                                "#Index_id:\n"
                                "#  - number\n\n"
                                "#This will extract Audio 1 from Index_001.brwsd\n"
                                "Index_001:\n"
                                "  - 1\n\n"
                                "#This will extract Audio 1 and 7 from Index_002.brwsd\n"
                                "Index_002:\n"
                                "  - 1\n"
                                "  - 7\n\n"
                                "#This will extract Audio 1 through 7 from Index_003.brwsd\n"
                                "Index_003:\n"
                                "  - 1 - 7\n\n"
                                "#This will extract Audio 1 AND 3 through 7 from Index_004.brwsd\n"
                                "Index_004:\n"
                                "  - 1\n"
                                "  - 3 - 7\n\n"
                                "#This will extract ALL Audio RWAVs from Index_005.brwsd\n"
                                "Index_005:\n"
                                "  - All\n\n"
                                "#These are just example instructions. You can delete anything you want"
                        )

                        # Set the YAML editor text
                        self.ui.text_yaml_edit.setPlainText(template_text)

                        # Change the page
                        self.ui.stacked_pages.setCurrentIndex(1)
                else:
                        print("Instruction creation canceled or empty input.")

        def edit_instructions(self):
                print("Edit Instructions clicked")

                # Open file dialog starting in {working_directory}/Instructions
                instructions_path = os.path.join(self.working_directory, "Instructions")
                file_path, _ = QFileDialog.getOpenFileName(
                        self,
                        "Open Instruction File",
                        instructions_path,
                        "YAML Files (*.yaml *.yml)"
                )

                if file_path:
                        try:
                                # Read file content
                                with open(file_path, "r", encoding="utf-8") as file:
                                        content = file.read()

                                # Set the editor text
                                self.ui.text_yaml_edit.setPlainText(content)

                                # Extract filename without extension and store it as the instruction name
                                base_name = os.path.basename(file_path)
                                name_without_ext = os.path.splitext(base_name)[0]
                                self.instruction_name = name_without_ext

                                print(f"Loaded instruction: {self.instruction_name}")
                                self.ui.stacked_pages.setCurrentIndex(1)

                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")
                else:
                        print("User canceled file selection.")

        def move(self):
                options_list = self.ui.list_options
                project_list = self.ui.list_project

                # Determine source and target lists based on selection
                if options_list.selectedItems():
                        source = options_list
                        target = project_list
                elif project_list.selectedItems():
                        source = project_list
                        target = options_list
                else:
                        print("No items selected to move.")
                        return

                # Move selected items
                for item in source.selectedItems():
                        target.addItem(item.text())
                        source.takeItem(source.row(item))

                print("Moved selected item(s).")

                # Save the project list to instructions.yaml
                if not hasattr(self, 'project_name') or not self.project_name:
                        print("No project loaded.")
                        return

                # Construct path: {working_directory}/Projects/{ProjectName}/instructions.yaml
                project_path = os.path.join(self.working_directory, "Projects", self.project_name)
                save_path = os.path.join(project_path, "instructions.yaml")

                # Gather items from list_project
                instructions = []
                for i in range(project_list.count()):
                        item_text = project_list.item(i).text()
                        instructions.append(item_text)

                # Write YAML file
                try:
                        with open(save_path, "w", encoding="utf-8") as f:
                                yaml.dump(instructions, f, sort_keys=False, allow_unicode=True)
                        print(f"Updated instruction file at: {save_path}")
                except Exception as e:
                        QMessageBox.critical(self, "Save Error", f"Failed to save instructions.yaml:\n{e}")


        def cancel_changes(self):
                print("Cancel Changes clicked")
                self.ui.stacked_pages.setCurrentIndex(0)
                self.ui.text_yaml_edit.setPlainText("")

        def save_changes(self):
                print("Save Changes clicked")
                self.ui.stacked_pages.setCurrentIndex(0)

                # Make sure we have a name to use
                if not hasattr(self, 'instruction_name') or not self.instruction_name:
                        QMessageBox.warning(self, "No Name", "No instruction name was set.")
                        return

                # Format the name: capitalize first letter of each word and replace spaces with underscores
                filename = self.instruction_name.title().replace(" ", "_") + ".yaml"

                # Get the YAML content
                content = self.ui.text_yaml_edit.toPlainText()

                # Convert tabs to 2 spaces
                content = content.replace("\t", "  ")

                # Construct full path
                save_path = os.path.join(self.working_directory, "Instructions", filename)

                try:
                        # Ensure the Instructions folder exists
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)

                        # Write the file
                        with open(save_path, "w", encoding="utf-8") as file:
                                file.write(content)

                        print(f"Saved to: {save_path}")
                except Exception as e:
                        QMessageBox.critical(self, "Save Failed", f"Could not save file:\n{e}")
                self.ui.text_yaml_edit.setPlainText("")
                self.setup_project()

        def create_brwsd(self):
                extract_rwavs(self.working_directory, self.project_name)
                setup_extraction(self.working_directory, self.project_name)
                build_brwsd_from_unmodified_rwavs(self.working_directory, self.project_name)
                print("Create BRWSD clicked")

                # Show the report dialog using your new class
                dialog = SuccessDialog(self.working_directory, self.project_name, self)
                dialog.exec()


        def create_wzsound(self):
            extract_rwavs(self.working_directory, self.project_name)
            too_big_list, exact_match_list = check_modified_vs_unmodified(self.working_directory, self.project_name)

            progress_dialog = ProgressDialog(self)
            cancel_flag = {'cancelled': False}

            # Connect close signal to update cancel_flag
            progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))

            progress_dialog.show()
            QApplication.processEvents()

            completed = create_patch_file(
                self.working_directory,
                self.project_name,
                too_big_list,
                exact_match_list,
                progress_ui=progress_dialog.ui,
                cancel_flag=cancel_flag
            )

            progress_dialog.close()

            if not completed:
                QMessageBox.critical(self, "Cancelled", "Operation cancelled by user.")
                return

            dialog = ReportDialog(self.working_directory, self.project_name, too_big_list, exact_match_list, self)
            dialog.exec()

        def setup_project(self):
                print("Setting up project...")

                # Clear both lists
                self.ui.list_options.clear()
                self.ui.list_project.clear()

                # Paths
                instructions_path = os.path.join(self.working_directory, "Instructions")
                project_path = os.path.join(self.working_directory, "Projects", self.project_name)
                instructions_yaml_path = os.path.join(project_path, "instructions.yaml")

                # Read selected instructions from project
                selected_instructions = []
                if os.path.exists(instructions_yaml_path):
                        try:
                                with open(instructions_yaml_path, "r", encoding="utf-8") as f:
                                        selected_instructions = yaml.safe_load(f) or []
                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to load instructions.yaml:\n{e}")
                                return

                # Normalize selected instructions (in case someone edited it)
                selected_set = set(item.strip() for item in selected_instructions)

                # All instruction files
                if not os.path.exists(instructions_path):
                        QMessageBox.warning(self, "Missing Folder", "Instructions folder not found.")
                        return

                yaml_files = [f for f in os.listdir(instructions_path) if f.endswith(".yaml")]

                if not yaml_files:
                        QMessageBox.information(self, "No Files", "No YAML files found in Instructions.")
                        return

                # Split between project list and available options
                for file in yaml_files:
                        name_no_ext = os.path.splitext(file)[0]
                        formatted_name = name_no_ext.replace("_", " ").title()

                        if formatted_name in selected_set:
                                self.ui.list_project.addItem(formatted_name)
                        else:
                                self.ui.list_options.addItem(formatted_name)

                print(f"Setup complete. {self.ui.list_project.count()} in project, {self.ui.list_options.count()} available.")

        def update_project_buttons_state(self):
                is_enabled = bool(self.project_name)

                self.ui.button_move.setEnabled(is_enabled)
                self.ui.button_create_brwsd.setEnabled(is_enabled)
                self.ui.button_create_wzsound.setEnabled(is_enabled)

if __name__ == "__main__":
        app = QApplication(sys.argv)

        # Get the parent directory of the current script file
        test_working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test"))

        # Pass it into your main window
        widget = WZSPI_MainWindow(test_working_directory)
        widget.show()

        sys.exit(app.exec())
