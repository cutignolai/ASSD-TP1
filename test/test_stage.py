########################################################################################################################
# Archivo para testear la clase Stage y sus métodos
########################################################################################################################

from backend.Stage import Stage, StageIDs
import numpy as np
import matplotlib.pyplot as plt

def test_sin(f_0):
    """
    Función de test para la clase Stage y sus métodos.
    Verifica la actualización y procesamiento de señales, además de graficar los resultados.
    """
    # Crear la etapa de prueba (Filtro Anti Aliasing - FAA)
    S1 = Stage(StageIDs.FAA)

    # Crear la señal de entrada: una onda seno de 1 kHz
    t_in = np.linspace(0, 0.1, 1000)
    x_in = 5 * np.sin(2 * np.pi * 1000 * t_in)
    signal_in = [t_in, x_in]

    # Actualizar la etapa con la señal de entrada
    updated = S1.update(signal_in, is_on=True, is_plot=True)

    # Verificar que la actualización fue exitosa
    assert updated, "ERROR: No se pudo actualizar la etapa correctamente."

    # Obtener la señal de salida procesada
    signal_out = S1.get_signal_out()

    # Verificar que la señal de salida no esté vacía
    assert signal_out is not None and len(signal_out[1]) > 0, "ERROR: La señal de salida está vacía."

    # Verificar que la frecuencia de muestreo calculada sea positiva
    Tt = signal_in[0][-1] - signal_in[0][0]
    fs = len(signal_in[0]) / Tt
    assert fs > 0, f"ERROR: La frecuencia de muestreo es incorrecta: {fs}"

    # Crear la figura para los gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    # Usar las funciones de ploteo de la clase Stage para graficar las señales
    S1.plot_stage_time(ax[0])  # Ploteo de la señal en el dominio del tiempo
    S1.plot_stage_freq(ax[1])  # Ploteo de la señal en el dominio de la frecuencia

    # Configuración de los ejes
    ax[0].set_title("Tiempo")
    ax[0].set_xlabel("t [s]")
    ax[0].set_ylabel("x")
    ax[0].grid(True)

    ax[1].set_title("Frecuencia")
    ax[1].set_xlabel("f [Hz]")
    ax[1].set_ylabel("Magnitud")
    ax[1].grid(True)

    # Ajustar el layout y mostrar el gráfico
    plt.tight_layout()
    plt.show()

    # Validación de la FFT
    signal_out_f = S1.signal_out_f
    assert signal_out_f is not None, "ERROR: La señal en frecuencia no se calculó correctamente."

    # Verificar que la magnitud de la FFT sea mayor que 0 en algunas frecuencias
    assert np.any(signal_out_f[1] > 0), "ERROR: La FFT no tiene componentes de frecuencia."

    print("Test de la etapa 'FAA' completado exitosamente.")

