import PyQt5.QtWidgets

import sys
import gui_window_src

class MainWindow(PyQt5.QtWidgets.QMainWindow,  gui_window_src.Ui_MainWindow) :

    def __init__(self, parent=None):
        super(PyQt5.QtWidgets.QMainWindow, self).__init__(parent)
        self.setupUi(self)

        #Now start with real connections


if __name__ == '__main__' :
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec()