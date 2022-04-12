import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.gui import DIPGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = DIPGUI()
    Window.show()
    sys.exit(app.exec_())