def test_ut():
    """
    Test para graficar la función escalón de Heaviside f(t) = u(t).
    Verifica la correcta visualización de la función y la implementación de los ploteos.
    """

    # Crear la etapa de prueba (puede ser cualquier etapa, en este caso no importa)
    stage = Stage(StageIDs.FAA)

    # Generar la señal de entrada: función escalón de Heaviside u(t)
    t = np.linspace(-0.1, 0.1, 1000)  # Rango de tiempo
    u_t = np.heaviside(t, 1)  # Función escalón: 1 para t >= 0, 0 para t < 0
    signal_in = [t, u_t]

    # Actualizar la etapa con la señal de entrada (no se realiza procesamiento aquí)
    updated = stage.update(signal_in, is_on=True, is_plot=True)

    # Verificar que la actualización fue exitosa
    assert updated, "ERROR: No se pudo actualizar la etapa correctamente."

    # Obtener la señal de salida procesada
    signal_out = stage.get_signal_out()

    # Verificar que la señal de salida no esté vacía
    assert signal_out is not None and len(signal_out[1]) > 0, "ERROR: La señal de salida está vacía."


    # Crear la figura para los gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    # Usar las funciones de ploteo de la clase Stage para graficar las señales
    stage.plot_stage_time(ax[0])  # Ploteo de la señal en el dominio del tiempo
    stage.plot_stage_freq(ax[1])  # Ploteo de la señal en el dominio de la frecuencia

    # Configuración de los ejes
    ax[0].set_title(r"$f(t) = u(t)$ (Dominio del Tiempo)")
    ax[0].set_xlabel("t [s]")
    ax[0].set_ylabel("f(t)")
    ax[0].grid(True)

    ax[1].set_title("Frecuencia")
    ax[1].set_xlabel("f [Hz]")
    ax[1].set_ylabel("Magnitud")
    ax[1].grid(True)

    # Ajustar el layout y mostrar el gráfico
    plt.tight_layout()
    plt.show()

    # Validación de la FFT
    signal_out_f = stage.signal_out_f
    assert signal_out_f is not None, "ERROR: La señal en frecuencia no se calculó correctamente."

    # Verificar que la magnitud de la FFT sea mayor que 0 en algunas frecuencias
    assert np.any(signal_out_f[1] > 0), "ERROR: La FFT no tiene componentes de frecuencia."

    print("Test de la función escalón f(t) = u(t) completado exitosamente.")

def test_sin_with_ut(f_0):
    """
    Test para graficar la función f(t) = sin(ω₀ t * u(t)).
    Verifica la correcta visualización de la función y el procesamiento de la señal.
    """
    # Crear la etapa de prueba (puede ser cualquier etapa, en este caso no importa)
    stage = Stage(StageIDs.FAA)

    # Generar el tiempo t
    t = np.linspace(-0.1, 0.1, 1000)

    # Generar la señal: sin(ω₀ * t * u(t)) = sin(ω₀ * t) para t >= 0, 0 para t < 0
    sine_signal = np.sin(2 * np.pi * 1000 * t) * np.heaviside(t, 1)  # Se multiplica por u(t) para hacer la función escalón

    # Preparar la señal de entrada
    signal_in = [t, sine_signal]

    # Actualizar la etapa con la señal de entrada
    updated = stage.update(signal_in, is_on=True, is_plot=True)

    # Verificar que la actualización fue exitosa
    assert updated, "ERROR: No se pudo actualizar la etapa correctamente."

    # Obtener la señal de salida procesada
    signal_out = stage.get_signal_out()

    # Verificar que la señal de salida no esté vacía
    assert signal_out is not None and len(signal_out[1]) > 0, "ERROR: La señal de salida está vacía."


    # Crear la figura para los gráficos
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    # Usar las funciones de ploteo de la clase Stage para graficar las señales
    stage.plot_stage_time(ax[0])  # Ploteo de la señal en el dominio del tiempo
    stage.plot_stage_freq(ax[1])  # Ploteo de la señal en el dominio de la frecuencia

    # Configuración de los ejes
    ax[0].set_title(r"$f(t) = \sin(\omega_0 t \cdot u(t))$")
    ax[0].set_xlabel("t [s]")
    ax[0].set_ylabel("f(t)")
    ax[0].grid(True)

    ax[1].set_title("Frecuencia")
    ax[1].set_xlabel("f [Hz]")
    ax[1].set_ylabel("Magnitud")
    ax[1].grid(True)

    # Ajustar el layout y mostrar el gráfico
    plt.tight_layout()
    plt.show()

    # Validación de la FFT
    signal_out_f = stage.signal_out_f
    assert signal_out_f is not None, "ERROR: La señal en frecuencia no se calculó correctamente."

    # Verificar que la magnitud de la FFT sea mayor que 0 en algunas frecuencias
    assert np.any(signal_out_f[1] > 0), "ERROR: La FFT no tiene componentes de frecuencia."

    print(f"Test de la función f(t) = sin(ω₀ t * u(t)) con ω₀ = {f_0} completado exitosamente.")

# Ejecutar el test
#test_sin_with_ut(f_0=1000)
#test_ut()
test_sin(f_0=1000)



