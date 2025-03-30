from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import signal
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog, QApplication, QListWidgetItem, QMainWindow, QComboBox
from PyQt5 import QtCore
from frontend.front import *
from matplotlib.patches import Rectangle
from backend.FAA import *
import numpy as np
from template import *
import sys

# Python Modules

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

"""
if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
