import os

import numpy as np

data = {
    i: {} for i in range(24)
}

def transition_new(n, rise, fall):
    data[n]['transition_new'] = (rise, fall)

def pfet(oldw, neww, name, d, g, s):
    n = int(name.split('_')[1][1:])
    if 'fet' not in data[n-1]:
        data[n-1]['fet'] = []

    transistor_n = name.split('_')[0]
    data[n-1]['fet'].append((transistor_n, neww, g))

def nfet(oldw, neww, name, d, g, s):
    n = int(name.split('_')[1][1:])
    if 'fet' not in data[n-1]:
        data[n-1]['fet'] = []

    transistor_n = name.split('_')[0]
    data[n-1]['fet'].append((transistor_n, neww, g))

def capa(n, c):
    if 'capa' in data[n-1]:
        data[n-1]['capa'] += c
    else:
        data[n-1]['capa'] = c

def ground_truth_start(n, old_rise, old_fall, new_rise, new_fall):
    data[n-1]['ground_truth_start'] = (old_rise, old_fall, new_rise, new_fall)

def ground_truth_end(n, old_rise, old_fall, new_rise, new_fall):
    data[n-1]['ground_truth_end'] = (old_rise, old_fall, new_rise, new_fall)

def on_rise(n, rise):
    data[n-1]['on_rise'] = rise

def other_pins(n, pins):
    data[n]['other_pins'] = pins

def cell_name(n, name):
    data[n]['cell_name'] = name

def input_pin(n, name):
    data[n]['input_pin'] = name

# ===  clkbuf ===
cell_name(0, "clkbuf")
other_pins(0, "")
input_pin(0, "A")
transition_new(0, 0.0448, 0.0333)
capa(1, 0.016008)
capa(1, 0.0131965615)
pfet(4 * 1.00, 6 * 1.00, "3_I1",  "Vdd",     "I1/A", "I1/temp0")
nfet(4 * 0.42, 4 * 0.42, "0_I1", "Vgnd",     "I1/A", "I1/temp0")
pfet(4 * 4.00, 4 * 4.00, "1_I1",  "Vdd", "I1/temp0",     "I1/X")
nfet(4 * 1.68, 6 * 1.68, "2_I1", "Vgnd", "I1/temp0",     "I1/X")

ground_truth_start(1, 0.074, 0.438, 0.033, 0.344)
ground_truth_end(1, 0.204, 0.567, 0.152, 0.438)
on_rise(1, "rise")

# ===  buf ===
cell_name(1, "buf")
other_pins(1, "")
input_pin(1, "A")
transition_new(1, 0.0383, 0.0243)
capa(2, 0.029571)
capa(2, 0.02167141)
pfet(4 * 1.00, 4 * 1.00, "1_I2",  "Vdd",     "I2/A", "I2/temp0")
nfet(4 * 0.65, 6 * 0.65, "2_I2", "Vgnd",     "I2/A", "I2/temp0")

pfet(4 * 4.00, 6 * 4.00, "3_I2",  "Vdd", "I2/temp0",     "I2/X")
nfet(4 * 2.60, 4 * 2.60, "0_I2", "Vgnd", "I2/temp0",     "I2/X")

ground_truth_start(2, 0.206, 0.568, 0.153, 0.439)
ground_truth_end(2, 0.303, 0.694, 0.238, 0.593)
on_rise(2, "rise")

# ===  mux2, A0=1, A1=0 ===
cell_name(2, "mux2")
other_pins(2, "A0=1, A1=0")
input_pin(2, "S")
transition_new(2, 0.0396, 0.0413)
capa(3, 0.001558)
capa(3, 0.0044560134)

pfet(0.42, 16 * 0.42, "3_I3" ,      "Vdd",     "I3/S", "I3/temp1")
nfet(0.42, 16 * 0.42, "10_I3" ,     "Vgnd",     "I3/S", "I3/temp1")

pfet(0.42, 8 * 0.42, "2_I3" ,      "Vdd", "I3/temp1", "I3/temp3")
nfet(0.42, 8 * 0.42, "11_I3" ,     "Vgnd", "I3/temp1", "I3/temp0")

pfet(0.42, 8 * 0.42, "4_I3" , "I3/temp3",    "I3/A1", "I3/temp5")
nfet(0.42, 8 * 0.42, "5_I3" , "I3/temp2",    "I3/A1", "I3/temp5")

nfet(0.42, 4 * 0.42, "0_I3" ,     "Vgnd",     "I3/S", "I3/temp2")
pfet(0.42, 4 * 0.42, "9_I3" ,      "Vdd",     "I3/S", "I3/temp4")

pfet(0.42, 8 * 0.42, "6_I3" , "I3/temp4",    "I3/A0", "I3/temp5")
nfet(0.42, 8 * 0.42, "1_I3" , "I3/temp0",    "I3/A0", "I3/temp5")

pfet(1.00, 4 * 1.00, "8_I3",      "Vdd", "I3/temp5",     "I3/X")
nfet(0.65, 4 * 0.65, "7_I3",     "Vgnd", "I3/temp5",     "I3/X")


