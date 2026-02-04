# This Python file uses the following encoding: utf-8
import sys
import os
import re
import struct
import hashlib
import yaml
import shutil
import subprocess
import ctypes

from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QMainWindow, QMessageBox, QInputDialog, QPushButton, QVBoxLayout, QLineEdit, QLabel, QListWidget, QTextEdit, QComboBox
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QCursor, QIcon
from PySide6.QtCore import QTimer, QStringListModel, Signal, QEvent, Qt

# Try importing ui_form from current directory or GUI folder
try:
        from ui_form import Ui_WZSPI_MainWindow
except ImportError:
        try:
                from GUI.ui_form import Ui_WZSPI_MainWindow
        except ImportError as e:
                raise ImportError("Could not import Ui_WZSPI_MainWindow from ui_form or GUI.ui_form") from e

# Try importing hover_text from current directory or GUI folder
try:
        from hover_text import get_hover_descriptions
except ImportError:
        try:
                from GUI.hover_text import get_hover_descriptions
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

try:
        from rwav_extract import setup_extraction, setup_extraction_converted, setup_extraction_HD
except ImportError as e:
        print("failed to import rwav_extract")
        pass

try:
        from rwar_extract import extract_rwar_files, remove_duplicate_files
except ImportError as e:
        print("failed to import rwar_extract")
        pass

try:
        from brwsd_creator import build_brwsd_from_unmodified_rwavs
except ImportError as e:
        print("failed to import brwsd_creator")
        pass

try:
        from extract_brwsd import extract_rwavs, check_modified_vs_unmodified
except ImportError as e:
        print("failed to import extract_brwsd")
        pass

try:
        from patch_creator import create_patch_file
except ImportError as e:
        print("failed to import patch_creator")
        pass

try:
        from patch_wzsound import apply_wzsound_patch
except ImportError as e:
        print("failed to import patch_wzsound")
        pass

# Import version information
try:
    from version import VERSION, COMMIT_ID
except ImportError:
    VERSION, COMMIT_ID = "v0.0.0", "badcafe"

def get_file_hash(file_path, hash_type='sha256'):
        hasher = hashlib.new(hash_type)
        with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                        hasher.update(chunk)
        return hasher.hexdigest()

EXPECTED_SD_HASH = "917b19ae47307be10ecb894fdc77b5e03aeae390748449cee5663099b34034d1"
EXPECTED_HD_HASH = "6e4b9ad376df1d815326aa4e3d44de47872e3ebac57aee95cf28956a8a1ae960"

ALLOW_CUTSCENES = True
IS_PROJECT_LOADED = False
IS_CUTSCENE_FOLDER_CREATED = False
IS_HD_CUTSCENE_FOLDER_CREATED = False

def is_valid_filename(name):
        # Only allow letters, numbers, spaces, underscores, and dashes
        return bool(re.fullmatch(r'[A-Za-z0-9 _-]+', name))


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

