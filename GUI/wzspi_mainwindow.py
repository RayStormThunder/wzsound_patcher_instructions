# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow

# Try importing ui_form from current directory or GUI folder
try:
        # First, try local import (for development/testing inside GUI folder)
        from ui_form import Ui_WZSPI_MainWindow
except ImportError:
        try:
                # Fallback: import from GUI package (used when running from main app / PyInstaller)
                from GUI.ui_form import Ui_WZSPI_MainWindow
        except ImportError as e:
                raise ImportError("Could not import Ui_WZSPI_MainWindow from ui_form or GUI.ui_form") from e

class WZSPI_MainWindow(QMainWindow):
        def __init__(self, parent=None):
                super().__init__(parent)
                self.ui = Ui_WZSPI_MainWindow()
                self.ui.setupUi(self)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        widget = WZSPI_MainWindow()
        widget.show()
        sys.exit(app.exec())
