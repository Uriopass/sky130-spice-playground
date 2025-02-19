import numpy as np
from collections import defaultdict

np.random.seed(0)

cellnames = ['A', 'B', 'C', 'D', 'E']

seqin_cellnames = ['A']
seqout_cellnames = ['E']

end_nodes = [('E', 'r'), ('E', 'f')]

pin_combinations = [["r", "f"], ["r", "f"], ["r1", "1r", "f1", "1f"], ["r1", "1r", "f1", "1f"], ["r", "f"]]

all_cell_pin_states = [(cell, pin_state) for cell in cellnames for pin_state in pin_combinations[cellnames.index(cell)]]

nb_fets = np.random.randint(1, 20, size=len(cellnames))

W = {cellname: [np.random.random() for _ in range(nb_fets[i])] for i, cellname in enumerate(cellnames)}

for cellname in seqin_cellnames:
    del W[cellname]

for cellname in seqout_cellnames:
    del W[cellname]

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

use_max = 1.0

def softmax(arr):
    global use_max
    arrmax = use_max * np.max(arr)
    return np.log(np.sum(np.exp(arr - arrmax))) + arrmax

def softmax_grad(arr):
    global use_max
    arr_exp = np.exp(arr - use_max * np.max(arr))
    s = np.sum(arr_exp)
    return arr_exp / s

def softmax_grad_grad(arr):
    global use_max
    arr_exp = np.exp(arr - use_max * np.max(arr))
    s = np.sum(arr_exp)
    y = arr_exp / s
    return np.diag(y) - np.outer(y, y)

def forward():
    t = {    }
    slew = {    }
    capa_out = {
        x: 0.0 for x in all_cell_pin_states
    }

    capa_in = {
        x: 0.0 for x in all_cell_pin_states
    }

    T = {}
    S = {}

    for node in all_cell_pin_states:
        if node[0] in seqin_cellnames:
            continue
        if node[0] in seqout_cellnames:
            capa_in[node] = CapaSeqOUT
            continue
        model = CapaM[node]
        cellname = node[0]
        W_cell = W[cellname]
        capa_in[node] = (model @ np.append(W_cell, 1.0))[0].item()
        #print(f"capa_in[{node}] = {capa_in[node]}")

    # bw cursor

    for node, children in G.items():
        capa_out[node] = sum([capa_in[child] for child in children])

    t[('A', 'r')], slew[('A', 'r')] = DTSlewSeqIN[('A', 'r')] @ np.array([1.0, capa_out[('A', 'r')]])
    t[('A', 'f')], slew[('A', 'f')] = DTSlewSeqIN[('A', 'f')] @ np.array([1.0, capa_out[('A', 'f')]])

    def calc_dt_slew_seqin(child):
        return DTSlewSeqIN[child] @ np.array([1.0, capa_out[child]])

    def calc_T_seqout(child):
        T_parents = [t[p] for p in G_rev[child]]
        return softmax(T_parents)

    def calc_dt_slew(p, child, W):
        return [t[p], 0.0] + DTSlewM[child] @ np.array(np.append(W, [1.0, capa_out[child], slew[p]]))

    def dt_slew_real_formula(child):
        W_child = W[child[0]]
        TS_child = [
            calc_dt_slew(p, child, W_child) for p in G_rev[child]
        ]

        T[child] = [TS[0] for TS in TS_child]
        S[child] = [TS[1] for TS in TS_child]

        return softmax(T[child]), softmax_grad(T[child]) @ S[child]


    WB = W['B']
    t[('B', 'r')], slew[('B', 'r')] = calc_dt_slew(('A', 'r'), ('B', 'r'), WB)
    t[('B', 'f')], slew[('B', 'f')] = calc_dt_slew(('A', 'f'), ('B', 'f'), WB)

    WC = W['C']
    t[('C', 'r1')], slew[('C', 'r1')] = calc_dt_slew(('B', 'f'), ('C', 'r1'), WC)
    t[('C', '1r')], slew[('C', '1r')] = calc_dt_slew(('A', 'r'), ('C', '1r'), WC)
    t[('C', 'f1')], slew[('C', 'f1')] = calc_dt_slew(('B', 'r'), ('C', 'f1'), WC)
    t[('C', '1f')], slew[('C', '1f')] = calc_dt_slew(('A', 'f'), ('C', '1f'), WC)

    WD = W['D']
    t[('D', 'r1')], slew[('D', 'r1')] = calc_dt_slew(('B', 'f'), ('D', 'r1'), WD)
    t[('D', 'f1')], slew[('D', 'f1')] = calc_dt_slew(('B', 'r'), ('D', 'f1'), WD)

    TS_d1r = (calc_dt_slew(('C', '1r'), ('D', '1r'), WD),
              calc_dt_slew(('C', 'r1'), ('D', '1r'), WD))

    T[('D', '1r')] = (TS_d1r[0][0], TS_d1r[1][0])
    S[('D', '1r')] = (TS_d1r[0][1], TS_d1r[1][1])

    t[('D', '1r')] = softmax(T[('D', '1r')])
    slew[('D', '1r')] = softmax_grad(T[('D', '1r')]) @ S[('D', '1r')]

    TS_d1f = (calc_dt_slew(('C', '1f'), ('D', '1f'), WD),
              calc_dt_slew(('C', 'f1'), ('D', '1f'), WD))

    T[('D', '1f')] = (TS_d1f[0][0], TS_d1f[1][0])
    S[('D', '1f')] = (TS_d1f[0][1], TS_d1f[1][1])

    t[('D', '1f')] = softmax(T[('D', '1f')])
    slew[('D', '1f')] = softmax_grad(T[('D', '1f')]) @ S[('D', '1f')]

    t[('E', 'r')] = softmax([t[('D', 'r1')], t[('D', '1r')]])
    t[('E', 'f')] = softmax([t[('D', 'f1')], t[('D', '1f')]])

    for node in all_cell_pin_states:
        if node[0] in seqout_cellnames:
            t_check = calc_T_seqout(node)
            assert np.allclose(t[node], t_check)
            continue

        if node[0] in seqin_cellnames:
            t_check, slew_check = calc_dt_slew_seqin(node)
        else:
            t_check, slew_check = dt_slew_real_formula(node)
        assert np.allclose(t[node], t_check)
        assert np.allclose(slew[node], slew_check)

    cost = softmax([t[node] for node in end_nodes])

    return t, T, S, slew, capa_out, cost

