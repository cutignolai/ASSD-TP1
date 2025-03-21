########################################################################################################################
# Archivo para testear el funcionamiento de la clase FAA con espectro de frecuencia
########################################################################################################################
from backend.FAA import FAA
from backend.Stage import StageIDs
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Crear instancia del filtro
########################################################################################################################
# Archivo para testear el funcionamiento de la clase FAA con espectro de frecuencia
########################################################################################################################
from backend.FAA import FAA
from backend.Stage import StageIDs
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Crear instancia del filtro
S1 = FAA(StageIDs.FAA)

# Parámetros de la señal
fs = 1E6  # Frecuencia de muestreo (1 MHz)
t_in = np.linspace(0, 0.001, int(fs * 0.001), endpoint=False)  # 1 ms de señal sin incluir el último punto
x_in = 5 * np.sin(2 * np.pi * 1E3 * t_in) + 2 * np.sin(2 * np.pi * 50E3 * t_in)  # Seno de 1 kHz, 5V de amplitud
signal_in = np.array([t_in, x_in])

# Función para calcular la FFT con normalización
def calcular_fft(signal, t):
    Tt = t[-1] - t[0]  # Tiempo total de muestreo
    N = len(signal)  # Número de muestras
    fs = N / Tt  # Frecuencia de muestreo calculada
    yf = fft(signal)  # Transformada de Fourier
    xf = fftfreq(N, 1 / fs)  # Frecuencias incluyendo negativas
    mag = 2.0 / N * np.abs(yf)  # Magnitud normalizada
    return xf, mag

# Procesar la señal
if S1.update(signal_in, True, True):
    # Crear figura y ejes
    fig, ax = plt.subplots(2, 2, figsize=(12, 6))

    # Gráfico de tiempo - Entrada
    ax1, ax2 = ax[0]
    ax1.set_title("Señal en el dominio del tiempo (Entrada)")
    ax1.set_xlabel("Tiempo [s]")
    ax1.set_ylabel("Amplitud [V]")
    ax1.plot(t_in, x_in, label="Entrada", color="orange", linewidth=1)
    ax1.legend()
    ax1.grid()

    # Gráfico de tiempo - Salida
    ax2.set_title("Señal en el dominio del tiempo (Salida)")
    ax2.set_xlabel("Tiempo [s]")
    ax2.set_ylabel("Amplitud [V]")
    S1.plot_stage_time(ax2)  # Usa la función heredada
    ax2.grid()

    # Gráfico de espectro - Entrada
    ax3, ax4 = ax[1]
    f_in, X_in = calcular_fft(x_in, t_in)
    ax3.set_title("Espectro de Frecuencia (Entrada)")
    ax3.set_xlabel("Frecuencia [Hz]")
    ax3.set_ylabel("Amplitud")
    ax3.stem(f_in, X_in, linefmt="b-", markerfmt="bo", basefmt=" ")  # Cambio a stem plot
    ax3.set_xlim(-5E3, 5E3)  # Limita la vista a ±5 kHz
    ax3.grid()

    # Gráfico de espectro - Salida (ya lo hace Stage)
    ax4.set_title("Espectro de Frecuencia (Salida)")
    ax4.set_xlabel("Frecuencia [Hz]")
    ax4.set_ylabel("Amplitud")
    S1.plot_stage_freq(ax4)  # Usa la función heredada
    ax4.grid()

    # Ajuste y muestra del gráfico
    plt.tight_layout()
    plt.show()
else:
    print("Error en el procesamiento de la señal")