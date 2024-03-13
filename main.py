from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Students Management")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        # Main menu
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Submenus
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # Hide column with default IDs
        self.setCentralWidget(self.table)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add toolbar elements
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.clicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Clean if there were buttons yet
        children = self.findChildren(QPushButton)
        if children:
            for item in children:
                self.statusbar.removeWidget(item)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students")
        self.table.setRowCount(0)  # Reset the table and load it again fresh
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        cursor.close()
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Student's name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter Student's Name")
        layout.addWidget(self.student_name)

        # Choose Course widget combo box
        self.course_name = QComboBox()
        courses = ["Astronomy", "Biology", "Maths", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add Mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText(" Student's Mobile Phone")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh data in table from DB
        main_window.load_data()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = main_window.table.currentRow()

        # Get ID of selected student
        self.student_id = main_window.table.item(index, 0).text()

        # Get student's name from selected row
        student_name = main_window.table.item(index, 1).text()

        #  Student's name widget with passed name
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Enter Student's Name")
        layout.addWidget(self.student_name)

        # Choose Course combo box widget
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Astronomy", "Biology", "Maths", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add Mobile
        mobile_value = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile_value)
        self.mobile.setPlaceholderText(" Student's Mobile Phone")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Add Student")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ? , mobile = ? WHERE id = ?",
            (self.student_name.text(),
             self.course_name.itemText(self.course_name.currentIndex()),
             self.mobile.text(),
             self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Refresh data in table from DB
        main_window.load_data()

class DeleteDialog(QDialog):
    pass
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Enter Name to Search")
        layout.addWidget(self.search_name)

        # Add search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)

        # Find items in the table
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        # Select cells in table with found items
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()






app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
