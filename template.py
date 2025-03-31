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

        # Conectar botón "actualizar" a la función update_all
        self.actualizar.clicked.connect(self.update_all)

        # Configuración del ploteo de tiempo
        self.figure_tiempo = Figure(figsize=(3, 2), dpi=80)
        self.canvas_tiempo = FigureCanvas(self.figure_tiempo)
        self.plot_tiempo_layout.addWidget(NavigationToolbar(self.canvas_tiempo, self))
        canvas_index_tiempo = self.plot_tiempo.addWidget(self.canvas_tiempo)
        self.plot_tiempo.setCurrentIndex(canvas_index_tiempo)
        self.ax1 = self.figure_tiempo.add_subplot(1, 1, 1)

        # Configuración del ploteo de frecuencia
        self.figure_frec = Figure(figsize=(3, 2), dpi=80)
        self.canvas_frec = FigureCanvas(self.figure_frec)
        self.frec_plot_layout.addWidget(NavigationToolbar(self.canvas_frec, self))
        canvas_index_frec = self.frec_plot.addWidget(self.canvas_frec)
        self.frec_plot.setCurrentIndex(canvas_index_frec)
        self.ax2 = self.figure_frec.add_subplot(1, 1, 1)

        # Crear instancia de generador de señal
        signal_generator = SignalGen()
        self.signal = np.array([])

        # Crear arreglo de stages
        self.stages = []  # Arreglo de stages

        # Agregar stages al arreglo con nombres descriptivos
        self.stages.append(signal_generator)
        faa_stage = FAA(StageIDs.FAA)
        self.stages.append(faa_stage)
        sample_and_hold_stage = SampleAndHold()
        self.stages.append(sample_and_hold_stage)
        analog_switch_stage = LlaveAnalogica()
        self.stages.append(analog_switch_stage)
        second_faa_stage = FAA(StageIDs.FR)
        self.stages.append(second_faa_stage)

    def update_all(self):
        # Limpiar gráficos actuales
        self.ax1.clear()
        self.canvas_tiempo.draw()
        self.ax2.clear()
        self.canvas_frec.draw()

        # Procesamiento de señales
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

        # Graficar resultados
        for stage in self.stages:
            stage.plot_stage_time(self.ax1)
            stage.plot_stage_freq(self.ax2)
        self.canvas_tiempo.draw()
        self.canvas_frec.draw()
        self.ax1.legend()
        self.ax2.legend()