ground_truth_start(3, 0.305, 0.696, 0.242, 0.597)
ground_truth_end(3, 0.621, 0.924, 0.436, 0.729)
on_rise(3, "rise")

# ===  mux2, S=0, A1=1 ===
cell_name(3, "mux2")
other_pins(3, "S=0, A1=1")
input_pin(3, "A0")
transition_new(3, 0.0367, 0.0456)
capa(4, 0.013917)
capa(4, 0.017433986)

pfet(0.64, 0.64, "3_I4",      "Vdd",     "I4/S", "I4/temp4")
nfet(0.42, 0.42, "10_I4" ,     "Vgnd",     "I4/S", "I4/temp4")

pfet(0.64, 0.36, "2_I4" ,      "Vdd", "I4/temp4", "I4/temp2")
nfet(0.42, 10 * 0.42, "11_I4" ,     "Vgnd", "I4/temp4", "I4/temp1")

pfet(0.64, 0.36, "4_I4" , "I4/temp5",    "I4/A1", "I4/temp2")
nfet(0.42, 0.36, "5_I4", "I4/temp5",    "I4/A1", "I4/temp3")

pfet(0.64, 10 * 0.64, "0_I4" ,      "Vdd",     "I4/S", "I4/temp0")
nfet(0.42, 0.36, "9_I4" ,     "Vgnd",     "I4/S", "I4/temp3")

pfet(0.64, 6 * 0.64, "6_I4" , "I4/temp5",    "I4/A0", "I4/temp0")
nfet(0.42, 8 * 0.42, "1_I4" , "I4/temp5",    "I4/A0", "I4/temp1")

pfet(2.00, 4.0 * 2.00, "8_I4" ,      "Vdd", "I4/temp5",     "I4/X")
nfet(1.30, 2.0 * 1.30, "7_I4" ,     "Vgnd", "I4/temp5",     "I4/X")

ground_truth_start(4, 0.621, 0.925, 0.437, 0.729)
ground_truth_end(4, 0.957, 1.206, 0.582, 0.820)
on_rise(4, "fall")

# ===  xor2, A=0 ===
cell_name(4, "xor2")
other_pins(4, "A=0")
input_pin(4, "B")
transition_new(4, 0.0536, 0.0572)
capa(5, 0.004687)
capa(5, 0.006688504)

pfet(1.00, 10*1.00, "8_I5",     "Vdd",     "I5/A", "I5/temp0")
pfet(1.00,  2*1.00, "3_I5","I5/temp3",     "I5/B", "I5/temp0")

nfet(0.65, 2*0.36, "5_I5",     "Vgnd",     "I5/A", "I5/temp3")
nfet(0.65, 2*0.65, "2_I5",     "Vgnd",     "I5/B", "I5/temp3")

pfet(1.00, 2*1.00, "0_I5", "I5/temp2", "I5/temp3",     "I5/X")
nfet(0.65, 2*0.65, "6_I5",     "Vgnd", "I5/temp3",     "I5/X")

pfet(1.00, 10*1.00, "7_I5",      "Vdd",     "I5/A", "I5/temp2")
pfet(1.00, 3*1.00, "4_I5",      "Vdd",     "I5/B", "I5/temp2")

nfet(0.65, 3*0.65, "1_I5", "I5/temp1",     "I5/B",     "I5/X")
nfet(0.65, 10*0.65, "9_I5",     "Vgnd",     "I5/A", "I5/temp1")


ground_truth_start(5, 0.959, 1.208, 0.584, 0.822)
ground_truth_end(5, 1.165, 1.517, 0.691, 0.968)
on_rise(5, "fall")

# ===  a21o, A1=1, B1=0 ===
cell_name(5, "a21o")
other_pins(5, "A1=1, B1=0")
input_pin(5, "A2")
transition_new(5, 0.0433, 0.1389)
capa(6, 0.007073)
capa(6, 0.008910184)

pfet(1.00, 0.36, "3_I6",      "Vdd",    "I6/A1", "I6/temp0")
pfet(1.00, 3 * 1.00, "6_I6",      "Vdd",    "I6/A2", "I6/temp0")

nfet(0.65, 10 * 0.65, "5_I6",     "Vgnd",    "I6/A1", "I6/temp1")
nfet(0.65, 3 * 0.65, "7_I6", "I6/temp1",    "I6/A2", "I6/temp2")

pfet(1.00, 2 * 1.00, "1_I6", "I6/temp2",    "I6/B1", "I6/temp0")
nfet(0.65, 0.36, "0_I6",     "Vgnd",    "I6/B1", "I6/temp2")

pfet(1.00, 3 * 1.00, "2_I6",      "Vdd", "I6/temp2",     "I6/X")
nfet(0.65, 3 * 0.65, "4_I6",     "Vgnd", "I6/temp2",     "I6/X")


ground_truth_start(6, 1.166, 1.517, 0.691, 0.969)
ground_truth_end(6, 1.393, 1.784, 0.841, 1.094)
on_rise(6, "fall")

