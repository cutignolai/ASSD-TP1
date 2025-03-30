from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import signal
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog, QApplication, QListWidgetItem, QMainWindow, QComboBox
from PyQt5 import QtCore
from frontend.front import *
from matplotlib.patches import Rectangle
from backend.FAA import *
from backend.Stage import *
import numpy as np
from backend.Signal import *
from backend.SampleAndHold import *
from backend.Stage import *
from backend.LlaveAnalogica import *
from copy import copy


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Buttons clicked ####
        self.actualizar.clicked.connect(self.update_all)
        # self.update.clicked.connect(self.update_all)
        # Cosas de ploteo #####
        # figure(figsize=(3, 2), dpi=80)7

        self.figure_tiempo = Figure(figsize=(3, 2), dpi=80)
        self.canvas_tiempo = FigureCanvas(self.figure_tiempo)
        self.plot_tiempo_layout.addWidget(NavigationToolbar(self.canvas_tiempo, self))
        canvas_index_tiempo = self.plot_tiempo.addWidget(self.canvas_tiempo)
        self.plot_tiempo.setCurrentIndex(canvas_index_tiempo)
        self.ax1 = self.figure_tiempo.add_subplot(1, 1, 1)

        self.figure_frec = Figure(figsize=(3, 2), dpi=80)
        self.canvas_frec = FigureCanvas(self.figure_frec)
        self.frec_plot_layout.addWidget(NavigationToolbar(self.canvas_frec, self))
        canvas_index_frec = self.frec_plot.addWidget(self.canvas_frec)
        self.frec_plot.setCurrentIndex(canvas_index_frec)
        self.ax2 = self.figure_frec.add_subplot(1, 1, 1)

        # Creo
        # todo: Meter generate_signal al arreglo de stages así después se plotea todo piola con el for
        generate_signal = SignalGen()
        self.signal = np.array([])
        # Creo Array de stages ####
        self.stages = []  # Array with templates

        self.stages.append(generate_signal)
        aux = FAA(StageIDs.FAA)
        self.stages.append(aux)
        aux1 = SampleAndHold()
        self.stages.append(aux1)
        aux2 = LlaveAnalogica()
        # signal_in, FREC, DUTY
        self.stages.append(aux2)
        aux3 = FAA(StageIDs.FR)
        self.stages.append(aux3)

        # self.wrongtemplate = 0

    def update_all(self):
        self.ax1.clear()
        self.canvas_tiempo.draw()
        self.ax2.clear()
        self.canvas_frec.draw()

        # Signal processing
        self.stages[0].update(self.signal, True, self.plot_xin.isChecked(), signal_type=self.Xin.currentText(),
                              A=self.Amplitud.value(), freq=self.Frec_xin.value() * (10 ** 3), phase=0,
                              fs=self.frec_sample.value() * (10 ** 3), DC=self.DC.value())
        self.stages[1].update(copy(self.stages[0].signal_out), self.on_FAA.isChecked(), self.plot_FAA.isChecked(), None,
                              self.Amplitud.value(), self.Frec_xin.value() * (10 ** 3), phase=0,
                              fs=self.frec_sample.value() * (10 ** 3), DC=self.DC.value())
        self.stages[2].update(copy(self.stages[1].signal_out), self.on_SH.isChecked(), self.plot_SH.isChecked(),
                              self.Xin.currentText(), self.Amplitud.value(), self.Frec_xin.value() * (10 ** 3), phase=0,
                              fs=self.frec_sample.value() * (10 ** 3), DC=self.DC.value())
        self.stages[3].update(copy(self.stages[2].signal_out), self.on_LA.isChecked(), self.plot_LA.isChecked(), None,
                              self.Amplitud.value(), self.Frec_xin.value() * (10 ** 3), phase=0,
                              fs=self.frec_sample.value() * (10 ** 3), DC=self.DC.value())
        self.stages[4].update(copy(self.stages[3].signal_out), self.on_FR.isChecked(), self.plot_FR.isChecked(), None,
                              self.Amplitud.value(), self.Frec_xin.value() * (10 ** 3), phase=0,
                              fs=self.frec_sample.value() * (10 ** 3), DC=self.DC.value())

        # Plot

        for i in range(5):
            self.stages[i].plot_stage_time(self.ax1)
            self.stages[i].plot_stage_freq(self.ax2)
        self.canvas_tiempo.draw()
        self.canvas_frec.draw()
        self.ax1.legend()
        self.ax2.legend()
        """
        self.stages[2].update(self.generate_signal.signal_in, self.on_LA.isChecked(),self.plot_LA.isChecked(),self.Xin.currentText(),self.Amplitud.value(), self.Frec_xin.value()*(10**3), phase=0, fs=self.frec_sample.value()*(10**3), DC=self.DC.value())
        #(self, signal_in, is_on, is_plot, signal_type=None, A=None, freq=None, phase=None, fs=None, DC=None)
        if self.plot_SH.isChecked():
            self.stages[2].plot_stage_time(self.ax1)
            self.stages[2].plot_stage_freq(self.ax2)
            self.canvas_tiempo.draw()
            self.canvas_frec.draw()
            self.ax1.legend()

        #signal_in, is_on, is_plot, signal_type = None, amplitude = None, freq = None, phase = None, fs = None, DC = None

        self.stages[1].update(self.stages[0].get_signal_out(), self.on_SH, self.plot_SH, signal_type=None,amplitude=self.Amplitud, freq=self.Frec_xin, phase=0, fs=self.frec_sample, DC=self.DC)
        if self.plot_SH:
            self.stages[1].plot_stage_time(self, self.ax1)
            self.stages[1].plot_stage_freq(self.ax2)
        self.stages[2].update(self.stages[1].get_signal_out(), self.on_LA, self.plot_LA, signal_type=None,amplitude=self.Amplitud, freq=self.Frec_xin, phase=0, fs=self.frec_sample, DC=self.DC)
        if self.plot_LA:
            self.stages[2].plot_stage_time(self, self.ax1)
            self.stages[2].plot_stage_freq(self.ax2)
        self.stages[3].update(self.stages[2].get_signal_out(), self.on_FR, self.plot_FR, signal_type=None,amplitude=self.Amplitud, freq=self.Frec_xin, phase=0, fs=self.frec_sample, DC=self.DC)
        if self.plot_FR:
            self.stages[3].plot_stage_time(self, self.ax1)
            self.stages[3].plot_stage_freq(self.ax2)
        """
