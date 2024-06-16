import sys
from PySide6.QtWidgets import QApplication,QWidget
from abwidget import AbWidget

app = QApplication(sys.argv)

window = AbWidget()
window.show()

app.exec()