# ===  a211o, C1=0, A1=1, B1=0 ===
cell_name(6, "a211o")
other_pins(6, "C1=0, A1=1, B1=0")
input_pin(6, "A2")
transition_new(6, 0.0439, 0.0777)
capa(7, 0.004707)
capa(7, 0.006688504)

pfet(1.00, 4 * 1.00, "8_I7", "I7/temp3",    "I7/B1", "I7/temp1")
pfet(1.00, 4 * 1.00, "1_I7", "I7/temp2",    "I7/C1", "I7/temp1")

nfet(0.65, 0.36, "3_I7",     "Vgnd",    "I7/B1", "I7/temp2")
nfet(0.65, 0.36, "9_I7",     "Vgnd",    "I7/C1", "I7/temp2")

pfet(1.00, 0.36, "6_I7",      "Vdd",    "I7/A1", "I7/temp3")
pfet(1.00, 3 * 1.00, "2_I7",      "Vdd",    "I7/A2", "I7/temp3")

nfet(0.65, 10 * 0.65, "5_I7",     "Vgnd",    "I7/A1", "I7/temp0")
nfet(0.65, 3 * 0.65, "7_I7", "I7/temp0",    "I7/A2", "I7/temp2")

pfet(1.00, 3 * 1.00, "0_I7",      "Vdd", "I7/temp2",     "I7/X")
nfet(0.65, 3 * 0.65, "4_I7",     "Vgnd", "I7/temp2",     "I7/X")


ground_truth_start(7, 1.394, 1.785, 0.842, 1.094)
ground_truth_end(7, 1.713, 2.021, 1.042, 1.219)
on_rise(7, "fall")

# ===  a311o, C1=0, A1=1, A2=1, B1=0 ===
cell_name(7, "a311o")
other_pins(7, "C1=0, A1=1, A2=1, B1=0")
input_pin(7, "A3")
transition_new(7, 0.0474, 0.0711)
capa(8, 0.0070869997)
capa(8, 0.008910184)

pfet(1.00, 0.36, "7_I8" ,      "Vdd",    "I8/A1", "I8/temp0")
pfet(1.00, 0.36, "1_I8" ,      "Vdd",    "I8/A2", "I8/temp0")
pfet(1.00, 4 * 1.00, "9_I8" ,      "Vdd",    "I8/A3", "I8/temp0")

nfet(0.65, 20 * 0.65, "5_I8" ,     "Vgnd",    "I8/A1", "I8/temp4")
nfet(0.65, 20 * 0.65, "3_I8" , "I8/temp4",    "I8/A2", "I8/temp1")
nfet(0.65, 4 * 0.65, "4_I8" , "I8/temp2",    "I8/A3", "I8/temp1")

pfet(1.00, 4 * 1.00, "11_I8", "I8/temp3",    "I8/B1", "I8/temp0")
pfet(1.00, 4 * 1.00, "0_I8" , "I8/temp3",    "I8/C1", "I8/temp2")
nfet(0.65, 0.36, "2_I8" ,     "Vgnd",    "I8/B1", "I8/temp2")
nfet(0.65, 0.36, "10_I8",     "Vgnd",    "I8/C1", "I8/temp2")

pfet(2.00, 2.0 * 2.00, "6_I8" ,      "Vdd", "I8/temp2",     "I8/X")
nfet(1.30, 2.0 * 1.30, "8_I8" ,     "Vgnd", "I8/temp2",     "I8/X")


ground_truth_start(8, 1.714, 2.021, 1.042, 1.219)
ground_truth_end(8, 2.088, 2.277, 1.252, 1.344)
on_rise(8, "fall")

# ===  a221oi, B2=1, C1=0, A1=1, B1=0 ===
cell_name(8, "a221oi")
other_pins(8, "B2=1, C1=0, A1=1, B1=0")
input_pin(8, "A2")
transition_new(8, 0.0522, 0.0815)
capa(9, 0.002373)
capa(9, 0.0044560134)

pfet(2.00, 3.5 * 2.00, "1_I9" , "I9/temp1", "I9/B1", "I9/temp0")
pfet(2.00, 3.5 * 2.00, "5_I9" , "I9/temp1", "I9/B2", "I9/temp0")

nfet(1.30, 0.36, "3_I9" ,     "Vgnd", "I9/B2", "I9/temp3")
nfet(1.30, 0.36, "0_I9" , "I9/temp3", "I9/B1",     "I9/Y")

pfet(2.00, 0.36, "6_I9" ,      "Vdd", "I9/A1", "I9/temp1")
pfet(2.00, 3.5 * 2.00, "2_I9" ,      "Vdd", "I9/A2", "I9/temp1")

nfet(1.30, 10 * 1.30, "7_I9" ,     "Vgnd", "I9/A1", "I9/temp2")
nfet(1.30, 3.5 * 1.30, "4_I9" , "I9/temp2", "I9/A2",     "I9/Y")

pfet(2.00, 3.5 * 2.00, "9_I9" , "I9/temp0", "I9/C1",     "I9/Y")
nfet(1.30, 0.36, "10_I9",     "Vgnd", "I9/C1",     "I9/Y")


