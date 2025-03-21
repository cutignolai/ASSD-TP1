from backend.Stage import Stage
import scipy.signal as ss
import numpy as np

def get_sallenkey_tf(R1, R2, C1, C2):
    return ss.TransferFunction([1/(R1 * R2 * C1 * C2)], [1, 1/(R2 * C1) + 1/(R1 * C1), 1/(R1 * R2 * C1 * C2)])

class FAA(Stage):
    def __init__(self, stage_id):
        super().__init__(stage_id)

    def process_stage(self, signal_in):
        print("ENTREE")
        # Filtro pasabajos obtenido a partir de la filter tool de TC, aproximando con Legendre
        '''
        filter1 = ss.lti([1], [1, 30952.2, 244104263.46])
        filter2 = ss.lti([1], [1, 23632.2, 185763709.62])
        filter3 = ss.lti([1], [1, 13585.8, 185763709.62])
        filter4 = ss.lti([1], [1, 4287, 244104263.46])
        filter1 = ss.lti([], [-5.163 + 2.469E4j, -5.163 - 2.469E4j], 1)
        filter2 = ss.lti([], [-3.675 + 6.981E4j, -3.675 + 6.981E4j], 1)
        filter3 = ss.lti([], [-1.345 + 9.682E4j, -1.345 + 9.682E4j], 1)
        filter4 = ss.lti([], [], 1E-8)'''

        filter1 = get_sallenkey_tf(16E3, 6.8E3, 1E-9, 668E-12)
        filter2 = get_sallenkey_tf(43E3, 12E3, 1E-9, 150E-12)
        filter3 = get_sallenkey_tf(12E3, 4.3E3, 10E-9, 150E-12)
        filter4 = get_sallenkey_tf(12E3, 12E3, 1E-9, 1E-9)

        # Ahora hago pasar la señal de entrada por las diferentes etapas del filtro
        x, y, z = ss.lsim(filter1, signal_in[1], signal_in[0])   # Funcion output(tensión , tiempo)
        x, y, z = ss.lsim(filter2, y, x)
        x, y, z = ss.lsim(filter3, y, x)
        x, y, z = ss.lsim(filter4, y, x)

        self.signal_out = np.array([x, y])

        return True


