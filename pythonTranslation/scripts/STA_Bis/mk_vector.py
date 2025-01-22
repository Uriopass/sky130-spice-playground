import numpy as np
from numba.pycc import CC

cc = CC('mk_vector')

@cc.export('mk_vector', 'f8[:](f8[:], f8, f8)')
def mk_vector(w, capa, slew):
    numb_fets = len(w)
    input_tensor = np.zeros(3 + numb_fets * 5 + numb_fets * (numb_fets - 1) * 2, dtype=np.float64)

    input_tensor[0] = 1.0
    input_tensor[1] = slew
    input_tensor[2] = capa

    for j in range(numb_fets):
        w_j = w[j]
        input_tensor[3 + j * 5    ] = 1.0 / w_j
        input_tensor[3 + j * 5 + 1] = capa / w_j
        input_tensor[3 + j * 5 + 2] = np.cbrt(capa / w_j)
        input_tensor[3 + j * 5 + 3] = np.sqrt(slew / w_j)
        input_tensor[3 + j * 5 + 4] = np.cbrt(slew * capa / w_j)

    for j in range(numb_fets):
        w_j = w[j]
        off = 3 + numb_fets * 5 + j * (numb_fets - 1) * 2
        for k in range(numb_fets):
            if j == k:
                continue
            w_k = w[k]
            input_tensor[off + (k - (1 if k > j else 0)) * 2    ] = w_j / w_k
            input_tensor[off + (k - (1 if k > j else 0)) * 2 + 1] = capa / (w_j + w_k)
    return input_tensor

if __name__ == "__main__":
    cc.compile()