ground_truth_start(9, 2.089, 2.277, 1.253, 1.345)
ground_truth_end(9, 2.339, 2.367, 1.396, 1.390)
on_rise(9, "fall")

# ===  or4, D=0, C=0, B=0 ===
cell_name(9, "or4")
other_pins(9, "D=0, C=0, B=0")
input_pin(9, "A")
transition_new(9, 0.0775, 0.0318)
capa(10, 0.00152)
capa(10, 0.0044560134)
pfet(0.42, 20 * 0.42, "3_I10",       "Vdd",     "I10/D", "I10/temp1")
pfet(0.42, 20 * 0.42, "2_I10", "I10/temp1",     "I10/B", "I10/temp2")
pfet(0.42, 20 * 0.42, "5_I10", "I10/temp2",     "I10/C", "I10/temp3")
pfet(0.42, 3 * 0.42, "8_I10", "I10/temp3",     "I10/A", "I10/temp0")

nfet(0.42, 0.42, "9_I10",      "Vgnd",     "I10/A", "I10/temp0")
nfet(0.42, 0.36, "0_I10",      "Vgnd",     "I10/B", "I10/temp0")
nfet(0.42, 0.36, "7_I10",      "Vgnd",     "I10/C", "I10/temp0")
nfet(0.42, 0.36, "1_I10",      "Vgnd",     "I10/D", "I10/temp0")

pfet(1.00, 3 * 1.0,  "6_I10",       "Vdd", "I10/temp0", "I10/X")
nfet(0.65, 3 * 0.65, "4_I10",      "Vgnd", "I10/temp0", "I10/X")


ground_truth_start(10, 2.340, 2.367, 1.397, 1.390)
ground_truth_end(10, 2.532, 2.850, 1.542, 1.512)
on_rise(10, "rise")

# ===  a21oi, A2=1, B1=0 ===
cell_name(10, "a21oi")
other_pins(10, "A2=1, B1=0")
input_pin(10, "A1")
transition_new(10, 0.0563, 0.0374)
capa(11, 0.007154)
capa(11, 0.008910184)

pfet(2.00, 2 * 2.00, "5_I11" ,       "Vdd", "I11/A1", "I11/temp2")
pfet(2.00, 0.36, "7_I11" ,       "Vdd", "I11/A2", "I11/temp2")

nfet(0.65, 20 * 0.65, "0_I11" ,      "Vgnd", "I11/A2", "I11/temp0")
nfet(0.65, 2 * 0.65, "10_I11", "I11/temp0", "I11/A1",     "I11/Y")

nfet(0.65, 20 * 0.65, "3_I11" ,      "Vgnd", "I11/A2", "I11/temp1")
nfet(0.65, 2 * 0.65, "2_I11" , "I11/temp1", "I11/A1",     "I11/Y")

pfet(4.00, 4.00, "4_I11" , "I11/temp2", "I11/B1",     "I11/Y")
nfet(0.36, 0.36, "1_I11" ,      "Vgnd", "I11/B1",     "I11/Y")


ground_truth_start(11, 2.532, 2.850, 1.542, 1.513)
ground_truth_end(11, 2.649, 3.062, 1.593, 1.651)
on_rise(11, "rise")

# ===  o211a, A2=0, C1=1, B1=1 ===
cell_name(11, "o211a")
other_pins(11, "A2=0, C1=1, B1=1")
input_pin(11, "A1")
transition_new(11, 0.0387, 0.1300)
capa(12, 0.0073059998)
capa(12, 0.008910184)

pfet(1.00, 20 * 1.00, "5_I12",       "Vdd",    "I12/A2", "I12/temp0")
pfet(1.00, 3 * 1.00, "4_I12", "I12/temp0",    "I12/A1", "I12/temp2")

nfet(0.65, 3 * 0.65, "0_I12",      "Vgnd",    "I12/A1", "I12/temp3")
nfet(0.65, 0.36, "9_I12",      "Vgnd",    "I12/A2", "I12/temp3")

pfet(1.00, 0.36, "3_I12",       "Vdd",    "I12/B1", "I12/temp2")
pfet(1.00, 0.36, "2_I12",       "Vdd",    "I12/C1", "I12/temp2")
nfet(0.65, 3 * 0.65, "1_I12", "I12/temp3",    "I12/B1", "I12/temp1")
nfet(0.65, 3 * 0.65, "6_I12", "I12/temp2",    "I12/C1", "I12/temp1")

pfet(1.00, 3 * 1.00, "7_I12",       "Vdd", "I12/temp2",     "I12/X")
nfet(0.65, 3 * 0.65, "8_I12",      "Vgnd", "I12/temp2",     "I12/X")


ground_truth_start(12, 2.649, 3.062, 1.594, 1.652)
ground_truth_end(12, 2.926, 3.330, 1.707, 1.807)
on_rise(12, "fall")

# ===  a41o, A3=1, A4=1, A2=1, B1=0 ===
cell_name(12, "a41o")
other_pins(12, "A3=1, A4=1, A2=1, B1=0")
input_pin(12, "A1")
transition_new(12, 0.0377, 0.0820)
capa(13, 0.004739)
capa(13, 0.006688504)

