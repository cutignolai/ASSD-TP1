########################################################################################################################
# Archivo para testear el funcionamiento de la clase Sample&Hold
########################################################################################################################
from backend.Signal import SignalGen
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

S1 = SignalGen()
t_in = np.linspace(0, 1, 1000)
x_in = 5 * np.sin(2 * np.pi * 1E3 * t_in)
signal_in = [copy(t_in), copy(x_in)]
S1.update(None, True, True, signal_type="Coseno", A=5, freq=1E3, phase=0)
f1, ax = plt.subplots(2)
ax1, ax2 = ax
ax1.set_title("Tiempo")
ax1.set_xlabel("t")
ax1.set_ylabel("x")
S1.plot_stage_time(ax1)
ax1.legend()
ax1.grid()
ax2.set_title("Frecuencia")
ax2.set_xlabel("f")
ax2.set_ylabel("x")
S1.plot_stage_freq(ax2)
ax2.grid()
plt.tight_layout()
plt.show()