class ProgressDialog(QDialog):
        cancelled = Signal()  # Custom signal emitted if the window is closed by user

        def __init__(self, parent=None, generated_text_message: str = ""):
                super().__init__(parent)
                self.ui = Ui_Dialog_Progress()
                self.ui.setupUi(self)

                # Set message
                if hasattr(self.ui, "generated_text"):
                        self.ui.generated_text.setText(generated_text_message)

                # Apply custom style to progress bar
                if hasattr(self.ui, "progressBar"):
                        self.ui.progressBar.setStyleSheet("""
                                QProgressBar {
                                        height: 20px;
                                        border: 1px solid #888;
                                        border-radius: 5px;
                                        background-color: #e0e0e0;
                                        text-align: center;
                                        font-weight: bold;
                                        color: black;
                                }
                                QProgressBar::chunk {
                                        background-color: #8950ba;
                                        border-radius: 5px;
                                }
                        """)

        def closeEvent(self, event):
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
                file_path, _ = QFileDialog.getOpenFileName(self, "Select SD WZSound.brsar", "", "BRSAR Files (*.brsar)")
                if file_path:
                        file_hash = get_file_hash(file_path)
                        print(f"File hash: {file_hash}")

                        if file_hash != EXPECTED_SD_HASH:
                                QMessageBox.critical(self, "Invalid File", "The selected file does not match the expected SD WZSound.brsar. Make sure you submit an UNMODIFIED SD WZSound.brsar")
                                return


                        try:
                                if not os.path.exists(self.program_data_dir):
                                        os.makedirs(self.program_data_dir)

                                copy_dialog = ProgressDialog(
                                        self,
                                        generated_text_message="Copying SD WZSound.brsar to Program Data Folder..."
                                )
                                copy_dialog.setWindowTitle("Copying File")
                                copy_dialog.ui.progressBar.setMaximum(0)
                                copy_dialog.ui.progressBar.setValue(0)
                                copy_dialog.show()
                                QApplication.processEvents()

                                shutil.copy(file_path, self.wzsound_path)

                                copy_dialog.close()
                                print(f"Copied WZSound.brsar to: {self.wzsound_path}")

                                progress_dialog = ProgressDialog(
                                        self,
                                        generated_text_message="Extracting RWAR files from WZSound SD..."
                                )
                                cancel_flag = {'cancelled': False}
                                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))

                                progress_dialog.setWindowTitle("Extracting RWAR")
                                progress_dialog.show()
                                QApplication.processEvents()

                                working_directory = os.path.dirname(sys.executable)
                                extract_rwar_files(
                                        self.wzsound_path,
                                        working_directory,
                                        target_folder="IndexesSD",
                                        progress_ui=progress_dialog.ui,
                                        cancel_flag=cancel_flag
                                )

                                progress_dialog.close()
                                self.accept()

                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to copy or extract file:\n{e}")



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
                        file_hash = get_file_hash(file_path)
                        print(f"File hash: {file_hash}")

                        if file_hash != EXPECTED_HD_HASH:
                                QMessageBox.critical(self, "Invalid File", "The selected file does not match the expected HD WZSound.brsar. Make sure you submit an UNMODIFIED HD WZSound.brsar")
                                self.reject()
                                return

                        try:
                                if not os.path.exists(self.program_data_dir):
                                        os.makedirs(self.program_data_dir)

                                copy_dialog = ProgressDialog(
                                        self,
                                        generated_text_message="Copying HD WZSound.brsar to Program Data Folder..."
                                )
                                copy_dialog.setWindowTitle("Copying File")
                                copy_dialog.ui.progressBar.setMaximum(0)
                                copy_dialog.ui.progressBar.setValue(0)
                                copy_dialog.show()
                                QApplication.processEvents()

                                shutil.copy(file_path, self.hd_wzsound_path)

                                copy_dialog.close()
                                print(f"Copied HD WZSound.brsar to: {self.hd_wzsound_path}")

                                progress_dialog = ProgressDialog(
                                        self,
                                        generated_text_message="Extracting RWAR files from WZSound HD..."
                                )
                                cancel_flag = {'cancelled': False}
                                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))

                                progress_dialog.setWindowTitle("Extracting RWAR (HD)")
                                progress_dialog.show()
                                QApplication.processEvents()

                                working_directory = os.path.dirname(sys.executable)
                                extract_rwar_files(
                                        self.hd_wzsound_path,
                                        working_directory,
                                        target_folder="IndexesHD",
                                        progress_ui=progress_dialog.ui,
                                        cancel_flag=cancel_flag
                                )

                                progress_dialog.close()
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
                self.ui.button_load_project.clicked.connect(self.load_project)
                self.ui.button_create_project.clicked.connect(self.create_project)
                self.ui.button_create_instructions.clicked.connect(self.create_instructions)
                self.ui.button_edit_instructions.clicked.connect(self.edit_instructions)
                self.ui.button_move.clicked.connect(self.move)
                self.ui.button_cancel_changes.clicked.connect(self.cancel_changes)
                self.ui.button_save_changes.clicked.connect(self.save_changes)
                self.ui.button_create_brwsd.clicked.connect(
                        lambda: self.create_brwsd(keep_dialog=True)
                )
                self.ui.button_create_wzsound.clicked.connect(self.create_wzsound)
                self.ui.button_upload_sd_cutscene.clicked.connect(lambda: self.create_cutscenes())
                self.ui.button_upload_hd_cutscene.clicked.connect(lambda: self.create_cutscenes_hd())

                # Connect patch_sd to run_patch
                self.ui.patch_sd.clicked.connect(self.run_patch)
                self.ui.patch_hd.clicked.connect(self.handle_patch_hd_click)
                self.ui.button_convert_project.clicked.connect(self.open_modified_input_dialog)

                self.ui.list_options.itemSelectionChanged.connect(lambda: self.ui.list_project.clearSelection())
                self.ui.list_project.itemSelectionChanged.connect(lambda: self.ui.list_options.clearSelection())

                self.ui.load_sd.clicked.connect(self.open_modified_sd_wzsound)
                self.ui.load_hd.clicked.connect(self.open_modified_hd_wzsound)
                self.ui.button_load_brwsd_folder.clicked.connect(self.open_brwsd)
                self.ui.button_load_instructions_folder.clicked.connect(self.open_instructions)
                self.ui.combo_allow_cutscene.currentIndexChanged.connect(
                        self.on_allow_cutscene_changed
                )



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
                    QListWidget::item:selected {
                        background-color: #2d1245;
                        color: white;
                    }
                """)

                self.ui.list_project.setStyleSheet("""
                    QListWidget {
                        background-color: #1e1e1e;
                        alternate-background-color: #2c2c2c;
                        color: white;
                    }
                    QListWidget::item:selected {
                        background-color: #2d1245;
                        color: white;
                    }
                """)

                self.is_editing_yaml = False
                self.ui.text_yaml_edit.focusInEvent = self.on_yaml_focus_in
                self.ui.text_yaml_edit.focusOutEvent = self.on_yaml_focus_out
                self.ui.description_text.setFocusPolicy(Qt.NoFocus)
                self.ui.description_text.setReadOnly(True)
                self.ui.description_text.setOpenExternalLinks(True)
                self.ui.description_text.setTextInteractionFlags(Qt.TextBrowserInteraction)




                # Syntax highlighter
                self.highlighter = YamlHighlighter(self.ui.text_yaml_edit.document())

                if hasattr(self.ui, "validateButton"):
                        self.ui.validateButton.clicked.connect(self.validate_yaml)

                self.update_cutscene_ui_state()

                # Description Text
                self.hover_descriptions = get_hover_descriptions()

                for name, widget in self.ui.__dict__.items():
                        if isinstance(widget, (QPushButton, QListWidget, QComboBox)) and name in self.hover_descriptions:
                                widget.installEventFilter(self)

                # Install event filters on buttons and lists
                for name, widget in self.ui.__dict__.items():
                        if isinstance(widget, (QPushButton, QListWidget, QComboBox)) and name in self.hover_descriptions:
                                widget.installEventFilter(self)

        def update_cutscene_ui_state(self):
                # Paths
                sd_demo = os.path.join(self.working_directory, "ProgramData", "demo")
                hd_demo = os.path.join(self.working_directory, "ProgramData", "demoHD")

                has_sd_demo = os.path.isdir(sd_demo)
                has_hd_demo = os.path.isdir(hd_demo)

                # Defaults
                self.ui.combo_allow_cutscene.setEnabled(False)
                self.ui.combo_allow_cutscene.setVisible(False)

                self.ui.button_upload_sd_cutscene.setVisible(True)
                self.ui.button_upload_hd_cutscene.setVisible(True)

                # --- SD cutscene logic ---
                if has_sd_demo:
                        # SD cutscene folder already exists
                        self.ui.button_upload_sd_cutscene.setVisible(False)
                        self.ui.combo_allow_cutscene.setVisible(True)
                else:
                        if IS_PROJECT_LOADED:
                                self.ui.combo_allow_cutscene.setEnabled(True)

                # --- HD cutscene logic ---
                if has_hd_demo:
                        self.ui.button_upload_hd_cutscene.setVisible(False)
                        self.ui.combo_allow_cutscene.setVisible(True)
                else:
                        if IS_PROJECT_LOADED:
                                self.ui.combo_allow_cutscene.setEnabled(True)

        def on_allow_cutscene_changed(self, index: int):
                global ALLOW_CUTSCENES
                ALLOW_CUTSCENES = (index == 0)
                project_dir = os.path.join(self.working_directory, "Projects", self.project_name)
                self.write_cutscenes_flag(project_dir, ALLOW_CUTSCENES)

        def write_cutscenes_flag(self, base_folder: str, value: bool) -> None:
                path = os.path.join(base_folder, "cutscene.txt")
                with open(path, "w", encoding="utf-8") as f:
                        f.write("true" if value else "false")

        def read_cutscenes_flag(self, base_folder: str) -> bool:
                path = os.path.join(base_folder, "cutscene.txt")

                # If file does not exist → create it with true
                if not os.path.exists(path):
                        self.write_cutscenes_flag(base_folder, True)
                        return True

                try:
                        with open(path, "r", encoding="utf-8") as f:
                                return f.read().strip().lower() == "true"
                except Exception:
                        # Fail-safe default
                        return True

        def create_cutscenes(self):
                # Folder picker
                src_dir = QFileDialog.getExistingDirectory(
                        self,
                        "Select folder demo folder containing SD .brsar files",
                        self.working_directory
                )
                if not src_dir:
                        return

                # Destinations
                programdata_demo = os.path.join(self.working_directory, "ProgramData", "demo")
                flat_out = os.path.join(self.working_directory, "IndexesSD")  # <- no /demo
                temp_root = os.path.join(flat_out, "_tmp_extract")

                os.makedirs(programdata_demo, exist_ok=True)
                os.makedirs(flat_out, exist_ok=True)
                os.makedirs(temp_root, exist_ok=True)

                # Find .brsar files (recursive)
                brsar_files = []
                for root, _, files in os.walk(src_dir):
                        for fn in files:
                                if fn.lower().endswith(".brsar"):
                                        brsar_files.append(os.path.join(root, fn))

                if not brsar_files:
                        QMessageBox.information(self, "No Files Found", "No .brsar files were found in that folder.")
                        return

                copied = 0
                extracted = 0
                moved = 0
                errors = []

                # ---- COPY PHASE ----
                for src_path in brsar_files:
                        try:
                                dest_path = os.path.join(programdata_demo, os.path.basename(src_path))
                                shutil.copy2(src_path, dest_path)
                                copied += 1
                        except Exception as e:
                                errors.append(f"Copy failed: {os.path.basename(src_path)} → {e}")

                # ---- EXTRACTION + FLATTEN PHASE ----
                for fn in os.listdir(programdata_demo):
                        if not fn.lower().endswith(".brsar"):
                                continue

                        brsar_path = os.path.join(programdata_demo, fn)
                        brsar_stem = os.path.splitext(fn)[0]

                        # Extract into temp subfolder
                        temp_folder_rel = os.path.join("IndexesSD", "_tmp_extract", brsar_stem)  # <- no /demo
                        temp_folder_abs = os.path.join(self.working_directory, temp_folder_rel)

                        try:
                                # Ensure clean temp folder
                                if os.path.exists(temp_folder_abs):
                                        shutil.rmtree(temp_folder_abs)
                                os.makedirs(temp_folder_abs, exist_ok=True)

                                extract_rwar_files(
                                        brsar_path,
                                        self.working_directory,
                                        target_folder=temp_folder_rel
                                )
                                extracted += 1

                                # Move extracted files into flat_out
                                for out_name in os.listdir(temp_folder_abs):
                                        src_out = os.path.join(temp_folder_abs, out_name)

                                        if not os.path.isfile(src_out):
                                                continue

                                        # out_name example: "Index_025_621.brwsd"
                                        out_stem, out_ext = os.path.splitext(out_name)

                                        # Remove "Index_" prefix if present, keep the rest (e.g. "025_621")
                                        if out_stem.startswith("Index_"):
                                                out_stem = out_stem[len("Index_"):]

                                        # Final name: "CutsceneA_025_621.brwsd"
                                        flat_name = f"{brsar_stem}_{out_stem}{out_ext}"
                                        dst_out = os.path.join(flat_out, flat_name)

                                        # If exists, suffix
                                        if os.path.exists(dst_out):
                                                base, ext = os.path.splitext(flat_name)
                                                n = 2
                                                while True:
                                                        alt = os.path.join(flat_out, f"{base}_{n}{ext}")
                                                        if not os.path.exists(alt):
                                                                dst_out = alt
                                                                break
                                                        n += 1

                                        shutil.move(src_out, dst_out)
                                        moved += 1

                        except Exception as e:
                                errors.append(f"Extract/flatten failed: {fn} → {e}")

                # Cleanup temp
                try:
                        if os.path.exists(temp_root):
                                shutil.rmtree(temp_root)
                except Exception:
                        pass

                try:
                        remove_duplicate_files(flat_out)
                except Exception as e:
                        errors.append(f"Duplicate cleanup failed → {e}")

                msg = (
                        f"Copied: {copied} .brsar file(s)\n"
                        f"Extracted: {extracted} archive(s)\n"
                        f"Flattened files moved: {moved}\n\n"
                        f"Flat output folder:\n{flat_out}"
                )

                if errors:
                        msg += "\n\nErrors:\n" + "\n".join(errors[:10])
                        if len(errors) > 10:
                                msg += f"\n...and {len(errors) - 10} more"

                QMessageBox.information(self, "Cutscene Extraction Complete", msg)
                self.update_cutscene_ui_state()


        def create_cutscenes_hd(self):
                # Folder picker
                src_dir = QFileDialog.getExistingDirectory(
                        self,
                        "Select folder demo folder containing HD .brsar files",
                        self.working_directory
                )
                if not src_dir:
                        return

                # Destinations
                programdata_demo = os.path.join(self.working_directory, "ProgramData", "demoHD")
                flat_out = os.path.join(self.working_directory, "IndexesHD")  # <- no /demo
                temp_root = os.path.join(flat_out, "_tmp_extract")

                os.makedirs(programdata_demo, exist_ok=True)
                os.makedirs(flat_out, exist_ok=True)
                os.makedirs(temp_root, exist_ok=True)

                # Find .brsar files (recursive)
                brsar_files = []
                for root, _, files in os.walk(src_dir):
                        for fn in files:
                                if fn.lower().endswith(".brsar"):
                                        brsar_files.append(os.path.join(root, fn))

                if not brsar_files:
                        QMessageBox.information(self, "No Files Found", "No .brsar files were found in that folder.")
                        return

                copied = 0
                extracted = 0
                moved = 0
                errors = []

                # ---- COPY PHASE ----
                for src_path in brsar_files:
                        try:
                                dest_path = os.path.join(programdata_demo, os.path.basename(src_path))
                                shutil.copy2(src_path, dest_path)
                                copied += 1
                        except Exception as e:
                                errors.append(f"Copy failed: {os.path.basename(src_path)} → {e}")

                # ---- EXTRACTION + FLATTEN PHASE ----
                for fn in os.listdir(programdata_demo):
                        if not fn.lower().endswith(".brsar"):
                                continue

                        brsar_path = os.path.join(programdata_demo, fn)
                        brsar_stem = os.path.splitext(fn)[0]

                        # Extract into temp subfolder
                        temp_folder_rel = os.path.join("IndexesHD", "_tmp_extract", brsar_stem)  # <- no /demo
                        temp_folder_abs = os.path.join(self.working_directory, temp_folder_rel)

                        try:
                                # Ensure clean temp folder
                                if os.path.exists(temp_folder_abs):
                                        shutil.rmtree(temp_folder_abs)
                                os.makedirs(temp_folder_abs, exist_ok=True)

                                extract_rwar_files(
                                        brsar_path,
                                        self.working_directory,
                                        target_folder=temp_folder_rel
                                )
                                extracted += 1

                                # Move extracted files into flat_out
                                for out_name in os.listdir(temp_folder_abs):
                                        src_out = os.path.join(temp_folder_abs, out_name)

                                        if not os.path.isfile(src_out):
                                                continue

                                        # out_name example: "Index_025_621.brwsd"
                                        out_stem, out_ext = os.path.splitext(out_name)

                                        # Remove "Index_" prefix if present, keep the rest (e.g. "025_621")
                                        if out_stem.startswith("Index_"):
                                                out_stem = out_stem[len("Index_"):]

                                        # Final name: "CutsceneA_025_621.brwsd"
                                        flat_name = f"{brsar_stem}_{out_stem}{out_ext}"
                                        dst_out = os.path.join(flat_out, flat_name)

                                        # If exists, suffix
                                        if os.path.exists(dst_out):
                                                base, ext = os.path.splitext(flat_name)
                                                n = 2
                                                while True:
                                                        alt = os.path.join(flat_out, f"{base}_{n}{ext}")
                                                        if not os.path.exists(alt):
                                                                dst_out = alt
                                                                break
                                                        n += 1

                                        shutil.move(src_out, dst_out)
                                        moved += 1

                        except Exception as e:
                                errors.append(f"Extract/flatten failed: {fn} → {e}")

                # Cleanup temp
                try:
                        if os.path.exists(temp_root):
                                shutil.rmtree(temp_root)
                except Exception:
                        pass

                try:
                        remove_duplicate_files(flat_out)
                except Exception as e:
                        errors.append(f"Duplicate cleanup failed → {e}")

                msg = (
                        f"Copied: {copied} .brsar file(s)\n"
                        f"Extracted: {extracted} archive(s)\n"
                        f"Flattened files moved: {moved}\n\n"
                        f"Flat output folder:\n{flat_out}"
                )

                if errors:
                        msg += "\n\nErrors:\n" + "\n".join(errors[:10])
                        if len(errors) > 10:
                                msg += f"\n...and {len(errors) - 10} more"

                QMessageBox.information(self, "Cutscene Extraction Complete", msg)
                self.update_cutscene_ui_state()



        def on_yaml_focus_in(self, event):
                self.is_editing_yaml = True
                self.ui.description_text.setHtml(self.hover_descriptions["text_yaml_edit"])
                QTextEdit.focusInEvent(self.ui.text_yaml_edit, event)

        def on_yaml_focus_out(self, event):
                self.is_editing_yaml = False

                # Only clear if not hovering another relevant widget
                cursor_widget = QApplication.widgetAt(QCursor.pos())
                hovered_name = next(
                        (name for name, widget in self.ui.__dict__.items() if widget == cursor_widget),
                        None
                )

                if not hovered_name or hovered_name not in self.hover_descriptions:
                        self.ui.description_text.clear()

                QTextEdit.focusOutEvent(self.ui.text_yaml_edit, event)


        def eventFilter(self, source, event):
                if event.type() == QEvent.Enter:
                        for name, widget in self.ui.__dict__.items():
                                if widget == source and name in self.hover_descriptions:
                                        self.ui.description_text.setHtml(self.hover_descriptions[name])
                                        break
                elif event.type() == QEvent.Leave:
                        if self.is_editing_yaml:
                                self.ui.description_text.setHtml(self.hover_descriptions["text_yaml_edit"])
                return super().eventFilter(source, event)




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
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Modified SD WZSound.brsar", "", "BRSAR Files (*.brsar)")
                if not file_path:
                        QMessageBox.information(self, "Cancelled", "No file selected.")
                        return

                # Step 3: Copy the selected file into the project folder and extract RWARs with progress
                try:
                        modified_dir = os.path.join(project_dir, "InputWZSoundSD")
                        os.makedirs(modified_dir, exist_ok=True)

                        # Copy to ModifiedWZSound/WZSound.brsar
                        dest_path = os.path.join(modified_dir, "WZSound.brsar")
                        shutil.copy(file_path, dest_path)
                        print(f"[INFO] Copied modified WZSound to: {dest_path}")

                        # Show progress dialog
                        progress_dialog = ProgressDialog(self, generated_text_message="Extracting RWAR files...")
                        progress_dialog.setWindowTitle("Extracting RWAR")
                        cancel_flag = {"cancelled": False}
                        progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))
                        progress_dialog.show()
                        QApplication.processEvents()

                        target_folder = os.path.join("Projects", project_name, "Indexes")
                        extract_rwar_files(
                                dest_path,
                                self.working_directory,
                                target_folder=target_folder,
                                progress_ui=progress_dialog.ui,
                                cancel_flag=cancel_flag
                        )

                        progress_dialog.close()

                except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to copy file:\n{e}")
                        return


                # Step 4: You can store the instruction file name, or continue processing here
                print(f"[SUCCESS] Project setup complete for '{project_name}' with instruction file '{instruction_file}'")

                # Step 5: Compare Indexes and generate instruction YAML
                modified_indexes = os.path.join(project_dir, "Indexes")
                original_indexes = os.path.join(self.working_directory, "IndexesSD")
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
                                yaml.dump([instruction_name_without_ext.replace("_", " ")], f, default_flow_style=False)
                        print(f"[INFO] Wrote instructions.yaml to: {instruction_list_path}")
                except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to write instructions.yaml:\n{e}")
                        return

                # Step 7: Generate converted BRWSD using final project name
                self.create_brwsd_converted(project_name)

        def create_brwsd_converted(self, project_name):
                project_dir = os.path.join(self.working_directory, "Projects", project_name)
                allow_cutscenes = self.read_cutscenes_flag(project_dir)

                progress_dialog = ProgressDialog(
                        self,
                        generated_text_message="Starting BRWSD Creation..."
                )
                progress_dialog.setWindowTitle("Creating BRWSD")
                cancel_flag = {"cancelled": False}
                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))
                progress_dialog.show()
                QApplication.processEvents()

                extract_rwavs(
                        self.working_directory,
                        project_name,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                setup_extraction(
                        self.working_directory,
                        project_name,
                        allow_cutscenes=allow_cutscenes,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                setup_extraction_converted(
                        self.working_directory,
                        project_name,
                        allow_cutscenes=allow_cutscenes,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                build_brwsd_from_unmodified_rwavs(
                        self.working_directory,
                        project_name,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                progress_dialog.close()

                dialog = SuccessDialog(self.working_directory, project_name, self)

                self.project_name = project_name
                self.ui.label_project.setText(self.project_name.replace("_", " ").title())
                self.setup_project()

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
                layout.addWidget(QLabel("Instruction File Name (Should be a short description of the types of sounds you edited):"))
                layout.addWidget(instruction_input)
                layout.addWidget(QLabel("Submit an SD WZSound file that IS MODIFIED with sound effects already replaced in it"))
                layout.addWidget(submit_button)

                def on_submit():
                        project_name = project_input.text().strip()
                        instruction_file = instruction_input.text().strip()

                        if not project_name or not instruction_file:
                                QMessageBox.warning(dialog, "Missing Input", "Both fields must be filled.")
                                return

                        if not is_valid_filename(project_name):
                                QMessageBox.critical(
                                        dialog,
                                        "Invalid Project Name",
                                        "Project name may only contain letters, numbers, spaces, underscores (_), and dashes (-)."
                                )
                                return

                        if not is_valid_filename(instruction_file):
                                QMessageBox.critical(
                                        dialog,
                                        "Invalid Instruction File Name",
                                        "Instruction file name may only contain letters, numbers, spaces, underscores (_), and dashes (-)."
                                )
                                return

                        dialog.accept()
                        print(f"Submitted project: {project_name}, instruction file: {instruction_file}")
                        self.convert_modified(project_name, instruction_file)

                submit_button.clicked.connect(on_submit)

                dialog.exec()


        def open_modified_sd_wzsound(self):
                project_path = os.path.join(self.working_directory, "Projects", self.project_name, "ModifiedWZSoundSD")
                if os.path.exists(project_path):
                        subprocess.Popen(f'explorer "{project_path}"')
                else:
                        print("[INFO] SD WZSound file not found.")

        def open_modified_hd_wzsound(self):
                project_path = os.path.join(self.working_directory, "Projects", self.project_name, "ModifiedWZSoundHD")
                if os.path.exists(project_path):
                        subprocess.Popen(f'explorer "{project_path}"')
                else:
                        print("[INFO] HD WZSound file not found.")

        def open_brwsd(self):
                folder_path = os.path.join(self.working_directory, "Projects", self.project_name)
                if os.path.exists(folder_path):
                        subprocess.Popen(f'explorer "{folder_path}"')
                else:
                        print("[INFO] BRWSD folder not found.")

        def open_instructions(self):
                file_path = os.path.join(self.working_directory, "Releases", self.project_name)
                if os.path.exists(file_path):
                        subprocess.Popen(f'explorer "{file_path}"')
                else:
                        print("[INFO] Instructions file not found.")

        def handle_patch_hd_click(self):
                self.create_brwsd()
                indexes_hd_path = os.path.join(self.working_directory, "IndexesHD")

                # If IndexesHD missing, require HD WZSound and extract IndexesHD normally
                if not os.path.exists(indexes_hd_path):
                        dialog = MissingBrsarHDDialog(self.working_directory, self)
                        if dialog.exec() != QDialog.Accepted:
                                print("User cancelled HD WZSound selection.")
                                return
                        else:
                                print("HD WZSound provided.")

                # Proceed with the actual HD patch logic
                self.run_hd_patch()

        def run_hd_patch(self):
                project_dir = os.path.join(self.working_directory, "Projects", self.project_name)
                allow_cutscenes = self.read_cutscenes_flag(project_dir)

                progress_dialog = ProgressDialog(
                        self,
                        generated_text_message="Extracting RWAV files (HD)..."
                )
                progress_dialog.setWindowTitle("Extracting (HD)")
                cancel_flag = {'cancelled': False}
                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))

                progress_dialog.show()
                QApplication.processEvents()

                project_name = self.project_name
                setup_extraction_HD(
                        self.working_directory,
                        project_name,
                        allow_cutscenes=allow_cutscenes,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                progress_dialog.close()

                self.patch_hd_wzsound(self.working_directory, project_name)

        def patch_hd_wzsound(self, working_directory, project_name):
                # ---- PATHS ----
                project_folder = os.path.join(working_directory, "Projects", project_name)

                hd_output_folder = os.path.join(project_folder, "ModifiedWZSoundHD")
                os.makedirs(hd_output_folder, exist_ok=True)

                source_wz_hd = os.path.join(working_directory, "ProgramData", "WZSoundHD.brsar")
                source_demo_dir = os.path.join(working_directory, "ProgramData", "demoHD")

                unmodified_folder = os.path.join(project_folder, "UnmodifiedRwavsHD")
                modified_folder = os.path.join(project_folder, "ModifiedRwavs")

                if not os.path.isfile(source_wz_hd):
                        print(f"[ERROR] Missing HD source file: {source_wz_hd}")
                        return
                if not os.path.isdir(unmodified_folder):
                        print(f"[ERROR] Missing folder: {unmodified_folder}")
                        return
                if not os.path.isdir(modified_folder):
                        print(f"[ERROR] Missing folder: {modified_folder}")
                        return

                # ---- BUILD TARGET LIST (WZSoundHD + demoHD/*.brsar) ----
                targets: list[tuple[str, str]] = []  # (label, full_path)
                targets.append(("WZSound.brsar", source_wz_hd))

                if os.path.isdir(source_demo_dir):
                        for fn in sorted(os.listdir(source_demo_dir)):
                                if fn.lower().endswith(".brsar"):
                                        targets.append((fn, os.path.join(source_demo_dir, fn)))

                if not targets:
                        print("[ERROR] No target .brsar files found.")
                        return

                # ---- LOAD UNMOD+MOD RWAV PAIRS (ONLY WHERE MOD EXISTS) ----
                rwav_pairs: list[tuple[str, bytes, bytes]] = []  # (filename, unmod_data, mod_data)

                unmod_names = [f for f in sorted(os.listdir(unmodified_folder)) if f.lower().endswith(".rwav")]
                if not unmod_names:
                        print("[WARNING] No unmodified RWAVs found in UnmodifiedRwavsHD.")
                        return

                for fn in unmod_names:
                        unmod_path = os.path.join(unmodified_folder, fn)
                        mod_path = os.path.join(modified_folder, fn)

                        # Only usable if a modified version exists
                        if not os.path.isfile(mod_path):
                                continue

                        try:
                                with open(unmod_path, "rb") as f:
                                        unmod_data = f.read()
                                with open(mod_path, "rb") as f:
                                        mod_data = f.read()
                        except Exception:
                                continue

                        # Safety: we only support overwrite-with-pad (mod <= unmod)
                        if len(mod_data) > len(unmod_data):
                                continue

                        rwav_pairs.append((fn, unmod_data, mod_data))

                if not rwav_pairs:
                        print("[WARNING] No RWAV pairs to patch (no matching modified files, or size checks failed).")
                        return

                # ---- SCAN TARGETS FOR RWAV HEADERS ----
                RWAV_MAGIC = b"RWAV\xFE\xFF\x01\x02"

                # label -> {"path": str, "offsets": list[int]}
                target_rwav_index: dict[str, dict] = {}

                for label, path in targets:
                        try:
                                with open(path, "rb") as f:
                                        data = f.read()
                        except Exception as e:
                                print(f"[WARN] Could not read {label}: {e}")
                                target_rwav_index[label] = {"path": path, "offsets": []}
                                continue

                        offsets: list[int] = []
                        start = 0
                        while True:
                                i = data.find(RWAV_MAGIC, start)
                                if i == -1:
                                        break
                                offsets.append(i)
                                start = i + 1

                        target_rwav_index[label] = {"path": path, "offsets": offsets}

                # ---- COUNT TOTAL RWAVS (FOR PROGRESS) ----
                total_rwavs = sum(len(info["offsets"]) for info in target_rwav_index.values())
                if total_rwavs == 0:
                        print("[WARNING] No RWAV headers found in any target file.")
                        return

                # ---- PROGRESS DIALOG ----
                progress_dialog = ProgressDialog(
                        self,
                        generated_text_message="Patching HD WZSound..."
                )
                progress_dialog.setWindowTitle("Patching HD WZSound")
                progress_dialog.ui.progressBar.setMaximum(total_rwavs)
                progress_dialog.ui.progressBar.setValue(0)
                progress_dialog.show()
                QApplication.processEvents()

                step = 0

                def try_patch_at_offset(data: bytearray, offset: int) -> bool:
                        """
                        Checks if ANY unmodified RWAV matches EXACTLY at this offset.
                        If match -> overwrite with modified data (and pad zeros to unmod length).
                        Returns True if changed.
                        """
                        for fn, unmod_data, mod_data in rwav_pairs:
                                end_unmod = offset + len(unmod_data)
                                if end_unmod > len(data):
                                        continue

                                if data[offset:end_unmod] != unmod_data:
                                        continue

                                # Match found: override bytes
                                data[offset:offset + len(mod_data)] = mod_data

                                # Zero out any remaining bytes if mod is smaller
                                remaining = len(unmod_data) - len(mod_data)
                                if remaining > 0:
                                        data[offset + len(mod_data):end_unmod] = b"\x00" * remaining

                                return True

                        return False

                # ---- PATCH ALL TARGETS ----
                out_demo_dir = os.path.join(hd_output_folder, "demo")
                wrote_any_demo = False

                for label, path in targets:
                        try:
                                with open(path, "rb") as f:
                                        data = bytearray(f.read())
                        except Exception as e:
                                print(f"[WARN] Could not read target for patching {label}: {e}")

                                # Still advance progress for this target's headers
                                step += len(target_rwav_index.get(label, {}).get("offsets", []))
                                if hasattr(progress_dialog.ui, "progressBar"):
                                        progress_dialog.ui.progressBar.setValue(step)
                                QApplication.processEvents()
                                continue

                        changed = False
                        offsets = target_rwav_index.get(label, {}).get("offsets", [])

                        for off in offsets:
                                if hasattr(progress_dialog.ui, "label_status"):
                                        progress_dialog.ui.label_status.setText(f"{label} | RWAV @ 0x{off:X}")

                                # Attempt patch at this RWAV header
                                if try_patch_at_offset(data, off):
                                        changed = True

                                # Progress increments PER RWAV HEADER processed (match or not)
                                step += 1
                                if hasattr(progress_dialog.ui, "progressBar"):
                                        progress_dialog.ui.progressBar.setValue(step)
                                QApplication.processEvents()

                        # ---- WRITE OUTPUT RULES ----
                        if label == "WZSound.brsar":
                                # Always output WZSound
                                out_path = os.path.join(hd_output_folder, "WZSound.brsar")
                                try:
                                        with open(out_path, "wb") as f:
                                                f.write(data)
                                except Exception as e:
                                        progress_dialog.close()
                                        print(f"[ERROR] Could not write patched WZSound: {e}")
                                        return
                        else:
                                # Demo: only write if changed
                                if not changed:
                                        continue

                                os.makedirs(out_demo_dir, exist_ok=True)
                                out_path = os.path.join(out_demo_dir, label)
                                try:
                                        with open(out_path, "wb") as f:
                                                f.write(data)
                                        wrote_any_demo = True
                                except Exception as e:
                                        print(f"[ERROR] Could not write patched demo file {label}: {e}")

                # Remove empty demo dir if nothing written
                if not wrote_any_demo:
                        try:
                                if os.path.isdir(out_demo_dir) and not os.listdir(out_demo_dir):
                                        os.rmdir(out_demo_dir)
                        except Exception:
                                pass

                progress_dialog.close()
                self.show_confirmation_hd()



        def run_patch(self):
                progress_dialog = ProgressDialog(
                        self,
                        generated_text_message="Applying patch to SD WZSound.brsar..."
                )
                cancel_flag = {'cancelled': False}
                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))

                progress_dialog.setWindowTitle("Applying Patch")
                progress_dialog.show()
                QApplication.processEvents()

                completed = apply_wzsound_patch(
                        self.working_directory,
                        self.project_name,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                progress_dialog.close()
                if completed:
                        self.show_confirmation()

        def show_confirmation(self):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("WZSound SD Patch Applied")
            msg_box.setText("Successfully applied WZSound SD patch.")

            open_button = msg_box.addButton("Open WZSound Location", QMessageBox.AcceptRole)
            close_button = msg_box.addButton("Close", QMessageBox.RejectRole)

            msg_box.exec()

            if msg_box.clickedButton() == open_button:
                wzsound_folder = os.path.join(self.working_directory, "Projects", self.project_name, "ModifiedWZSoundSD")
                if os.path.exists(wzsound_folder):
                    subprocess.Popen(f'explorer "{wzsound_folder}"')  # Windows only
                else:
                    QMessageBox.warning(self, "Folder Not Found", f"Folder does not exist:\n{wzsound_folder}")

        def show_confirmation_hd(self):
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("WZSound HD Patch Applied")
                msg_box.setText("Successfully applied WZSound HD patch.")

                open_button = msg_box.addButton("Open WZSoundHD Location", QMessageBox.AcceptRole)
                close_button = msg_box.addButton("Close", QMessageBox.RejectRole)

                msg_box.exec()

                if msg_box.clickedButton() == open_button:
                        wzsound_hd_folder = os.path.join(self.working_directory, "Projects", self.project_name, "ModifiedWZSoundHD")
                        if os.path.exists(wzsound_hd_folder):
                                subprocess.Popen(f'explorer "{wzsound_hd_folder}"')  # Windows only
                        else:
                                QMessageBox.warning(self, "Folder Not Found", f"Folder does not exist:\n{wzsound_hd_folder}")


        def convert_project(self):
                self.convert_window = ConvertDialog(self.working_directory, self.project_name, self)
                self.convert_window.exec()  # Use .show() if you want it non-modal


        def load_project(self):
                # Path to the Projects folder
                projects_dir = os.path.join(self.working_directory, "Projects")

                # Ensure the Projects folder exists
                if not os.path.exists(projects_dir):
                        QMessageBox.information(self, "No Projects", "No projects found. Create one first.")
                        return

                # Get list of project folders and sort them by last modified time (descending)
                project_folders = [
                        name for name in os.listdir(projects_dir)
                        if os.path.isdir(os.path.join(projects_dir, name))
                ]

                if not project_folders:
                        QMessageBox.information(self, "No Projects", "No project folders found in the Projects directory.")
                        return

                # Sort by last modified time (most recent first)
                project_folders.sort(
                        key=lambda name: os.path.getmtime(os.path.join(projects_dir, name)),
                        reverse=True
                )

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
                        project_dir = os.path.join(self.working_directory, "Projects", self.project_name)

                        allow_cutscenes = self.read_cutscenes_flag(project_dir)

                        # Block signal so it doesn't re-write the file while setting UI
                        self.ui.combo_allow_cutscene.blockSignals(True)
                        self.ui.combo_allow_cutscene.setCurrentIndex(0 if allow_cutscenes else 1)
                        self.ui.combo_allow_cutscene.blockSignals(False)

                        self.ui.combo_allow_cutscene.setEnabled(True)

                        IS_PROJECT_LOADED = True
                        self.ui.combo_allow_cutscene.setEnabled(True)
                        print(f"Loaded project: {self.project_name}")


        def create_project(self):
                # Prompt the user to enter a project name
                name, ok = QInputDialog.getText(self, "Create Project", "Enter a name for the project:")

                if ok and name.strip():
                        if not is_valid_filename(name):
                                QMessageBox.critical(
                                        self,
                                        "Invalid Name",
                                        "Project name may only contain letters, numbers, spaces, underscores (_), and dashes (-)."
                                )
                                return

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

        def create_instructions(self):

                # Prompt the user to enter a name
                name, ok = QInputDialog.getText(
                        self,
                        "Create Instructions",
                        "Enter a name for this set of instructions. \nIt should explain what types of sound effects it is trying to export."
                )

                if ok and name.strip():
                        if not is_valid_filename(name):
                                QMessageBox.critical(
                                        self,
                                        "Invalid Name",
                                        "Instruction name may only contain letters, numbers, spaces, underscores (_), and dashes (-)."
                                )
                                return

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
                        return

                # Move selected items
                for item in source.selectedItems():
                        target.addItem(item.text())
                        source.takeItem(source.row(item))

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
                except Exception as e:
                        QMessageBox.critical(self, "Save Error", f"Failed to save instructions.yaml:\n{e}")


        def cancel_changes(self):
                self.ui.stacked_pages.setCurrentIndex(0)
                self.ui.text_yaml_edit.setPlainText("")

        def save_changes(self):
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

        def create_brwsd(self, keep_dialog=False):
                project_dir = os.path.join(self.working_directory, "Projects", self.project_name)
                allow_cutscenes = self.read_cutscenes_flag(project_dir)

                progress_dialog = ProgressDialog(self, generated_text_message="Starting BRWSD Creation...")
                progress_dialog.setWindowTitle("Creating BRWSD")
                cancel_flag = {"cancelled": False}
                progress_dialog.cancelled.connect(lambda: cancel_flag.update(cancelled=True))
                progress_dialog.show()
                QApplication.processEvents()

                extract_rwavs(
                        self.working_directory,
                        self.project_name,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                setup_extraction(
                        self.working_directory,
                        self.project_name,
                        allow_cutscenes=allow_cutscenes,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                build_brwsd_from_unmodified_rwavs(
                        self.working_directory,
                        self.project_name,
                        progress_ui=progress_dialog.ui,
                        cancel_flag=cancel_flag
                )

                progress_dialog.close()

                if keep_dialog:
                    dialog = SuccessDialog(self.working_directory, self.project_name, self)
                    dialog.exec()

        def create_wzsound(self):
                self.create_brwsd()
                extract_rwavs(self.working_directory, self.project_name)
                too_big_list, exact_match_list = check_modified_vs_unmodified(self.working_directory, self.project_name)

                progress_dialog = ProgressDialog(
                        self,
                        generated_text_message="Creating patch file, please wait..."
                )
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

                print("[SUCCESS] Create SD Patch Instructions")

        def setup_project(self):
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

                # Build set of valid instruction names (formatted)
                valid_set = {
                        os.path.splitext(f)[0].replace("_", " ").title()
                        for f in yaml_files
                }

                # Remove invalid entries from instructions.yaml
                filtered_instructions = [name for name in selected_set if name in valid_set]

                # Rewrite instructions.yaml if it changed
                if set(filtered_instructions) != selected_set:
                        try:
                                with open(instructions_yaml_path, "w", encoding="utf-8") as f:
                                        yaml.safe_dump(sorted(filtered_instructions), f)
                        except Exception as e:
                                QMessageBox.critical(self, "Error", f"Failed to update instructions.yaml:\n{e}")
                                return

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


        def update_project_buttons_state(self):
                is_enabled = bool(self.project_name) and bool(self.working_directory)

                self.ui.button_move.setEnabled(is_enabled)

                if is_enabled:
                        working_directory = self.working_directory
                        project_name = self.project_name

                        # Paths
                        brwsd_path = os.path.join(working_directory, "Projects", project_name, "your_project.brwsd")
                        instructions_path = os.path.join(working_directory, "Projects", project_name, "instructions.yaml")
                        hd_wzsound_path = os.path.join(working_directory, "Projects", project_name, "ModifiedWZSoundHD", "WZSound.brsar")
                        sd_wzsound_path = os.path.join(working_directory, "Projects", project_name, "ModifiedWZSoundSD", "WZSound.brsar")
                        patch_path = os.path.join(working_directory, "Releases", project_name, "WZSoundPatchInstructions", "wzsound_instructions.patch")

                        # Existence checks
                        brwsd_exists = os.path.exists(brwsd_path)
                        patch_exists = os.path.exists(patch_path)
                        hd_exists = os.path.exists(hd_wzsound_path)
                        sd_exists = os.path.exists(sd_wzsound_path)

                        instructions_exists = False
                        if os.path.exists(instructions_path):
                                with open(instructions_path, "r", encoding="utf-8") as f:
                                        content = f.read().strip()
                                        if content and content != "[]":
                                                instructions_exists = True

                        self.ui.button_load_brwsd_folder.setEnabled(brwsd_exists)
                        self.ui.patch_hd.setEnabled(brwsd_exists)
                        self.ui.button_create_wzsound.setEnabled(brwsd_exists)

                        self.ui.button_load_instructions_folder.setEnabled(patch_exists)
                        self.ui.patch_sd.setEnabled(patch_exists)
                        self.ui.load_sd.setEnabled(sd_exists)
                        self.ui.load_hd.setEnabled(hd_exists)

                        self.ui.button_create_brwsd.setEnabled(instructions_exists)

                else:
                        # Disable all dependent buttons if project_name or working_directory is None
                        self.ui.button_load_brwsd_folder.setEnabled(False)
                        self.ui.patch_hd.setEnabled(False)
                        self.ui.button_load_instructions_folder.setEnabled(False)
                        self.ui.patch_sd.setEnabled(False)
                        self.ui.load_sd.setEnabled(False)
                        self.ui.load_hd.setEnabled(False)
                        self.ui.button_create_brwsd.setEnabled(False)
                        self.ui.button_create_wzsound.setEnabled(False)

if __name__ == "__main__":
        app = QApplication(sys.argv)

        # Get the parent directory of the current script file
        test_working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test"))

        # Pass it into your main window
        widget = WZSPI_MainWindow(test_working_directory)
        widget.show()

        sys.exit(app.exec())
