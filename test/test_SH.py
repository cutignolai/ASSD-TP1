####################################################################################################
# Test de la clase SampleAndHold con diferentes frecuencias de muestreo
####################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from copy import copy
from backend.SampleAndHold import SampleAndHold

def test_sample_and_hold(fs):
    """
    Función para probar el Sample & Hold con una frecuencia de muestreo específica.

    Parámetros:
    - fs: Frecuencia de muestreo en Hz.
    """

    # Parámetros de la señal
    frecuencia_senal = 100  # Frecuencia de la señal en Hz
    amplitud = 5  # Amplitud de la señal

    # Generación de la señal de entrada
    t_in = np.linspace(0, 0.1, 1000)  # Vector de tiempo (0 a 0.1 seg)
    x_in = amplitud * np.sin(2 * np.pi * frecuencia_senal * t_in)  # Señal senoidal
    signal_in = [copy(t_in), copy(x_in)]

    print(f"Probando con fs = {fs} Hz")  # Para verificar que fs se pasa correctamente

    S1 = SampleAndHold()
    S1.update(signal_in, True, True, fs=fs)

    # Configuración de la figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'hspace': 0.4})
    fig.suptitle(f"Sample & Hold con fs = {fs} Hz", fontsize=12, fontweight='bold')

    # Gráfico en el dominio del tiempo
    ax1.set_title("Señal en el tiempo")
    ax1.set_xlabel("Tiempo [s]")
    ax1.set_ylabel("Amplitud")
    ax1.plot(t_in, x_in, label="Señal Original", color="tab:orange")
    S1.plot_stage_time(ax1)
    ax1.plot(S1.signal_out[0], S1.signal_out[1], color="red", marker="o", label="Puntos Muestreados")  # Puntos muestreados
    ax1.legend()
    ax1.grid(True)
    ax1.set_xlim(t_in[0], t_in[-1])

    # Gráfico en el dominio de la frecuencia
    ax2.set_title("Transformada en frecuencia")
    ax2.set_xlabel("Frecuencia [Hz]")
    ax2.set_ylabel("Magnitud")
    S1.plot_stage_freq(ax2)
    ax2.grid(True)

# Llamamos a la función con diferentes frecuencias de muestreo
test_sample_and_hold(500)
test_sample_and_hold(2000)
test_sample_and_hold(10000)

# Mostrar todas las figuras juntas
plt.show()
