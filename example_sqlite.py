from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton
import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()  # Returns the parent of the class and constructs
        self.setWindowTitle("Age Calculator by gruand")
        grid = QGridLayout()

        # Create widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_birth_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.date_birth_field = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # Add widgets to greed
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_birth_label, 1, 0)
        grid.addWidget(self.date_birth_field, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)  # Spanning across 1 row and 2 columns

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.date_birth_field.text()
        year_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old. ")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
