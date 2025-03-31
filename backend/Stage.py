########################################################################################################################
#                                                   STAGE                                                              #
#                                                                                                                      #
# Clase madre de la que todas las etapas heredan. Define los métodos comunes para todas las etapas, que pueden ser     #
# sobrecargados según la etapa en específico. Cada etapa recibe una señal de entrada (signal_in), la procesa y obtiene #
# la señal de salida (signal_out). Al crearse, sólo recibe el tipo de etapa y crea las variables internas que luego    #
# necesitarán inicializarse con update.                                                                                #
########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
from scipy.fft import fft, fftfreq
from copy import copy


########################################################################################################################
# STAGE IDs: Indica el tipo de etapa que hereda de la clase Stage, es el contenido de la variable stage_id en Stage.

class StageIDs(IntEnum):
    IN = 0      # Etapa de entrada (No hereda de Stage pero queda reservado)
    FAA = 1     # Filtro anti-aliasing
    SH = 2      # Sample & Hold
    LA = 3      # Llave analógica
    FR = 4      # Filtro recuperador
    ERR = -1    # Error
########################################################################################################################


########################################################################################################################
# STAGE TYPE: Nombres de las etapas, se utilizan en los mensajes de error.

StageType = ["Entrada", "Filtro Anti-Aliasing", "Sample & Hold", "Llave Analógica", "Filtro Recuperador", "Error"]
########################################################################################################################


########################################################################################################################
# STAGE COLORS: Color que se asignará a cada tipo de etapa para el gráfico

StageColors = ["royalblue", "darkorange", "seagreen", "crimson", "saddlebrown", "deeppink"]
########################################################################################################################


########################################################################################################################
# CLASE STAGE:

class Stage:

    def __init__(self, stage_id):
        self.stage_id = stage_id
        self.signal_in = None
        self.signal_out = None
        self.is_on = True
        self.is_plot = True
        self.signal_out_f = None

    def process_stage(self, signal_in):
        """
        process_stage:
        * Método privado virtual que procesa la señal de entrada y provee una señal a la salida.
        * Este método deberá ser recargado por cada clase hija.
        * RECIBE LA SEÑAL DE ENTRADA QUE SE DEBE PROCESAR Y MODIFICA signal_out.
        * Devuelve True si se pudo procesar correctamente y signal_out se obtuvo exitosamente, False si hubo un error.
        """

        # Si imprime el siguiente mensaje, es porque no se reemplazo la funcion en la clase heredada
        print("ERROR: No se sobrecargó process_stage() o se creó un objeto Stage")

        self.signal_out = signal_in
        return True

    def error(self):
        """
        error: Método que se utiliza para dar un mensaje de error, imprime un mensaje genérico segun la etapa.
        """
        print("Hubo un error en la etapa " + StageType[self.stage_id])  # Mensaje de error

        return

    def update(self, signal_in, is_on, is_plot, signal_type=None, A=None, freq=None, phase=None, fs=None, DC=None):
        """
        update:
        * Método para actualizar los datos de la etapa.
        * Llama a la función process_stage cuando cambia la señal de entrada.
        * Se puede sobrecargar, pero no lo recomiendo. Convendría directamente cambiar process stage.
        * Devuelve True si salió bien, False si hubo un error y no puedo actualizar.
        """

        r = True

        # Si se puentea la etapa (la etapa esta apagada), directamente devuelve la señal de entrada
        if is_on is False:
            self.signal_in = signal_in
            self.signal_out = signal_in
            self.is_on = is_on
            self.is_plot = is_plot
            self.get_fft()


        else:
            # Si sale bien la de salida, actualiza
            if self.process_stage(copy(signal_in)):
                self.signal_in = signal_in
                self.is_on = is_on
                self.is_plot = is_plot
                self.get_fft()

            # Si no, no actualiza y avisa que hubo error
            else:
                self.error()
                r = False

        return r

    def get_signal_out(self):
        """
        get_signal_out: Getter para la señal de salida de la etapa
        """
        return self.signal_out

    def plot_stage_time(self, ax):
        """
        plot_stage_time: Grafica la salida de la etapa en el tiempo
        Recibe el axis del front para graficar sobre él
        """
        if self.is_plot is True:
            if(self.stage_id == 2):
                ax.plot(self.signal_out[0], self.signal_out[1], color="red", marker="o", label="Puntos Muestreados")  # Puntos muestreados
            else:
                ax.plot(self.signal_out[0], self.signal_out[1], label=StageType[self.stage_id], color=StageColors[self.stage_id])
        return

    def plot_stage_freq(self, ax):
        """
        plot_stage_freq: Grafica la salida de la etapa en la frecuencia
        Recibe el axis del front para graficar sobre él
        """
        if self.is_plot is True:
            ax.plot(self.signal_out_f[0], self.signal_out_f[1], label=StageType[self.stage_id], color=StageColors[self.stage_id])
        return

    def get_fft(self):
        """
        get_fft: método privado calcula la FFT de la señal de salida para poder graficarla en frecuencia
        Obtiene los parámetros Tt y fs a partir de la señal de entrada
        Calcula el arreglo de frecuencias y magnitud y las guarda
        """

        if self.signal_in is None or self.signal_out is None:
            print("Advertencia: La señal de entrada o salida no está definida.")
            return

        if len(self.signal_in[0]) == 0 or len(self.signal_out[1]) == 0:
            print("Advertencia: La señal de entrada o salida está vacía.")
            return

        # Tiempo total de muestreo
        Tt = self.signal_in[0][-1] - self.signal_in[0][0]

        # Número de muestras en la señal de salida
        N = len(self.signal_out[1])

        # Frecuencia de muestreo
        fs = N / Tt  # Corrección en el cálculo de `fs`

        # Calculamos la FFT
        yf = fft(self.signal_out[1])

        # Arreglo de frecuencias (solo positivas)
        xf = fftfreq(N, 1 / fs)

        # Magnitud de la FFT normalizada
        mag = 2.0 / N * np.abs(yf[:len(xf)])

        # Guardamos los valores en el objeto
        self.signal_out_f = [xf, mag]

        return

########################################################################################################################
