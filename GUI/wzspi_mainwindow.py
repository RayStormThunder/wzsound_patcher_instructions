# This Python file uses the following encoding: utf-8
import sys
import os
import re
import yaml
import shutil
import subprocess

from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QMainWindow, QMessageBox, QInputDialog, QPushButton
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

try:
        from rwav_extract import setup_extraction
        print("imported rwav_extract")
except ImportError as e:
        print("failed to import rwav_extract")
        pass

try:
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

