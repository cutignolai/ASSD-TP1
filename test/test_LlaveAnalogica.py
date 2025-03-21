########################################################################################################################
# Archivo para testear el funcionamiento de la clase Llave
########################################################################################################################

from backend.LlaveAnalogica import LlaveAnalogica
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

# Crear instancia de la clase LLA (Llave Analógica)
L1 = LlaveAnalogica()

# Definir el arreglo de tiempo y la señal de entrada (senoidal)
t_in = np.linspace(0, 0.1, 1000)  # Tiempo de 0 a 0.1 segundos con 1000 puntos
x_in = 5 * np.sin(2 * np.pi * 1E2 * t_in)  # Señal de entrada: seno a 100 Hz con amplitud 5
signal_in = [copy(t_in), copy(x_in)]  # Crear una copia de la señal para evitar modificar la original

# Actualizar la llave analógica con la señal de entrada
# Parámetros: signal_in (señal de entrada), True (encender la etapa), True (habilitar gráfico),
# fs=1000 (frecuencia de muestreo), DC=50 (ciclo de trabajo al 50%)
L1.update(signal_in, True, True, fs=1000, DC=50)

# Crear la figura con dos subgráficos
f1, ax = plt.subplots(2, 1, figsize=(10, 6))  # Dos gráficos apilados en una columna
ax1, ax2 = ax  # Desempaquetamos las posiciones de los gráficos

# Configuración del primer gráfico: Dominio del Tiempo
ax1.set_title("Señal en el Dominio del Tiempo")
ax1.set_xlabel("Tiempo [s]")
ax1.set_ylabel("Amplitud")
ax1.plot(t_in, x_in, label="Señal de Entrada", color="orange")  # Señal de entrada
L1.plot_stage_time(ax1)  # Graficar la salida procesada
ax1.legend()
ax1.grid(True)  # Activar la cuadrícula

# Configuración del segundo gráfico: Dominio de la Frecuencia
ax2.set_title("Transformada de Frecuencia de la Señal")
ax2.set_xlabel("Frecuencia [Hz]")
ax2.set_ylabel("Amplitud")
L1.plot_stage_freq(ax2)  # Graficar la FFT de la señal procesada
ax2.grid(True)  # Activar la cuadrícula

# Ajustar el diseño de la figura para que no se sobrepongan los gráficos
plt.tight_layout()

# Mostrar los gráficos
plt.show()
