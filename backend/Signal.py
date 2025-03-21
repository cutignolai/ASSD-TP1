from backend.Stage import Stage, StageIDs
import numpy as np


class SignalGen(Stage):
    def __init__(self):
        super().__init__(StageIDs.IN)
        self.amplitud = None
        self.frecuencia = None
        self.defasaje = None
        self.tipo = None
        self.signal_in = None
        self.signal_out = None

    def __process_stage(self):
        if self.frecuencia is None or self.amplitud is None:
            return False  # No procesar si faltan parámetros esenciales

        # Parámetros generales de la señal
        puntos_por_periodo = 100
        T = 1 / self.frecuencia  # Periodo
        cantidad_periodos = 10
        x_in = np.linspace(0, cantidad_periodos * T, puntos_por_periodo * cantidad_periodos)

        # Selección del tipo de señal
        if self.tipo == "Coseno":
            y_in = self.amplitud * np.cos(2 * np.pi * self.frecuencia * x_in - np.deg2rad(self.defasaje))

        elif self.tipo == "Seno":
            y_in = self.amplitud * np.sin(2 * np.pi * self.frecuencia * x_in - np.deg2rad(self.defasaje))



        elif self.tipo == "SenoXB":

            # Definimos correctamente la cantidad de puntos

            puntos_seno = puntos_por_periodo * 3 // 2  # 1.5T de duración

            x2 = np.linspace(0, 1.5 * T, puntos_seno, endpoint=False)  # `endpoint=False` evita un punto extra

            seno_periodoymedio = self.amplitud * np.sin(2 * np.pi * self.frecuencia * x2)

            repeticiones = int(np.ceil(cantidad_periodos / 1.5))  # Asegurar repeticiones suficientes

            y_in = np.tile(seno_periodoymedio, repeticiones)

            # Recortamos `y_in` para que tenga la misma longitud que `x_in`

            y_in = y_in[:len(x_in)]



        elif self.tipo == "ExpoXB":
            # La señal es una exponencial con un periodo de 2T
            x2 = np.linspace(-T, T, puntos_por_periodo * 2)
            y_aux = np.exp(-5 * self.frecuencia * np.abs(x2))  # Exponencial decreciente
            y_in = np.tile(self.amplitud * y_aux, cantidad_periodos // 2)  # Repetimos cada 2T

        else:
            # Señal combinada con tres frecuencias
            y_in = self.amplitud * (
                    0.5 * np.cos(2 * 1.8 * np.pi * self.frecuencia * x_in) +
                    np.cos(2 * np.pi * 2 * self.frecuencia * x_in) +
                    0.5 * np.cos(2 * np.pi * 2.2 * self.frecuencia * x_in)
            )

        # Actualización de la señal de salida
        self.signal_out = np.array([x_in, y_in])
        self.signal_in = self.signal_out
        return True

    def update(self, signal_in, is_on, is_plot, signal_type=None, A=None, freq=None, phase=None, fs=None, DC=None):
        # Verifica si hubo cambios en los parámetros
        if (signal_type != self.tipo or A != self.amplitud or freq != self.frecuencia or phase != self.defasaje):
            # Actualiza los valores
            self.tipo = signal_type
            self.amplitud = A
            self.frecuencia = freq
            self.defasaje = phase

            if self.__process_stage():  # Si la señal se generó correctamente
                self.is_on = is_on
                self.is_plot = is_plot
                self.get_fft()
                return True
            else:
                self.error()
                return False

        # Si no hay cambios en la señal, solo actualiza el estado de ploteo
        if not is_plot:
            self.is_plot = False
        return True
