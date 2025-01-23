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
            off2 = (k - (1 if k > j else 0)) * 2
            input_tensor[off + off2    ] = w_j / w_k
            input_tensor[off + off2 + 1] = capa / (w_j + w_k)
    return input_tensor

@cc.export('vector_grad', 'Tuple((f8[:], f8))(f8[:], f8, f8, f8[:])')
def vector_grad(w, capa, slew, dout):
    """returns the derivative of w and capa given the output derivative"""

    numb_fets = len(w)
    dw = np.zeros(numb_fets)
    dcapa = 0.0

    for j in range(numb_fets):
        w_j = w[j]
        dw[j] += -dout[3 + j * 5] / w_j ** 2
        dw[j] += -dout[3 + j * 5 + 1] * capa / w_j ** 2
        dw[j] += -dout[3 + j * 5 + 2] * np.cbrt(capa / w_j ** 4) / 3
        dw[j] += -dout[3 + j * 5 + 3] / (2 * np.sqrt(slew / w_j ** 3))
        dw[j] += -dout[3 + j * 5 + 2] * np.cbrt(slew * capa / w_j ** 4) / 3

        dcapa += dout[3 + j * 5 + 1] / w_j

    for j in range(numb_fets):
        w_j = w[j]
        off = 3 + numb_fets * 5 + j * (numb_fets - 1) * 2
        for k in range(numb_fets):
            if j == k:
                continue
            w_k = w[k]
            off2 = (k - (1 if k > j else 0)) * 2
            dw[j] += dout[off + off2] / w_k
            dw[k] -= dout[off + off2] * w_j / w_k ** 2
            dcapa += dout[off + off2 + 1] / (w_j + w_k)

    return dw, dcapa

if __name__ == "__main__":
    cc.compile()