pfet(1.00, 3 * 1.00, "5_I13" ,       "Vdd",    "I13/A1", "I13/temp0")
pfet(1.00, 0.36, "3_I13" ,       "Vdd",    "I13/A2", "I13/temp0")
pfet(1.00, 0.36, "2_I13" ,       "Vdd",    "I13/A3", "I13/temp0")
pfet(1.00, 0.36, "4_I13" ,       "Vdd",    "I13/A4", "I13/temp0")

nfet(0.65, 20 * 0.65, "1_I13" ,      "Vgnd",    "I13/A4", "I13/temp4")
nfet(0.65, 20 * 0.65, "11_I13", "I13/temp4",    "I13/A3", "I13/temp1")
nfet(0.65, 20 * 0.65, "0_I13" , "I13/temp1",    "I13/A2", "I13/temp2")
nfet(0.65, 3 * 0.65, "6_I13" , "I13/temp2",    "I13/A1", "I13/temp3")

pfet(1.00, 1.5 * 1.00, "7_I13" , "I13/temp3",    "I13/B1", "I13/temp0")
nfet(0.65, 0.36, "9_I13" ,      "Vgnd",    "I13/B1", "I13/temp3")

pfet(1.00, 3 * 1.00, "8_I13" ,       "Vdd", "I13/temp3",     "I13/X")
nfet(0.65, 3 * 0.65, "10_I13",      "Vgnd", "I13/temp3",     "I13/X")

ground_truth_start(13, 2.926, 3.330, 1.708, 1.808)
ground_truth_end(13, 3.163, 3.614, 1.868, 1.926)
on_rise(13, "fall")

# ===  a21oi, A2=1, B1=0 ===
cell_name(13, "a21oi")
other_pins(13, "A2=1, B1=0")
input_pin(13, "A1")
transition_new(13, 0.0473, 0.0852)
capa(14, 0.004508)
capa(14, 0.0044560134)
pfet(2.00, 3 * 2.00, "5_I14" ,       "Vdd", "I14/A1", "I14/temp2")
pfet(2.00, 0.36, "7_I14" ,       "Vdd", "I14/A2", "I14/temp2")

nfet(0.65, 10 * 0.65, "0_I14" ,      "Vgnd", "I14/A2", "I14/temp0")
nfet(0.65, 3 * 0.65, "10_I14", "I14/temp0", "I14/A1",     "I14/Y")

nfet(0.65, 10 * 0.65, "3_I14" ,      "Vgnd", "I14/A2", "I14/temp1")
nfet(0.65, 3 * 0.65, "2_I14" , "I14/temp1", "I14/A1",     "I14/Y")

pfet(2.00, 1.5 * 2.00, "4_I14" , "I14/temp2", "I14/B1",     "I14/Y")
nfet(1.30, 0.36, "1_I14" ,      "Vgnd", "I14/B1",     "I14/Y")


ground_truth_start(14, 3.164, 3.615, 1.868, 1.926)
ground_truth_end(14, 3.328, 3.713, 1.970, 1.967)
on_rise(14, "fall")

# ===  nand2b, B=1 ===
cell_name(14, "nand2b")
other_pins(14, "B=1")
input_pin(14, "A_N")
transition_new(14, 0.0791, 0.0295)
capa(15, 0.0046929996)
capa(15, 0.006688504)

pfet(0.42, 3 * 0.42, "4_I15",       "Vdd",   "I15/A_N", "I15/temp1")
nfet(0.42, 3 * 0.42, "1_I15",      "Vgnd",   "I15/A_N", "I15/temp1")

pfet(1.00, 0.36, "3_I15",       "Vdd",     "I15/B",     "I15/Y")
nfet(0.65, 20 * 0.65, "2_I15",      "Vgnd",     "I15/B", "I15/temp0")

pfet(1.00, 3 * 1.00, "5_I15",       "Vdd", "I15/temp1",     "I15/Y")
nfet(0.65, 3 * 0.65, "0_I15", "I15/temp0", "I15/temp1",     "I15/Y")

ground_truth_start(15, 3.328, 3.714, 1.970, 1.967)
ground_truth_end(15, 3.517, 3.916, 2.071, 2.074)
on_rise(15, "fall")

# ===  nor2, B=0 ===
cell_name(15, "nor2")
other_pins(15, "B=0")
input_pin(15, "A")
transition_new(15, 0.0646, 0.0364)
capa(16, 0.0038550003)
capa(16, 0.006688504)

pfet(1.00, 10.00,    "0_I16",       "Vdd", "I16/B", "I16/temp0")
pfet(1.00, 3 * 1.00, "3_I16", "I16/temp0", "I16/A",     "I16/Y")

nfet(0.65, 3 * 0.65, "2_I16",      "Vgnd", "I16/A",     "I16/Y")
nfet(0.65, 0.36,     "1_I16",      "Vgnd", "I16/B",     "I16/Y")


ground_truth_start(16, 3.517, 3.916, 2.072, 2.074)
ground_truth_end(16, 3.619, 4.182, 2.116, 2.150)
on_rise(16, "rise")

