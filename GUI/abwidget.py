from PySide6.QtWidgets import QPushButton,QWidget,QHBoxLayout,QVBoxLayout

class AbWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AbbyWidget")
        button1 = QPushButton("I Love Abby")
        button1.clicked.connect(self.button1_clicked)
        button2 = QPushButton("I Don't Love Abby")
        button2.clicked.connect(self.button2_clicked)

        button_layout = QVBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        self.setLayout(button_layout)

    def button1_clicked(self):
        print("YESS!!!")
    def button2_clicked(self):
        print("Go back choose again")