def backward(t, T, S, slew, capa_out):
    g_cost = 1

    g_W = {}

    for cellname in W:
        g_W[cellname] = np.zeros_like(W[cellname])

    gt = defaultdict(float)
    gslew = defaultdict(float)

    gcapa_out = defaultdict(float)
    gcapa_in = defaultdict(float)

    def grad_calc_T_seqout(child):
        T_parents = [t[p] for p in G_rev[child]]
        return softmax_grad(T_parents)

    def grad_calc_dt_slew_seqin(child):
        return DTSlewSeqIN[child].T

    def grad_calc_dt_slew(child, gt, gslew):
        #return [t[p], 0.0] + DTSlewM[child] @ np.array(np.append(W, [1.0, capa_out[child], slew[p]]))

        # on voudra g_W et g_tp et g_capa_out et g_slew

        g_tp = gt
        g_V = DTSlewM[child].T @ [gt, gslew]

        g_W = g_V[:-3]
        g_capa_out = g_V[-2]
        g_slew = g_V[-1]

        return g_W, g_tp, g_capa_out, g_slew


    def grad_dt_slew_real_formula(child, gt_out, gslew_out):
        g_T_child_gt = softmax_grad(T[child])
        g_T_child_slew = softmax_grad_grad(T[child]) @ S[child]

        g_T_child = g_T_child_gt * gt_out + g_T_child_slew * gslew_out
        g_S_child = softmax_grad(T[child]).T * gslew_out

        for gt_c, gs_c, p in zip(g_T_child, g_S_child, G_rev[child]):
            g_Wc, gtp, gcapa_out_c, gsp = grad_calc_dt_slew(child, gt_c, gs_c)
            g_W[child[0]] += g_Wc
            gcapa_out[child] += gcapa_out_c
            gt[p] += gtp
            gslew[p] += gsp

    g_end_nodes = softmax_grad([t[node] for node in end_nodes]) * g_cost

    for node in reversed(all_cell_pin_states):
        if node[0] in seqout_cellnames:
            #t_check = calc_T_seqout(node)
            g_t_check = g_end_nodes[end_nodes.index(node)]
            gt_parents = grad_calc_T_seqout(node) * g_t_check
            for cell_i, parent in enumerate(G_rev[node]):
                gt[parent] += gt_parents[cell_i]
            continue

        if node[0] in seqin_cellnames:
            #t_check, slew_check = calc_dt_slew_seqin(node)

            debugg = grad_calc_dt_slew_seqin(node) @ [gt[node], gslew[node]]
            _, gcapa_out[node] = debugg
        else:
            #t_check, slew_check = dt_slew_real_formula(node)

            grad_dt_slew_real_formula(node, gt[node], gslew[node])

    for node, children in G.items():
        for child in children:
            gcapa_in[child] += gcapa_out[node]

    for node in all_cell_pin_states:
        if node[0] in seqout_cellnames:
            continue
        if node[0] in seqin_cellnames:
            continue

        model = CapaM[node]
        cellname = node[0]
        gW_cell = (model.T * gcapa_in[node])[:-1]

        g_W[cellname] += gW_cell.flatten()

    return g_W

import pprint
t, T, S, slew, capa_out, _ = forward()

g_W = backward(t, T, S, slew, capa_out)

# now estimate using finite differences

g_W_fd = {}
import matplotlib.pyplot as plt

eps = 1e-4

for _ in range(1000):
    W = {cellname: [np.random.random() for _ in range(nb_fets[i])] for i, cellname in enumerate(cellnames)}

    for cellname in ['B']:
        g_W_fd[cellname] = np.zeros_like(W[cellname])

        W_old = W[cellname].copy()
        for i in range(len(W[cellname])):
            W[cellname][i] = W_old[i] + eps
            _, _, _, _, _, cost1 = forward()
            W[cellname][i] = W_old[i] - eps
            _, _, _, _, _, cost2 = forward()

            g_W_fd[cellname][i] = (cost1 - cost2) / (2 * eps)

            W[cellname][i] = W_old[i]

        #print("g_W", 2.0 * g_W[cellname])
        #print("g_W_fd", g_W_fd[cellname])
        print(np.mean((g_W_fd[cellname] - 1.7 * g_W[cellname]) / g_W[cellname]))