# ===  a311o, A3=1, C1=0, A1=1, B1=0 ===
cell_name(16, "a311o")
other_pins(16, "A3=1, C1=0, A1=1, B1=0")
input_pin(16, "A2")
transition_new(16, 0.0332, 0.0704)
capa(17, 0.004377)
capa(17, 0.0044560134)

pfet(1.00, 0.36, "10_I17",       "Vdd",    "I17/A1", "I17/temp4")
pfet(1.00, 2.5 * 1.00, "9_I17" ,       "Vdd",    "I17/A2", "I17/temp4")
pfet(1.00, 0.36, "8_I17" ,       "Vdd",    "I17/A3", "I17/temp4")

nfet(0.65, 20 * 0.65, "1_I17" ,      "Vgnd",    "I17/A3", "I17/temp2")
nfet(0.65, 20 * 0.65, "2_I17" , "I17/temp2",    "I17/A1", "I17/temp3")
nfet(0.65, 0.65, "4_I17" , "I17/temp3",    "I17/A2", "I17/temp1")

pfet(1.00, 2 * 1.00, "6_I17" , "I17/temp4",    "I17/B1", "I17/temp0")
pfet(1.00, 2 * 1.00, "5_I17" , "I17/temp1",    "I17/C1", "I17/temp0")
nfet(0.65, 0.36, "3_I17" ,      "Vgnd",    "I17/B1", "I17/temp1")
nfet(0.65, 0.36, "0_I17" ,      "Vgnd",    "I17/C1", "I17/temp1")

pfet(1.00, 2 * 1.00, "7_I17" ,       "Vdd", "I17/temp1",     "I17/X")
nfet(0.65, 2 * 0.65, "11_I17",      "Vgnd", "I17/temp1",     "I17/X")


ground_truth_start(17, 3.619, 4.182, 2.116, 2.150)
ground_truth_end(17, 3.931, 4.453, 2.305, 2.306)
on_rise(17, "fall")

# ===  a21o, A2=1, B1=0 ===
cell_name(17, "a21o")
other_pins(17, "A2=1, B1=0")
input_pin(17, "A1")
transition_new(17, 0.0519, 0.0872)
capa(18, 0.0047270004)
capa(18, 0.006688504)

pfet(1.00, 3.5 * 1.00, "3_I18",       "Vdd",    "I18/A1", "I18/temp0")
pfet(1.00, 0.36, "6_I18",       "Vdd",    "I18/A2", "I18/temp0")

nfet(0.65, 20 * 0.65, "5_I18",      "Vgnd",    "I18/A2", "I18/temp1")
nfet(0.65, 3.5 * 0.65, "7_I18", "I18/temp1",    "I18/A1", "I18/temp2")

nfet(0.65, 0.36, "0_I18",      "Vgnd",    "I18/B1", "I18/temp2")
pfet(1.00, 3.5 * 1.00, "1_I18", "I18/temp2",    "I18/B1", "I18/temp0")

pfet(1.00, 3.5 * 1.00, "2_I18",       "Vdd", "I18/temp2",     "I18/X")
nfet(0.65, 3.5 * 0.65, "4_I18",      "Vgnd", "I18/temp2",     "I18/X")


ground_truth_start(18, 3.931, 4.453, 2.305, 2.306)
ground_truth_end(18, 4.145, 4.657, 2.443, 2.412)
on_rise(18, "fall")

# ===  o21a, A2=1, A1=1 ===
cell_name(18, "o21a")
other_pins(18, "A2=1, A1=1")
transition_new(18, 0.0363, 0.0634)
capa(19, 0.0023304995)

pfet(1.00, 0.36, "0_I19",       "Vdd",    "I19/A1", "I19/temp2")
pfet(1.00, 0.36, "6_I19", "I19/temp2",    "I19/A2", "I19/temp1")

nfet(0.65, 10 * 0.65, "2_I19",      "Vgnd",    "I19/A1", "I19/temp0")
nfet(0.65, 10 * 0.65, "3_I19",      "Vgnd",    "I19/A2", "I19/temp0")

pfet(1.00, 4 * 1.00, "5_I19",       "Vdd",    "I19/B1", "I19/temp1")
nfet(0.65, 4 * 0.65, "1_I19", "I19/temp1",    "I19/B1", "I19/temp0")

pfet(1.00, 4 * 1.00, "4_I19",       "Vdd", "I19/temp1",     "I19/X")
nfet(0.65, 4 * 0.65, "7_I19",      "Vgnd", "I19/temp1",     "I19/X")


ground_truth_start(19, 4.145, 4.657, 2.444, 2.413)
ground_truth_end(19, 4.254, 4.779, 2.508, 2.477)
on_rise(19, "fall")

# ===  a21oi, A2=0, A1=1 ===
cell_name(19, "a21oi")
other_pins(19, "A2=0, A1=1")
transition_new(19, 0.0148, 0.0249)
capa(20, 0.0023304995)

pfet(1.00, 20 * 1.00, "3_I20",       "Vdd", "I20/A1", "I20/temp1")
pfet(1.00, 20 * 1.00, "1_I20",       "Vdd", "I20/A2", "I20/temp1")
pfet(1.00, 2 * 1.00, "4_I20", "I20/temp1", "I20/B1",     "I20/Y")

