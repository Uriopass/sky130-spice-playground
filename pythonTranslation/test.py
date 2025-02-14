import numpy as np
from rasterio.crs import defaultdict

np.random.seed(0)

cellnames = ['A', 'B', 'C', 'D', 'E']
pin_combinations = [["r", "f"], ["r", "f"], ["r1", "1r", "f1", "1f"], ["r1", "1r", "f1", "1f"], ["r", "f"]]

all_cell_pin_states = [(cell, pin_state) for cell in cellnames for pin_state in pin_combinations[cellnames.index(cell)]]

nb_fets = np.random.randint(1, 20, size=len(cellnames))

W = [[np.random.random() for _ in range(nb_fet)] for nb_fet in nb_fets]

DTSlewM = {
    (cell, pin_state): np.random.random((2, nb_fets[cellnames.index(cell)] + 3))
    for (cell, pin_state) in all_cell_pin_states
}
CapaM = {
    (cell, pin_state): np.random.random((1, nb_fets[cellnames.index(cell)] + 1))
    for (cell, pin_state) in all_cell_pin_states
}

DTSlewSeqIN = {
    ('A', 'r'): np.random.random((2, 2)),
    ('A', 'f'): np.random.random((2, 2)),
}

CapaSeqOUT = 0.5

G = {
    ('A', 'r'): [('B', 'r'), ('C', '1r')],
    ('A', 'f'): [('B', 'f'), ('C', '1f')],
    ('B', 'r'): [('C', 'f1'), ('D', 'f1')],
    ('B', 'f'): [('C', 'r1'), ('D', 'r1')],
    ('C', 'r1'): [('D', '1r')],
    ('C', '1r'): [('D', '1r')],
    ('C', 'f1'): [('D', '1f')],
    ('C', '1f'): [('D', '1f')],
    ('D', 'r1'): [('E', 'r')],
    ('D', '1r'): [('E', 'r')],
    ('D', 'f1'): [('E', 'f')],
    ('D', '1f'): [('E', 'f')]
}

G_rev = defaultdict(list)

for parent, children in G.items():
    for child in children:
        G_rev[child].append(parent)

def softmax(arr):
    return np.log(np.sum(np.exp(arr)))

def softmax_grad(arr):
    arr_exp = np.exp(arr)
    s = np.sum(arr_exp)
    return arr_exp / s

def forward():
    t = {    }
    slew = {    }
    capa_out = {
        x: 0.0 for x in all_cell_pin_states
    }

    capa_in = {
        x: 0.0 for x in all_cell_pin_states
    }

    for node in all_cell_pin_states:
        model = CapaM[node]
        cellname = node[0]
        W_cell = W[cellnames.index(cellname)]
        capa_in[node] = (model @ np.append(W_cell, 1.0))[0]

    for node, children in G.items():
        capa_out[node] = sum([capa_in[child] for child in children])

    t[('A', 'r')], slew[('A', 'r')] = DTSlewSeqIN[('A', 'r')] @ np.array([1.0, capa_out[('A', 'r')]])
    t[('A', 'f')], slew[('A', 'f')] = DTSlewSeqIN[('A', 'f')] @ np.array([1.0, capa_out[('A', 'f')]])


    def calc_dt_slew(parent, child, W):
        return t[parent] + DTSlewM[child] @ np.array(np.append(W, [1.0, capa_out[child], slew[parent]]))

    def dt_slew_real_formula(child):
        W_child = W[cellnames.index(child[0])]
        TS_child = [
            calc_dt_slew(p, child, W_child) for p in G_rev[child]
        ]

        T_child = [TS[0] for TS in TS_child]
        S_child = [TS[1] for TS in TS_child]

        return softmax(T_child), softmax_grad(T_child) @ S_child


    WB = W[cellnames.index('B')]
    t[('B', 'r')], slew[('B', 'r')] = calc_dt_slew(('A', 'r'), ('B', 'r'), WB)
    t[('B', 'f')], slew[('B', 'f')] = calc_dt_slew(('A', 'f'), ('B', 'f'), WB)



    WC = W[cellnames.index('C')]
    t[('C', 'r1')], slew[('C', 'r1')] = calc_dt_slew(('B', 'f'), ('C', 'r1'), WC)
    t[('C', '1r')], slew[('C', '1r')] = calc_dt_slew(('A', 'r'), ('C', '1r'), WC)
    t[('C', 'f1')], slew[('C', 'f1')] = calc_dt_slew(('B', 'r'), ('C', 'f1'), WC)
    t[('C', '1f')], slew[('C', '1f')] = calc_dt_slew(('A', 'f'), ('C', '1f'), WC)



    WD = W[cellnames.index('D')]
    t[('D', 'r1')], slew[('D', 'r1')] = calc_dt_slew(('B', 'f'), ('D', 'r1'), WD)
    t[('D', 'f1')], slew[('D', 'f1')] = calc_dt_slew(('B', 'r'), ('D', 'f1'), WD)

    TS_d1r = (calc_dt_slew(('C', '1r'), ('D', '1r'), WD),
              calc_dt_slew(('C', 'r1'), ('D', '1r'), WD))

    T_d1r = (TS_d1r[0][0], TS_d1r[1][0])
    S_d1r = (TS_d1r[0][1], TS_d1r[1][1])

    t[('D', '1r')] = softmax(T_d1r)
    slew[('D', '1r')] = softmax_grad(T_d1r) @ S_d1r

    TS_d1f = (calc_dt_slew(('C', '1f'), ('D', '1f'), WD),
              calc_dt_slew(('C', 'f1'), ('D', '1f'), WD))

    T_d1f = (TS_d1f[0][0], TS_d1f[1][0])
    S_d1f = (TS_d1f[0][1], TS_d1f[1][1])

    t[('D', '1f')] = softmax(T_d1f)
    slew[('D', '1f')] = softmax_grad(T_d1f) @ S_d1f



    WE = W[cellnames.index('E')]

    TS_er = (calc_dt_slew(('D', 'r1'), ('E', 'r'), WE),
             calc_dt_slew(('D', '1r'), ('E', 'r'), WE))

    T_er = (TS_er[0][0], TS_er[1][0])
    S_er = (TS_er[0][1], TS_er[1][1])

    t[('E', 'r')] = softmax(T_er)
    slew[('E', 'r')] = softmax_grad(T_er) @ S_er

    TS_ef = (calc_dt_slew(('D', 'f1'), ('E', 'f'), WE),
             calc_dt_slew(('D', '1f'), ('E', 'f'), WE))

    T_ef = (TS_ef[0][0], TS_ef[1][0])
    S_ef = (TS_ef[0][1], TS_ef[1][1])

    t[('E', 'f')] = softmax(T_ef)
    slew[('E', 'f')] = softmax_grad(T_ef) @ S_ef

    for node in all_cell_pin_states:
        if node[0] == 'A':
            continue
        t_check, slew_check = dt_slew_real_formula(node)
        assert np.allclose(t[node], t_check)
        assert np.allclose(slew[node], slew_check)

    return t, slew, capa_out

import pprint
pprint.pprint(forward())
