from backend.Stage import Stage, StageIDs
from copy import copy

class SampleAndHold(Stage):
    def __init__(self):
        super().__init__(StageIDs.SH)
        self.fs = 0

    def update(self, signal_in, is_on, is_plot, signal_type=None, A=None, freq=None, phase=None, fs=None, DC=None):
        r = True

        # Si se puentea la etapa, directamente devuelve la señal de entrada
        if is_on is False:
            self.signal_in = signal_in
            self.signal_out = signal_in
            self.is_on = is_on
            self.is_plot = is_plot

        else:
            self.fs = fs                                      # La vuelve a procesar para obtener la salida

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

    def process_stage(self, signal_in):

        if self.fs is None or self.fs == 0:
            return False

        k = 0
        signal_out = signal_in

        """
        t_entrada = signal_in[0]
        amp_entrada = signal_in[1]
        
        t_out = signal_out[0]
        amp_out = signal_out[1]
        
        """

        for j in range(int((signal_in[0][-1] - signal_in[0][0]) * self.fs) + 2):    # Define la cantidad de muestras

            for i in range(k, len(signal_in[0])):                                   # Recorre el arreglo
                if signal_in[0][i] >= j/self.fs:                                    # Si es mayor al armónico,
                    signal_out[1][i] = signal_in[1][i]                              # Muestrea el valor
                    k = i + 1
                    break
                else:                                                               # Si es menor,
                    signal_out[1][i] = signal_out[1][i-1]                           # Copia el valor anterior

        self.signal_out = signal_out
        return True