nfet(0.65, 0.36, "0_I20", "I20/temp0", "I20/A1",     "I20/Y")
nfet(0.65, 0.36, "5_I20",      "Vgnd", "I20/A2", "I20/temp0")
nfet(0.65, 2 * 0.65, "2_I20",      "Vgnd", "I20/B1",     "I20/Y")


ground_truth_start(20, 4.254, 4.779, 2.508, 2.477)
ground_truth_end(20, 4.421, 4.831, 2.584, 2.512)
on_rise(20, "fall")

# ===  xnor2, B=0 ===
cell_name(20, "xnor2")
other_pins(20, "B=0")
transition_new(20, 0.0843, 0.0322)

capa(21, 0.0023304995)

pfet(1.00, 10 * 1.00, "0_I21",       "Vdd",     "I21/B", "I21/temp3")
pfet(1.00, 0.36, "6_I21",       "Vdd",     "I21/B", "I21/temp2")
pfet(1.00, 3 * 1.00, "1_I21",       "Vdd",     "I21/A", "I21/temp2")

nfet(0.65, 10 * 0.65, "5_I21",      "Vgnd",     "I21/B", "I21/temp1")
nfet(0.65, 10 * 0.65, "9_I21",      "Vgnd",     "I21/B", "I21/temp0")
nfet(0.65, 3 * 0.65, "2_I21", "I21/temp2",     "I21/A", "I21/temp1")
nfet(0.65, 3 * 0.65, "3_I21",      "Vgnd",     "I21/A", "I21/temp0")

pfet(1.00, 3 * 1.00, "8_I21", "I21/temp3",     "I21/A",     "I21/Y")

pfet(1.00, 3 * 1.00, "7_I21",       "Vdd", "I21/temp2",     "I21/Y")
nfet(0.65, 3 * 0.65, "4_I21", "I21/temp0", "I21/temp2",     "I21/Y")


ground_truth_start(21, 4.421, 4.831, 2.584, 2.512)
ground_truth_end(21, 4.510, 4.982, 2.646, 2.588)
on_rise(21, "rise")

# ===  a22o, A2=0, B2=1, A1=1 ===
cell_name(21, "a22o")
other_pins(21, "A2=0, B2=1, A1=1")
transition_new(21, 0.0350, 0.0619)

capa(22, 0.0023304995)
pfet(1.00, 2 * 1.00, "4_I22", "I22/temp1",    "I22/B1", "I22/temp0")
pfet(1.00, 0.36, "8_I22", "I22/temp1",    "I22/B2", "I22/temp0")

nfet(0.65, 10 * 0.65, "9_I22",      "Vgnd",    "I22/B2", "I22/temp3")
nfet(0.65, 2 * 0.65, "1_I22", "I22/temp3",    "I22/B1", "I22/temp0")

pfet(1.00, 10 * 1.0, "5_I22",       "Vdd",    "I22/A1", "I22/temp1")
pfet(1.00, 10 * 1.0, "0_I22",       "Vdd",    "I22/A2", "I22/temp1")

nfet(0.65, 0.36, "6_I22", "I22/temp2",    "I22/A1", "I22/temp0")
nfet(0.65, 0.36, "2_I22",      "Vgnd",    "I22/A2", "I22/temp2")

pfet(1.00, 2 * 1.00, "3_I22",       "Vdd", "I22/temp0",     "I22/X")
nfet(0.65, 2 * 0.65, "7_I22",      "Vgnd", "I22/temp0",     "I22/X")

ground_truth_start(22, 4.510, 4.982, 2.646, 2.588)
ground_truth_end(22, 4.689, 5.131, 2.733, 2.671)
on_rise(22, "fall")

# ===  a21o, A1=1, B1=0 ===
cell_name(22, "a21o")
other_pins(22, "A1=1, B1=0")
transition_new(22, 0.0256, 0.0486)

capa(23, 0.0023304995)
pfet(1.00, 0.36, "3_I23",       "Vdd",    "I23/A1", "I23/temp0")
pfet(1.00, 3 * 1.00, "6_I23",       "Vdd",    "I23/A2", "I23/temp0")

nfet(0.65, 20 * 0.65, "5_I23",      "Vgnd",    "I23/A1", "I23/temp1")
nfet(0.65, 3 * 0.65, "7_I23", "I23/temp2",    "I23/A2", "I23/temp1")

pfet(1.00, 3 * 1.00, "1_I23", "I23/temp2",    "I23/B1", "I23/temp0")
nfet(0.65, 0.36, "0_I23",      "Vgnd",    "I23/B1", "I23/temp2")

pfet(1.00, 3 * 1.00, "2_I23",       "Vdd", "I23/temp2",     "I23/X")
nfet(0.65, 3 * 0.65, "4_I23",      "Vgnd", "I23/temp2",     "I23/X")


ground_truth_start(23, 4.689, 5.131, 2.733, 2.671)
ground_truth_end(23, 4.847, 5.246, 2.843, 2.740)
on_rise(23, "fall")

