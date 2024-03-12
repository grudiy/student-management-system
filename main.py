from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Management")

        file_menu_item = self.menuBar().addMenu("&File")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        help_menu_item = self.menuBar().addMenu("&Help")

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Phone"))
        self.setCentralWidget(self.table)

    def load_data(self):
        pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())