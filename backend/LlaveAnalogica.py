from backend.Stage import Stage, StageIDs


# LLAVE ANALÓGICA
#   Hace la multiplicación de la señal x(t) con una cuadrada de período T y duty cycle DC.
#   t: arreglo con valores en tiempo
#   y: arreglo con valores de la función evaluada en el tiempo t.

class LlaveAnalogica(Stage):

    CHECK_ON = True
    CHECK_OF = False

    def __init__(self):
        super().__init__(StageIDs.LA)
        self.FS = 0
        self.DC = 0

    def update(self, signal_in, is_on, is_plot, signal_type=None, A=None, freq=None, phase=None, fs=None, DC=None):

        r = True

        # Si se puentea la etapa, directamente devuelve la señal de entrada
        if is_on is False:
            self.signal_in = signal_in
            self.signal_out = signal_in
            self.is_on = is_on
            self.is_plot = is_plot

        else:
            self.FS = fs
            self.DC = DC  # la vuelve a procesar para obtener la salida\

            # Si sale bien la de salida, actualiza
            if self.process_stage(signal_in):
                self.signal_in = signal_in
                self.is_on = is_on
                self.is_plot = is_plot
                self.get_fft()

            # Si no, no actualiza y avisa que hubo error
            else:
                self.error()
                r = False

    def process_stage(self, signal_in):
        """
        Procesa la señal de entrada aplicando la llave analógica (muestreo y ciclo de trabajo).

        Parámetros:
        - signal_in: Señal de entrada (lista con tiempo y amplitud).

        Devuelve:
        - True si el proceso fue exitoso, False si hubo algún error.
        """

        t = signal_in[0]    # Tiempo
        amp = signal_in[1]  # Amplitud de la señal

        self.signal_out = signal_in

        T = (1 / self.FS)  # Calcula el período de la señal a partir de la frecuencia de muestreo

        k = 0

        # Si la llave está activada (CHECK_ON)
        if (self.is_on == self.CHECK_ON):

            Teff = T * (self.DC / 100)  # Calcula el tiempo efectivo de la señal cuadrada (basado en el ciclo de trabajo)

            j = 0

            while(t[j] < t[-1]):  # Mientras no se haya alcanzado el último valor de tiempo

                for i in range(k, len(t)):  # Itera sobre los puntos de tiempo a partir de k

                    actual_time = t[i]  # Tiempo actual de la señal
                    max_signal_time = T + (j * T)  # Tiempo máximo de la señal (fin de un ciclo)

                    positive_top_time = Teff + (j * T)  # Tiempo hasta el cual la señal cuadrada es positiva

                    # Si el tiempo actual está dentro del intervalo positivo de la señal cuadrada
                    if actual_time < positive_top_time:
                        self.signal_out[1][i] = amp[i]  # Mantiene el valor de la amplitud de la señal de entrada

                    # Si el tiempo está en el intervalo negativo de la señal cuadrada (cuando la señal debería estar en cero)
                    elif (positive_top_time <= actual_time < max_signal_time):
                        self.signal_out[1][i] = 0  # Pone la señal de salida en cero (muestreo negativo)

                    else:
                        # Si se sale del intervalo del ciclo cuadrado, se actualiza el índice k para continuar con la siguiente iteración
                        k = i + 1
                        break

                j = j + 1  # Avanza al siguiente ciclo
        else:
            # Si la llave está apagada, la señal de salida es igual a la de entrada
            self.signal_out = signal_in

        return True