# ===  and2, A=1 ===
cell_name(23, "and2")
other_pins(23, "A=1")
transition_new(23, 0.0218, 0.0265)
capa(24, 0.001678)
capa(24, 0.0023304995)
capa(24, 0.00126)
pfet(0.42, 0.36, "0_I24",       "Vdd",     "I24/A", "I24/temp1")
pfet(0.42, 3 * 0.42, "4_I24",       "Vdd",     "I24/B", "I24/temp1")

nfet(0.42, 5 * 0.42, "1_I24",      "Vgnd",     "I24/A", "I24/temp0")
nfet(0.42, 3 * 0.42, "2_I24", "I24/temp1",     "I24/B", "I24/temp0")

pfet(1.00, 3 * 1.00, "5_I24",       "Vdd", "I24/temp1",     "I24/X")
nfet(0.65, 3 * 0.65, "3_I24",      "Vgnd", "I24/temp1",     "I24/X")

ground_truth_start(24, 4.848, 5.246, 2.832, 2.728)
ground_truth_end(24, 5.007, 5.419, 2.929, 2.806)
on_rise(24, "fall")

import netCDF4 as nc

def mk_vector(vec_size, transition, capa, sizes):
    jj = 0

    vector = np.zeros(vec_size)

    def addval(v):
        nonlocal jj
        vector[jj] = v
        jj += 1

    addval(1.0)
    addval(transition)
    addval(capa)

    numb_fets = len(sizes)

    for j in range(numb_fets):
        w_j = sizes[j]
        addval(1.0 / w_j)
        addval(capa / w_j)
        addval(np.cbrt(capa / w_j))
        addval(np.sqrt(transition / w_j))
        addval(np.cbrt(transition * capa / w_j))

    for j in range(numb_fets):
        w_j = sizes[j]
        for k in range(numb_fets):
            if j == k:
                continue
            w_k = sizes[k]
            addval(w_j / w_k)
            addval(capa / (w_j + w_k))

    return vector
for cell_i, cell in data.items():
    path = f"models/sky130_fd_sc_hd__{cell['cell_name']}.nc"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    if cell['cell_name'] != 'mux2':
        continue
    estimator_data = nc.Dataset(path, "r")
    first_group = next(estimator_data.groups.__iter__())

    pin_list = [name.split(":")[0] for name in first_group.split(",")]

    other_pins_map = {
        'val_'+value.split("=")[0].strip(): "1.8" if value.split("=")[1].strip() == "1" else "0" for value in cell['other_pins'].strip().split(",") if value != ''
    }


    capa = cell['capa'] * 1000

    if cell_i+1 in data:
        next_cell_input_pin = data[cell_i+1]['input_pin']
        for trans in data[cell_i+1]['fet']:
            if trans[2].endswith('/'+next_cell_input_pin):
                capa += trans[1] * 0.15 * 0.01 * 1000 # 0.01 is pF/um²


    for risefall in ["rise", "fall"]:
        risefall_inv = "rise" if risefall == "fall" else "fall"
        rise_case = risefall_inv if cell['on_rise'] == 'fall' else risefall

        case = ""
        for i,pin in enumerate(pin_list):
            if pin in other_pins_map:
                case += f"{pin}:{other_pins_map[pin]}"
            else:
                case += f"{pin}:{rise_case}"

            if i < len(pin_list) - 1:
                case += ","

        if cell['cell_name'] == 'and2':
            case = f"val_B:1.8,val_A:{rise_case}"

        estimator = estimator_data.groups[case]
        values = estimator.variables["linear_estimator"][:, :]

        fet_sizes = []

        maxfet = max([int(fet[0]) for fet in cell['fet']])
        if maxfet != len(cell['fet']) - 1:
            print("fets are not contiguous for", cell['cell_name'])
            continue

        numb_fets = len(cell['fet'])

        if 3 + 5 * numb_fets + 2 * numb_fets * (numb_fets - 1) != values.shape[0]:
            print("Wrong number of transistors for cell", cell['cell_name'])
            continue

        for fet in sorted(cell['fet'], key=lambda x: x[0]):
            fet_sizes.append(fet[1])

        transition = cell['transition_new'][1 if risefall == "fall" else 0]

        print(transition* 1.0 / 0.6, capa,fet_sizes)
        vector = mk_vector(values.shape[0], transition* 1.0 / 0.6, capa, fet_sizes)

        estimated = values.T @ vector


        real_dt = cell['ground_truth_end'][3 if risefall == "fall" else 2] - cell['ground_truth_start'][3 if risefall == "fall" else 2]
        real_trans = 0.1
        if cell_i + 1 in data:
            real_trans = data[cell_i + 1]['transition_new'][1 if risefall == 'fall' else 0]

        rel_err_dt = np.abs(estimated[0] - real_dt) / np.maximum(0.1, real_dt)
        rel_err_trans = np.abs(estimated[1] - real_trans) / real_trans

        print(cell['cell_name'], risefall, rel_err_dt, rel_err_trans, [real_dt, real_trans], estimated)

        #print(vector)