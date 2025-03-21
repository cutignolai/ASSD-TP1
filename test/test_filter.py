import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Definir las características del filtro Sallen-Key
def get_sallenkey_tf(R, C, f0):
    # Frecuencia de corte en radianes por segundo
    w0 = 2 * np.pi * f0
    # Parámetros del filtro
    numerator = [w0**2]
    denominator = [1, np.sqrt(2)*w0, w0**2]
    return numerator, denominator

# Parámetros de los filtros
filtro1_params = get_sallenkey_tf(6800, 1e-9, 16e3)
filtro2_params = get_sallenkey_tf(12000, 150e-12, 43e3)
filtro3_params = get_sallenkey_tf(4300, 150e-12, 12e3)
filtro4_params = get_sallenkey_tf(12000, 1e-9, 12e3)

# Crear un rango de frecuencias para evaluar la respuesta en frecuencia
freeq = np.logspace(1, 5, num=1000)  # De 10 Hz a 100 kHz

# Evaluar la respuesta en frecuencia para cada filtro
w, h1 = signal.freqs(filtro1_params[0], filtro1_params[1], worN=freeq*2*np.pi)
_, h2 = signal.freqs(filtro2_params[0], filtro2_params[1], worN=freeq*2*np.pi)
_, h3 = signal.freqs(filtro3_params[0], filtro3_params[1], worN=freeq*2*np.pi)
_, h4 = signal.freqs(filtro4_params[0], filtro4_params[1], worN=freeq*2*np.pi)

# Ventana 1: Graficar los filtros individuales
plt.figure(figsize=(10, 6))
plt.semilogx(freeq, 20 * np.log10(abs(h1)), label="Filtro 1 - 16 kHz", color='r')
plt.semilogx(freeq, 20 * np.log10(abs(h2)), label="Filtro 2 - 43 kHz", color='b')
plt.semilogx(freeq, 20 * np.log10(abs(h3)), label="Filtro 3 - 12 kHz", color='g')
plt.semilogx(freeq, 20 * np.log10(abs(h4)), label="Filtro 4 - 12 kHz", color='g')

# Etiquetas y título
plt.title("Respuesta en frecuencia de filtros pasabajos")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud [dB]")
plt.grid(True, which='both', ls='--', color='gray')

# Líneas de frecuencia de corte
plt.axvline(x=16000, color='r', linestyle='--', label="16 kHz (Filtro 1)")
plt.axvline(x=43000, color='b', linestyle='--', label="43 kHz (Filtro 2)")
plt.axvline(x=12000, color='g', linestyle='--', label="12 kHz (Filtro 3 y 4)")

# Leyenda
plt.legend(loc="lower left")
plt.show()

# Ventana 2: Graficar el filtro combinado en cascada y calcular su frecuencia de corte
# Combinar las funciones de transferencia de los filtros (multiplicación de los numeradores y denominadores)
combined_num = filtro1_params[0]
combined_den = filtro1_params[1]
combined_num = np.polymul(combined_num, filtro2_params[0])
combined_den = np.polymul(combined_den, filtro2_params[1])
combined_num = np.polymul(combined_num, filtro3_params[0])
combined_den = np.polymul(combined_den, filtro3_params[1])
combined_num = np.polymul(combined_num, filtro4_params[0])
combined_den = np.polymul(combined_den, filtro4_params[1])

# Calcular la respuesta en frecuencia del filtro combinado
_, h_combined = signal.freqs(combined_num, combined_den, worN=freeq*2*np.pi)

# Graficar la respuesta del filtro combinado
plt.figure(figsize=(10, 6))
plt.semilogx(freeq, 20 * np.log10(abs(h_combined)), label="Filtro combinado en cascada", color='red')

plt.semilogx(freeq, 20 * np.log10(abs(h1)), label="Filtro 1 - 16 kHz", color='grey')
plt.semilogx(freeq, 20 * np.log10(abs(h2)), label="Filtro 2 - 43 kHz", color='grey')
plt.semilogx(freeq, 20 * np.log10(abs(h3)), label="Filtro 3 - 12 kHz", color='grey')
plt.semilogx(freeq, 20 * np.log10(abs(h4)), label="Filtro 4 - 12 kHz", color='grey')


# Buscar la frecuencia de corte a -3 dB (donde la magnitud es la mitad de la máxima)
magnitude_db = 20 * np.log10(abs(h_combined))
cutoff_freq_idx = np.where(magnitude_db <= -3)[0][0]
cutoff_freq = freeq[cutoff_freq_idx]

# Mostrar la frecuencia de corte en la gráfica
plt.axvline(x=cutoff_freq, color='red', linestyle='-.', label=f"Frecuencia de corte: {cutoff_freq:.2f} Hz")

# Etiquetas y título
plt.title("Respuesta en frecuencia del filtro combinado en cascada")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud [dB]")
plt.grid(True, which='both', ls='--', color='gray')

# Leyenda
plt.legend(loc="lower left")
plt.show()
