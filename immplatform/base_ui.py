from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import main

class WidgetUI(QWidget):

    def __init__(self, main=None):
        QWidget.__init__(self, main)
        self.main = main

    def initUi(self):
        return True
