from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Management")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())