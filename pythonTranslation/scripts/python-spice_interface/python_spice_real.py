
bins_nfet = [
    0.36,
    0.39,
    0.42,
    0.52,
    0.54,
    0.55,
    0.58,
    0.6,
    0.61,
    0.64,
    0.65,
    0.74,
    0.84,
    1.0,
    1.26,
    1.68,
    2.0,
    3.0,
    5.0,
    7.0
]

bins_pfet = [
    0.36,
    0.42,
    0.54,
    0.55,
    0.63,
    0.64,
    0.70,
    0.75,
    0.79,
    0.82,
    0.84,
    0.86,
    0.94,
    1.00,
    1.12,
    1.26,
    1.65,
    1.68,
    2.00,
    3.00,
    5.00,
    7.00
]

MINSIZE = 0.36

timings_to_track = set()

def area(W):
    return 0.15 * W

def perim(W):
    return 2*(W + 0.15)

fets = {}

use_old = False

total_size_old = 0
total_size = 0

def pfet(oldW, W, name, D, G, S):
    global use_old
    global total_size
    global total_size_old

    total_size += W
    total_size_old += oldW

    if use_old:
        W = oldW
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    mult = W

    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"

def nfet(oldW, W, name, D, G, S):
    global use_old
    global total_size
    global total_size_old

    total_size += W
    total_size_old += oldW

    if use_old:
        W = oldW
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"

with open("../../libs/ngspice/out.spice", 'r') as f:
    spice = f.read()

spice = spice.split('\n')

to_clear = ['2_I1', '4_I1', '6_I1', '7_I1', '8_I1', '9_I1', '1_I2', '2_I2', '3_I2', '5_I2', '6_I2', '7_I2', '11_I4', '13_I4', '12_I8', '13_I8', '8_I9', '11_I9', '12_I9', '13_I9', '14_I9', '15_I9', '16_I9', '17_I9', '18_I9', '19_I9', '6_I11', '8_I11', '9_I11', '11_I11', '6_I14', '8_I14', '9_I14', '11_I14']
for name in to_clear: fets[name] = ''

# ===  dfxtp ===
pfet(0.42, 0.42, "5_I0" ,      "Vdd",     "I0/D", "I0/temp10")
pfet(0.42, 0.42, "17_I0",      "Vdd", "I0/temp1",  "I0/temp5")
pfet(1.00, 1.00, "7_I0" ,      "Vdd", "I0/temp2",  "I0/temp1")
pfet(0.42, 0.42, "2_I0" , "I0/temp6", "I0/temp3",  "I0/temp4")
pfet(0.42, 0.42, "15_I0", "I0/temp8", "I0/temp3",  "I0/temp2")
pfet(0.64, 0.64, "19_I0",      "Vdd", "I0/temp3",  "I0/temp9")
pfet(0.75, 0.75, "11_I0",      "Vdd", "I0/temp6",  "I0/temp8")
pfet(0.42, 0.42, "9_I0" ,      "Vdd", "I0/temp8",  "I0/temp4")
pfet(0.42, 0.42, "8_I0" , "I0/temp6", "I0/temp9", "I0/temp10")
pfet(0.42, 0.42, "12_I0", "I0/temp5", "I0/temp9",  "I0/temp2")
pfet(0.64, 0.64, "3_I0" ,      "Vdd",      "clk",  "I0/temp3")
nfet(0.42, 0.42, "22_I0",     "Vgnd",     "I0/D", "I0/temp10")
nfet(0.42, 0.42, "13_I0",     "Vgnd", "I0/temp1",  "I0/temp0")
nfet(0.65, 0.65, "21_I0",     "Vgnd", "I0/temp2",  "I0/temp1")
nfet(0.42, 0.42, "14_I0",     "Vgnd", "I0/temp3",  "I0/temp9")
nfet(0.36, 0.36, "18_I0", "I0/temp2", "I0/temp3",  "I0/temp0")
nfet(0.36, 0.36, "20_I0", "I0/temp6", "I0/temp3", "I0/temp10")
nfet(0.64, 0.64, "10_I0",     "Vgnd", "I0/temp6",  "I0/temp8")
nfet(0.42, 0.42, "6_I0" ,     "Vgnd", "I0/temp8",  "I0/temp7")
nfet(0.36, 0.36, "1_I0" , "I0/temp8", "I0/temp9",  "I0/temp2")
nfet(0.36, 0.36, "16_I0", "I0/temp7", "I0/temp9",  "I0/temp6")
nfet(0.42, 0.42, "23_I0",     "Vgnd",      "clk",  "I0/temp3")

pfet(1.00, 3 * 1.00, "4_I0" ,      "Vdd", "I0/temp1",      "I0/Q")
nfet(0.65, 3 * 0.65, "0_I0" ,     "Vgnd", "I0/temp1",      "I0/Q")

# timing for       I0/D:
# timing for       I0/Q: 0.074 0.438 | 0.033 0.344 -0.041 -0.094
# transition for   I0/Q: 0.0446 0.0333
# timing for        clk: 0.100 0.100 | 0.100 0.100
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613

# ===  clkbuf ===
pfet(4 * 1.00, 6 * 1.00, "0_I1",  "Vdd",     "I1/A", "I1/temp0")
nfet(4 * 0.42, 4 * 0.42, "5_I1", "Vgnd",     "I1/A", "I1/temp0")
pfet(4 * 4.00, 4 * 4.00, "3_I1",  "Vdd", "I1/temp0",     "I1/X")
nfet(4 * 1.68, 6 * 1.68, "1_I1", "Vgnd", "I1/temp0",     "I1/X")
# timing for       I1/A: 0.074 0.438 | 0.033 0.344 -0.041 -0.094
# timing for       I1/X: 0.204 0.567 | 0.152 0.438 -0.052 -0.129
# transition for   I1/X: 0.0380 0.0241
# timing for   I1/temp0: 0.149 0.525 | 0.096 0.405 -0.053 -0.120
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  buf ===
pfet(4 * 1.00, 4 * 1.00, "8_I2",  "Vdd",     "I2/A", "I2/temp0")
nfet(4 * 0.65, 6 * 0.65, "9_I2", "Vgnd",     "I2/A", "I2/temp0")

pfet(4 * 4.00, 6 * 4.00, "0_I2",  "Vdd", "I2/temp0",     "I2/X")
nfet(4 * 2.60, 4 * 2.60, "4_I2", "Vgnd", "I2/temp0",     "I2/X")
# timing for       I2/A: 0.206 0.568 | 0.152 0.438 -0.054 -0.130
# timing for   I2/temp0: 0.249 0.652 | 0.190 0.538 -0.059 -0.114
# timing for       I2/X: 0.303 0.694 | 0.238 0.593 -0.065 -0.101
# transition for   I2/X: 0.0391 0.0411
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  mux2, A0=1, A1=0 ===
pfet(0.42, 16 * 0.42, "1_I3" ,      "Vdd",     "I3/S", "I3/temp1")
nfet(0.42, 16 * 0.42, "5_I3" ,     "Vgnd",     "I3/S", "I3/temp1")

pfet(0.42, 8 * 0.42, "0_I3" ,      "Vdd", "I3/temp1", "I3/temp3")
nfet(0.42, 8 * 0.42, "3_I3" ,     "Vgnd", "I3/temp1", "I3/temp0")

pfet(0.42, 8 * 0.42, "7_I3" , "I3/temp3",    "I3/A1", "I3/temp5")                         # Max size: 406.743

nfet(0.42, 8 * 0.42, "8_I3" , "I3/temp2",    "I3/A1", "I3/temp5")                         # Max size: 692.063
nfet(0.42, 4 * 0.42, "9_I3" ,     "Vgnd",     "I3/S", "I3/temp2")

pfet(0.42, 4 * 0.42, "2_I3" ,      "Vdd",     "I3/S", "I3/temp4")
pfet(0.42, 8 * 0.42, "4_I3" , "I3/temp4",    "I3/A0", "I3/temp5")                         # Max size: 155.188
nfet(0.42, 8 * 0.42, "6_I3" , "I3/temp0",    "I3/A0", "I3/temp5")                         # Max size: 264.0

pfet(1.00, 4 * 1.00, "10_I3",      "Vdd", "I3/temp5",     "I3/X")
nfet(0.65, 4 * 0.65, "11_I3",     "Vgnd", "I3/temp5",     "I3/X")
# timing for       I3/S: 0.305 0.696 | 0.238 0.593 -0.067 -0.103
# timing for       I3/X: 0.621 0.924 | 0.433 0.724 -0.188 -0.200
# transition for   I3/X: 0.0371 0.0458
# timing for   I3/temp0: 0.560 0.775 | 0.391 0.641 -0.169 -0.134
# timing for   I3/temp5: 0.537 0.828 | 0.385 0.672 -0.152 -0.156
# timing for   I3/temp2:
# timing for   I3/temp3: 0.358 1.112 | 0.270 0.959 -0.088 -0.153
# timing for   I3/temp4:
# timing for   I3/temp1: 0.340 0.764 | 0.255 0.632 -0.085 -0.132
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  mux2, S=0, A1=1 ===
pfet(0.64, 0.64, "12_I4",      "Vdd",     "I4/S", "I4/temp4")                         # Max size: 195.958
nfet(0.42, 0.42, "9_I4" ,     "Vgnd",     "I4/S", "I4/temp4")                         # Max size: 333.418

pfet(0.64, 10 * 0.64, "0_I4" ,      "Vdd",     "I4/S", "I4/temp0")                         # Max size: 195.958
pfet(0.64, 6 * 0.64, "1_I4" , "I4/temp5",    "I4/A0", "I4/temp0")
nfet(0.42, 8 * 0.42, "7_I4" , "I4/temp5",    "I4/A0", "I4/temp1")
nfet(0.42, 10 * 0.42, "8_I4" ,     "Vgnd", "I4/temp4", "I4/temp1")

pfet(0.64, 0.36, "6_I4" ,      "Vdd", "I4/temp4", "I4/temp2")
pfet(0.64, 0.36, "3_I4" , "I4/temp5",    "I4/A1", "I4/temp2")                         # Max size: 185.518
nfet(0.42, 0.36, "10_I4", "I4/temp5",    "I4/A1", "I4/temp3")                         # Max size: 315.654
nfet(0.42, 0.36, "5_I4" ,     "Vgnd",     "I4/S", "I4/temp3")                         # Max size: 333.418


pfet(2.00, 4.0 * 2.00, "2_I4" ,      "Vdd", "I4/temp5",     "I4/X")
nfet(1.30, 2.0 * 1.30, "4_I4" ,     "Vgnd", "I4/temp5",     "I4/X")
# timing for      I4/A0: 0.621 0.925 | 0.433 0.724 -0.188 -0.201
# timing for       I4/X: 0.957 1.206 | 0.578 0.816 -0.379 -0.390
# transition for   I4/X: 0.0534 0.0564
# timing for   I4/temp0:
# timing for   I4/temp1:
# timing for   I4/temp2:
# timing for   I4/temp3: 0.848 1.039 | 0.525 0.767 -0.323 -0.272
# timing for   I4/temp4:
# timing for   I4/temp5: 0.825 1.018 | 0.510 0.756 -0.315 -0.262
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  xor2, A=0 ===
pfet(1.00, 10*1.00, "8_I5",     "Vdd",     "I5/A", "I5/temp0")                          # Max size: 494.061
pfet(1.00,  2*1.00, "3_I5","I5/temp3",     "I5/B", "I5/temp0")

nfet(0.65, 2*0.36, "5_I5",     "Vgnd",     "I5/A", "I5/temp3")                          # Max size: 840.63
nfet(0.65, 2*0.65, "2_I5",     "Vgnd",     "I5/B", "I5/temp3")

pfet(1.00, 2*1.00, "0_I5", "I5/temp2", "I5/temp3",     "I5/X")
nfet(0.65, 2*0.65, "6_I5",     "Vgnd", "I5/temp3",     "I5/X")

pfet(1.00, 10*1.00, "7_I5",      "Vdd",     "I5/A", "I5/temp2")                          # Max size: 494.061
pfet(1.00, 3*1.00, "4_I5",      "Vdd",     "I5/B", "I5/temp2")

nfet(0.65, 3*0.65, "1_I5", "I5/temp1",     "I5/B",     "I5/X")
nfet(0.65, 10*0.65, "9_I5",     "Vgnd",     "I5/A", "I5/temp1")                          # Max size: 840.633

# timing for       I5/B: 0.959 1.208 | 0.578 0.816 -0.381 -0.392
# timing for       I5/X: 1.165 1.517 | 0.685 0.962 -0.480 -0.555
# transition for   I5/X: 0.0431 0.1389
# timing for   I5/temp0: 1.508 |
# timing for   I5/temp1: 1.536 | 0.993
# timing for   I5/temp2: 0.716 1.927 |
# timing for   I5/temp3: 1.078 1.260 | 0.635 0.845 -0.443 -0.415
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613
#use_old = False

# ===  a21o, A1=1, B1=0 ===
pfet(1.00, 0.36, "3_I6",      "Vdd",    "I6/A1", "I6/temp0")                          # Max size: 103.535
pfet(1.00, 3 * 1.00, "6_I6",      "Vdd",    "I6/A2", "I6/temp0")

nfet(0.65, 10 * 0.65, "5_I6",     "Vgnd",    "I6/A1", "I6/temp1")                          # Max size: 176.163
nfet(0.65, 3 * 0.65, "7_I6", "I6/temp1",    "I6/A2", "I6/temp2")

pfet(1.00, 2 * 1.00, "1_I6", "I6/temp2",    "I6/B1", "I6/temp0")                          # Max size: 359.621
nfet(0.65, 0.36, "0_I6",     "Vgnd",    "I6/B1", "I6/temp2")                          # Max size: 611.88

pfet(1.00, 3 * 1.00, "2_I6",      "Vdd", "I6/temp2",     "I6/X")
nfet(0.65, 3 * 0.65, "4_I6",     "Vgnd", "I6/temp2",     "I6/X")
# timing for      I6/A2: 1.166 1.517 | 0.685 0.962 -0.481 -0.555
# timing for       I6/X: 1.393 1.784 | 0.835 1.087 -0.558 -0.697
# transition for   I6/X: 0.0437 0.0775
# timing for   I6/temp0: 1.205 2.174 | 0.708 1.404 -0.497 -0.770
# timing for   I6/temp1:
# timing for   I6/temp2: 1.293 1.613 | 0.780 1.010 -0.513 -0.603
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a211o, C1=0, A1=1, B1=0 ===
pfet(1.00, 4 * 1.00, "8_I7", "I7/temp3",    "I7/B1", "I7/temp1")                          # Max size: 393.087
pfet(1.00, 4 * 1.00, "1_I7", "I7/temp2",    "I7/C1", "I7/temp1")                          # Max size: 307.884

nfet(0.65, 0.36, "3_I7",     "Vgnd",    "I7/B1", "I7/temp2")                          # Max size: 668.828
nfet(0.65, 0.36, "9_I7",     "Vgnd",    "I7/C1", "I7/temp2")                          # Max size: 523.858

pfet(1.00, 0.36, "6_I7",      "Vdd",    "I7/A1", "I7/temp3")                          # Max size: 61.726
pfet(1.00, 3 * 1.00, "2_I7",      "Vdd",    "I7/A2", "I7/temp3")

nfet(0.65, 10 * 0.65, "5_I7",     "Vgnd",    "I7/A1", "I7/temp0")                          # Max size: 105.02
nfet(0.65, 3 * 0.65, "7_I7", "I7/temp0",    "I7/A2", "I7/temp2")

pfet(1.00, 3 * 1.00, "0_I7",      "Vdd", "I7/temp2",     "I7/X")
nfet(0.65, 3 * 0.65, "4_I7",     "Vgnd", "I7/temp2",     "I7/X")
# timing for      I7/A2: 1.394 1.785 | 0.835 1.087 -0.559 -0.698
# timing for       I7/X: 1.713 2.021 | 1.035 1.211 -0.678 -0.810
# transition for   I7/X: 0.0477 0.0709
# timing for   I7/temp0:
# timing for   I7/temp1: 1.467 2.871 | 0.888 1.885 -0.579 -0.986
# timing for   I7/temp2: 1.608 1.880 | 0.977 1.139 -0.631 -0.741
# timing for   I7/temp3: 1.435 3.718 | 0.860 2.355 -0.575 -1.363
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a311o, C1=0, A1=1, A2=1, B1=0 ===
pfet(1.00, 0.36, "7_I8" ,      "Vdd",    "I8/A1", "I8/temp0")                         # Max size: 147.006
pfet(1.00, 0.36, "1_I8" ,      "Vdd",    "I8/A2", "I8/temp0")                         # Max size: 77.015
pfet(1.00, 4 * 1.00, "9_I8" ,      "Vdd",    "I8/A3", "I8/temp0")

nfet(0.65, 20 * 0.65, "5_I8" ,     "Vgnd",    "I8/A1", "I8/temp4")                         # Max size: 250.127
nfet(0.65, 20 * 0.65, "3_I8" , "I8/temp4",    "I8/A2", "I8/temp1")                         # Max size: 131.04
nfet(0.65, 4 * 0.65, "4_I8" , "I8/temp2",    "I8/A3", "I8/temp1")

pfet(1.00, 4 * 1.00, "11_I8", "I8/temp3",    "I8/B1", "I8/temp0")                         # Max size: 450.017
pfet(1.00, 4 * 1.00, "0_I8" , "I8/temp3",    "I8/C1", "I8/temp2")                         # Max size: 376.739
nfet(0.65, 0.36, "2_I8" ,     "Vgnd",    "I8/B1", "I8/temp2")                         # Max size: 765.693
nfet(0.65, 0.36, "10_I8",     "Vgnd",    "I8/C1", "I8/temp2")                         # Max size: 641.012

pfet(2.00, 2.0 * 2.00, "6_I8" ,      "Vdd", "I8/temp2",     "I8/X")
nfet(1.30, 2.0 * 1.30, "8_I8" ,     "Vgnd", "I8/temp2",     "I8/X")
#use_old = False
# timing for      I8/A3: 1.714 2.021 | 1.035 1.211 -0.679 -0.810
# timing for       I8/X: 2.088 2.277 | 1.246 1.336 -0.842 -0.941
# transition for   I8/X: 0.0522 0.0811
# timing for   I8/temp0: 1.757 4.301 | 1.060 2.577 -0.697 -1.724
# timing for   I8/temp1:
# timing for   I8/temp2: 1.985 2.142 | 1.181 1.258 -0.804 -0.884
# timing for   I8/temp3: 1.790 3.251 | 1.086 2.045 -0.704 -1.206
# timing for   I8/temp4:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a221oi, B2=1, C1=0, A1=1, B1=0 ===
pfet(2.00, 3.5 * 2.00, "1_I9" , "I9/temp1", "I9/B1", "I9/temp0")                            # Max size: 471.366
pfet(2.00, 3.5 * 2.00, "5_I9" , "I9/temp1", "I9/B2", "I9/temp0")                            # Max size: 190.889

nfet(1.30, 0.36, "3_I9" ,     "Vgnd", "I9/B2", "I9/temp3")                            # Max size: 324.794
nfet(1.30, 0.36, "0_I9" , "I9/temp3", "I9/B1",     "I9/Y")                            # Max size: 802.018

pfet(2.00, 0.36, "6_I9" ,      "Vdd", "I9/A1", "I9/temp1")                            # Max size: 174.774
pfet(2.00, 3.5 * 2.00, "2_I9" ,      "Vdd", "I9/A2", "I9/temp1")

nfet(1.30, 10 * 1.30, "7_I9" ,     "Vgnd", "I9/A1", "I9/temp2")                            # Max size: 297.374
nfet(1.30, 3.5 * 1.30, "4_I9" , "I9/temp2", "I9/A2",     "I9/Y")

pfet(2.00, 3.5 * 2.00, "9_I9" , "I9/temp0", "I9/C1",     "I9/Y")                            # Max size: 469.058
nfet(1.30, 0.36, "10_I9",     "Vgnd", "I9/C1",     "I9/Y")
#use_old = False
# Max size: 798.091
# timing for      I9/A2: 2.089 2.277 | 1.246 1.336 -0.843 -0.941
# timing for       I9/Y: 2.339 2.367 | 1.389 1.382 -0.950 -0.985
# transition for   I9/Y: 0.0774 0.0312
# timing for   I9/temp0: 2.170 3.791 | 1.306 2.356 -0.864 -1.435
# timing for   I9/temp1: 2.133 5.223 | 1.274 3.032 -0.859 -2.191
# timing for   I9/temp2:
# timing for   I9/temp3:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613

# ===  or4, D=0, C=0, B=0 ===
pfet(0.42, 20 * 0.42, "3_I10",       "Vdd",     "I10/D", "I10/temp1")                      # Max size: 157.955
pfet(0.42, 20 * 0.42, "2_I10", "I10/temp1",     "I10/B", "I10/temp2")                      # Max size: 230.202
pfet(0.42, 20 * 0.42, "5_I10", "I10/temp2",     "I10/C", "I10/temp3")                      # Max size: 221.739
pfet(0.42, 3 * 0.42, "8_I10", "I10/temp3",     "I10/A", "I10/temp0")

nfet(0.42, 0.42, "9_I10",      "Vgnd",     "I10/A", "I10/temp0")
nfet(0.42, 0.36, "0_I10",      "Vgnd",     "I10/B", "I10/temp0")                      # Max size: 391.682
nfet(0.42, 0.36, "7_I10",      "Vgnd",     "I10/C", "I10/temp0")                      # Max size: 377.283
nfet(0.42, 0.36, "1_I10",      "Vgnd",     "I10/D", "I10/temp0")                      # Max size: 268.757

pfet(1.00, 3 * 1.0,  "6_I10",       "Vdd", "I10/temp0", "I10/X")
nfet(0.65, 3 * 0.65, "4_I10",      "Vgnd", "I10/temp0", "I10/X")
#use_old = False

# timing for      I10/A: 2.340 2.367 | 1.389 1.382 -0.951 -0.985
# timing for      I10/X: 2.532 2.850 | 1.534 1.504 -0.998 -1.346
# transition for  I10/X: 0.0561 0.0371
# timing for    I10/temp0: 2.416 2.720 | 1.460 1.456 -0.956 -1.264
# timing for  I10/temp2:
# timing for  I10/temp3:
# timing for  I10/temp1:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a21oi, A2=1, B1=0 ===
#    old   new    name            drain   gate    source
pfet(2.00, 2 * 2.00, "5_I11" ,       "Vdd", "I11/A1", "I11/temp2")
pfet(2.00, 0.36, "7_I11" ,       "Vdd", "I11/A2", "I11/temp2")                        # Max size: 194.113

nfet(0.65, 20 * 0.65, "0_I11" ,      "Vgnd", "I11/A2", "I11/temp0")                        # Max size: 330.278
nfet(0.65, 2 * 0.65, "10_I11", "I11/temp0", "I11/A1",     "I11/Y")

nfet(0.65, 20 * 0.65, "3_I11" ,      "Vgnd", "I11/A2", "I11/temp1")                        # Max size: 330.278
nfet(0.65, 2 * 0.65, "2_I11" , "I11/temp1", "I11/A1",     "I11/Y")

pfet(4.00, 4.00, "4_I11" , "I11/temp2", "I11/B1",     "I11/Y")                        # Max size: 264.148
nfet(0.36, 0.36, "1_I11" ,      "Vgnd", "I11/B1",     "I11/Y")
#use_old = False
# Max size: 449.442
#                        ref           measure      delta = measure - ref
# timing for     I11/A1: 2.532 2.850 | 1.534 1.504 -0.998 -1.346
# timing for      I11/Y: 2.649 3.062 | 1.586 1.643 -1.063 -1.419
# transition for  I11/Y: 0.0382 0.1298
# timing for  I11/temp0:
# timing for  I11/temp1:
# timing for  I11/temp2: 3.016 2.905 | 1.863 1.526 -1.153 -1.379
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  o211a, A2=0, C1=1, B1=1 ===
pfet(1.00, 20 * 1.00, "5_I12",       "Vdd",    "I12/A2", "I12/temp0")                      # Max size: 327.425
pfet(1.00, 3 * 1.00, "4_I12", "I12/temp0",    "I12/A1", "I12/temp2")

nfet(0.65, 3 * 0.65, "0_I12",      "Vgnd",    "I12/A1", "I12/temp3")
nfet(0.65, 0.36, "9_I12",      "Vgnd",    "I12/A2", "I12/temp3")                      # Max size: 557.106

pfet(1.00, 0.36, "3_I12",       "Vdd",    "I12/B1", "I12/temp2")                      # Max size: 129.204
pfet(1.00, 0.36, "2_I12",       "Vdd",    "I12/C1", "I12/temp2")                      # Max size: 259.979
nfet(0.65, 3 * 0.65, "1_I12", "I12/temp3",    "I12/B1", "I12/temp1")                      # Max size: 219.838
nfet(0.65, 3 * 0.65, "6_I12", "I12/temp2",    "I12/C1", "I12/temp1")                      # Max size: 442.348

pfet(1.00, 3 * 1.00, "7_I12",       "Vdd", "I12/temp2",     "I12/X")
nfet(0.65, 3 * 0.65, "8_I12",      "Vgnd", "I12/temp2",     "I12/X")
#use_old = False

# timing for     I12/A1: 2.649 3.062 | 1.586 1.643 -1.063 -1.419
# timing for      I12/X: 2.926 3.330 | 1.699 1.798 -1.227 -1.532
# transition for  I12/X: 0.0379 0.0817
# timing for  I12/temp0:
# timing for  I12/temp1: 2.853 3.095 | 1.668 1.671 -1.185 -1.424
# timing for  I12/temp2: 2.814 3.155 | 1.651 1.712 -1.163 -1.443
# timing for  I12/temp3: 2.875 3.077 | 1.674 1.653 -1.201 -1.424
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a41o, A3=1, A4=1, A2=1, B1=0 ===
pfet(1.00, 3 * 1.00, "5_I13" ,       "Vdd",    "I13/A1", "I13/temp0")
pfet(1.00, 0.36, "3_I13" ,       "Vdd",    "I13/A2", "I13/temp0")                     # Max size: 290.888
pfet(1.00, 0.36, "2_I13" ,       "Vdd",    "I13/A3", "I13/temp0")                     # Max size: 227.5
pfet(1.00, 0.36, "4_I13" ,       "Vdd",    "I13/A4", "I13/temp0")                     # Max size: 217.087

nfet(0.65, 20 * 0.65, "1_I13" ,      "Vgnd",    "I13/A4", "I13/temp4")                     # Max size: 369.369
nfet(0.65, 20 * 0.65, "11_I13", "I13/temp4",    "I13/A3", "I13/temp1")                     # Max size: 387.086
nfet(0.65, 20 * 0.65, "0_I13" , "I13/temp1",    "I13/A2", "I13/temp2")                     # Max size: 494.939
nfet(0.65, 3 * 0.65, "6_I13" , "I13/temp2",    "I13/A1", "I13/temp3")

pfet(1.00, 1.5 * 1.00, "7_I13" , "I13/temp3",    "I13/B1", "I13/temp0")                     # Max size: 606.575
nfet(0.65, 0.36, "9_I13" ,      "Vgnd",    "I13/B1", "I13/temp3")                     # Max size: 1032.073

pfet(1.00, 3 * 1.00, "8_I13" ,       "Vdd", "I13/temp3",     "I13/X")
nfet(0.65, 3 * 0.65, "10_I13",      "Vgnd", "I13/temp3",     "I13/X")
#use_old = False

# timing for     I13/A1: 2.926 3.330 | 1.699 1.798 -1.227 -1.532
# timing for      I13/X: 3.163 3.614 | 1.859 1.916 -1.304 -1.698
# transition for  I13/X: 0.0471 0.0849
# timing for  I13/temp0: 2.977 4.192 | 1.720 2.333 -1.257 -1.859
# timing for  I13/temp1:
# timing for  I13/temp2:
# timing for  I13/temp3: 3.072 3.445 | 1.800 1.838 -1.272 -1.607
# timing for  I13/temp4:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a21oi, A2=1, B1=0 ===
pfet(2.00, 3 * 2.00, "5_I14" ,       "Vdd", "I14/A1", "I14/temp2")
pfet(2.00, 0.36, "7_I14" ,       "Vdd", "I14/A2", "I14/temp2")                        # Max size: 236.756

nfet(0.65, 10 * 0.65, "0_I14" ,      "Vgnd", "I14/A2", "I14/temp0")                        # Max size: 402.835
nfet(0.65, 3 * 0.65, "10_I14", "I14/temp0", "I14/A1",     "I14/Y")

nfet(0.65, 10 * 0.65, "3_I14" ,      "Vgnd", "I14/A2", "I14/temp1")                        # Max size: 402.835
nfet(0.65, 3 * 0.65, "2_I14" , "I14/temp1", "I14/A1",     "I14/Y")

pfet(2.00, 1.5 * 2.00, "4_I14" , "I14/temp2", "I14/B1",     "I14/Y")                        # Max size: 726.398
nfet(1.30, 0.36, "1_I14" ,      "Vgnd", "I14/B1",     "I14/Y")
#use_old = False
# Max size: 1235.948
# timing for     I14/A1: 3.164 3.615 | 1.859 1.916 -1.305 -1.699
# timing for      I14/Y: 3.328 3.713 | 1.961 1.957 -1.367 -1.756
# transition for  I14/Y: 0.0791 0.0294
# timing for  I14/temp0:
# timing for  I14/temp1:
# timing for  I14/temp2: 3.203 4.281 | 1.882 2.379 -1.321 -1.902
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  nand2b, B=1 ===
pfet(0.42, 3 * 0.42, "5_I15",       "Vdd",   "I15/A_N", "I15/temp1")
nfet(0.42, 3 * 0.42, "0_I15",      "Vgnd",   "I15/A_N", "I15/temp1")

pfet(1.00, 0.36, "4_I15",       "Vdd",     "I15/B",     "I15/Y")                      # Max size: 283.037
nfet(0.65, 20 * 0.65, "2_I15",      "Vgnd",     "I15/B", "I15/temp0")                      # Max size: 481.58

pfet(1.00, 3 * 1.00, "3_I15",       "Vdd", "I15/temp1",     "I15/Y")
nfet(0.65, 3 * 0.65, "1_I15", "I15/temp0", "I15/temp1",     "I15/Y") #
#use_old = False

# timing for    I15/A_N: 3.328 3.714 | 1.961 1.957 -1.367 -1.757
# timing for      I15/Y: 3.517 3.916 | 2.062 2.064 -1.455 -1.852
# transition for  I15/Y: 0.0644 0.0363
# timing for  I15/temp0:
# timing for  I15/temp1: 3.382 3.808 | 1.997 2.016 -1.385 -1.792
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  nor2, B=0 ===
pfet(1.00, 10.00,    "0_I16",       "Vdd", "I16/B", "I16/temp0")                          # Max size: 352.332
pfet(1.00, 3 * 1.00, "2_I16", "I16/temp0", "I16/A",     "I16/Y")

nfet(0.65, 3 * 0.65, "1_I16",      "Vgnd", "I16/A",     "I16/Y")
nfet(0.65, 0.36,     "3_I16",      "Vgnd", "I16/B",     "I16/Y")
#use_old = False
# Max size: 599.484
# timing for      I16/A: 3.517 3.916 | 2.062 2.064 -1.455 -1.852
# timing for      I16/Y: 3.619 4.182 | 2.106 2.139 -1.513 -2.043
# transition for  I16/Y: 0.0330 0.0701
# timing for  I16/temp0:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613

#

# ===  a311o, A3=1, C1=0, A1=1, B1=0 ===
pfet(1.00, 0.36, "10_I17",       "Vdd",    "I17/A1", "I17/temp4")                     # Max size: 303.532
pfet(1.00, 2.5 * 1.00, "9_I17" ,       "Vdd",    "I17/A2", "I17/temp4")
pfet(1.00, 0.36, "8_I17" ,       "Vdd",    "I17/A3", "I17/temp4")                     # Max size: 300.392

nfet(0.65, 20 * 0.65, "1_I17" ,      "Vgnd",    "I17/A3", "I17/temp2")                     # Max size: 511.109
nfet(0.65, 20 * 0.65, "2_I17" , "I17/temp2",    "I17/A1", "I17/temp3")                     # Max size: 516.453
nfet(0.65, 0.65, "4_I17" , "I17/temp3",    "I17/A2", "I17/temp1")

pfet(1.00, 2 * 1.00, "6_I17" , "I17/temp4",    "I17/B1", "I17/temp0")                     # Max size: 845.451
pfet(1.00, 2 * 1.00, "5_I17" , "I17/temp1",    "I17/C1", "I17/temp0")                     # Max size: 833.334
nfet(0.65, 0.36, "3_I17" ,      "Vgnd",    "I17/B1", "I17/temp1")                     # Max size: 1438.514
nfet(0.65, 0.36, "0_I17" ,      "Vgnd",    "I17/C1", "I17/temp1")                     # Max size: 1417.897

pfet(1.00, 2 * 1.00, "7_I17" ,       "Vdd", "I17/temp1",     "I17/X")
nfet(0.65, 2 * 0.65, "11_I17",      "Vgnd", "I17/temp1",     "I17/X")
#use_old = False

# timing for     I17/A2: 3.619 4.182 | 2.106 2.139 -1.513 -2.043
# timing for      I17/X: 3.931 4.453 | 2.295 2.295 -1.636 -2.158
# transition for  I17/X: 0.0519 0.0872
# timing for  I17/temp0: 3.693 5.445 | 2.149 3.053 -1.544 -2.392
# timing for  I17/temp1: 3.836 4.314 | 2.231 2.207 -1.605 -2.107
# timing for  I17/temp2:
# timing for  I17/temp3:
# timing for  I17/temp4: 3.661 6.505 | 2.126 3.671 -1.535 -2.834
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a21o, A2=1, B1=0 ===
pfet(1.00, 3.5 * 1.00, "3_I18",       "Vdd",    "I18/A1", "I18/temp0")
pfet(1.00, 0.36, "6_I18",       "Vdd",    "I18/A2", "I18/temp0")                      # Max size: 173.047

nfet(0.65, 20 * 0.65, "5_I18",      "Vgnd",    "I18/A2", "I18/temp1")                      # Max size: 294.435
nfet(0.65, 3.5 * 0.65, "7_I18", "I18/temp1",    "I18/A1", "I18/temp2")

nfet(0.65, 0.36, "0_I18",      "Vgnd",    "I18/B1", "I18/temp2")                      # Max size: 1422.152
pfet(1.00, 3.5 * 1.00, "1_I18", "I18/temp2",    "I18/B1", "I18/temp0")                      # Max size: 835.834

pfet(1.00, 3.5 * 1.00, "2_I18",       "Vdd", "I18/temp2",     "I18/X")
nfet(0.65, 3.5 * 0.65, "4_I18",      "Vgnd", "I18/temp2",     "I18/X")
#use_old = False

# timing for     I18/A1: 3.931 4.453 | 2.295 2.295 -1.636 -2.158
# timing for      I18/X: 4.145 4.657 | 2.433 2.402 -1.712 -2.255
# transition for  I18/X: 0.0363 0.0632
# timing for  I18/temp0: 3.972 5.041 | 2.321 2.653 -1.651 -2.388
# timing for  I18/temp1:
# timing for  I18/temp2: 4.061 4.524 | 2.387 2.339 -1.674 -2.185
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  o21a, A2=1, A1=1 ===
pfet(1.00, 0.36, "0_I19",       "Vdd",    "I19/A1", "I19/temp2")                      # Max size: 365.845
pfet(1.00, 0.36, "6_I19", "I19/temp2",    "I19/A2", "I19/temp1")                      # Max size: 367.333

nfet(0.65, 10 * 0.65, "2_I19",      "Vgnd",    "I19/A1", "I19/temp0")                      # Max size: 622.477
nfet(0.65, 10 * 0.65, "3_I19",      "Vgnd",    "I19/A2", "I19/temp0")                      # Max size: 625.008

pfet(1.00, 4 * 1.00, "5_I19",       "Vdd",    "I19/B1", "I19/temp1")
nfet(0.65, 4 * 0.65, "1_I19", "I19/temp1",    "I19/B1", "I19/temp0")

pfet(1.00, 4 * 1.00, "4_I19",       "Vdd", "I19/temp1",     "I19/X")
nfet(0.65, 4 * 0.65, "7_I19",      "Vgnd", "I19/temp1",     "I19/X")
#use_old = False

# timing for     I19/B1: 4.145 4.657 | 2.433 2.402 -1.712 -2.255
# timing for      I19/X: 4.254 4.779 | 2.497 2.466 -1.757 -2.313
# transition for  I19/X: 0.0149 0.0248
# timing for  I19/temp0:
# timing for  I19/temp1: 4.215 4.711 | 2.476 2.433 -1.739 -2.278
# timing for  I19/temp2:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a21oi, A2=0, A1=1 ===
pfet(1.00, 20 * 1.00, "3_I20",       "Vdd", "I20/A1", "I20/temp1")                         # Max size: 365.845
pfet(1.00, 20 * 1.00, "1_I20",       "Vdd", "I20/A2", "I20/temp1")                         # Max size: 916.998
pfet(1.00, 2 * 1.00, "4_I20", "I20/temp1", "I20/B1",     "I20/Y")

nfet(0.65, 0.36, "0_I20", "I20/temp0", "I20/A1",     "I20/Y")                         # Max size: 622.477
nfet(0.65, 0.36, "5_I20",      "Vgnd", "I20/A2", "I20/temp0")                         # Max size: 1560.25
nfet(0.65, 2 * 0.65, "2_I20",      "Vgnd", "I20/B1",     "I20/Y")
#use_old = False

# timing for     I20/B1: 4.254 4.779 | 2.497 2.466 -1.757 -2.313
# timing for      I20/Y: 4.421 4.831 | 2.573 2.501 -1.848 -2.330
# transition for  I20/Y: 0.0841 0.0321
# timing for  I20/temp0: 4.435 4.844 | 2.590 2.511 -1.845 -2.333
# timing for  I20/temp1:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  xnor2, B=0 ===
pfet(1.00, 10 * 1.00, "0_I21",       "Vdd",     "I21/B", "I21/temp3")         # Max size: 457.153
pfet(1.00, 0.36, "6_I21",       "Vdd",     "I21/B", "I21/temp2")         # Max size: 457.153
pfet(1.00, 3 * 1.00, "1_I21",       "Vdd",     "I21/A", "I21/temp2")

nfet(0.65, 10 * 0.65, "5_I21",      "Vgnd",     "I21/B", "I21/temp1")         # Max size: 777.834
nfet(0.65, 10 * 0.65, "9_I21",      "Vgnd",     "I21/B", "I21/temp0")         # Max size: 777.834
nfet(0.65, 3 * 0.65, "2_I21", "I21/temp2",     "I21/A", "I21/temp1")
nfet(0.65, 3 * 0.65, "3_I21",      "Vgnd",     "I21/A", "I21/temp0")

pfet(1.00, 3 * 1.00, "8_I21", "I21/temp3",     "I21/A",     "I21/Y")

pfet(1.00, 3 * 1.00, "7_I21",       "Vdd", "I21/temp2",     "I21/Y")
nfet(0.65, 3 * 0.65, "4_I21", "I21/temp0", "I21/temp2",     "I21/Y")
#use_old = False

# timing for      I21/A: 4.421 4.831 | 2.573 2.501 -1.848 -2.330
# timing for      I21/Y: 4.510 4.982 | 2.635 2.576 -1.875 -2.406
# transition for  I21/Y: 0.0350 0.0617
# timing for  I21/temp0: 4.436 5.006 | 2.592 2.604 -1.844 -2.402
# timing for  I21/temp2: 2.837 2.834 |
# timing for  I21/temp3: 3.207 |
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a22o, A2=0, B2=1, A1=1 ===
pfet(1.00, 2 * 1.00, "4_I22", "I22/temp1",    "I22/B1", "I22/temp0")
pfet(1.00, 0.36, "8_I22", "I22/temp1",    "I22/B2", "I22/temp0")                      # Max size: 416.588

nfet(0.65, 10 * 0.65, "9_I22",      "Vgnd",    "I22/B2", "I22/temp3")                      # Max size: 708.815
nfet(0.65, 2 * 0.65, "1_I22", "I22/temp3",    "I22/B1", "I22/temp0")

pfet(1.00, 10 * 1.0, "5_I22",       "Vdd",    "I22/A1", "I22/temp1")                      # Max size: 163.039
pfet(1.00, 10 * 1.0, "0_I22",       "Vdd",    "I22/A2", "I22/temp1")                      # Max size: 209.045

nfet(0.65, 0.36, "6_I22", "I22/temp2",    "I22/A1", "I22/temp0")                      # Max size: 277.406
nfet(0.65, 0.36, "2_I22",      "Vgnd",    "I22/A2", "I22/temp2")                      # Max size: 355.685

pfet(1.00, 2 * 1.00, "3_I22",       "Vdd", "I22/temp0",     "I22/X")
nfet(0.65, 2 * 0.65, "7_I22",      "Vgnd", "I22/temp0",     "I22/X")
#use_old = False

# timing for     I22/B1: 4.510 4.982 | 2.635 2.576 -1.875 -2.406
# timing for      I22/X: 4.689 5.131 | 2.722 2.659 -1.967 -2.472
# transition for  I22/X: 0.0255 0.0482
# timing for  I22/temp0: 4.636 5.049 | 2.688 2.607 -1.948 -2.442
# timing for  I22/temp1:
# timing for  I22/temp2: 4.649 5.066 | 2.702 2.616 -1.947 -2.450
# timing for  I22/temp3:
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  a21o, A1=1, B1=0 ===
pfet(1.00, 0.36, "3_I23",       "Vdd",    "I23/A1", "I23/temp0")                      # Max size: 431.381
pfet(1.00, 3 * 1.00, "6_I23",       "Vdd",    "I23/A2", "I23/temp0")

nfet(0.65, 20 * 0.65, "5_I23",      "Vgnd",    "I23/A1", "I23/temp1")                      # Max size: 733.985
nfet(0.65, 3 * 0.65, "7_I23", "I23/temp2",    "I23/A2", "I23/temp1")

pfet(1.00, 3 * 1.00, "1_I23", "I23/temp2",    "I23/B1", "I23/temp0")                      # Max size: 951.233
nfet(0.65, 0.36, "0_I23",      "Vgnd",    "I23/B1", "I23/temp2")                      # Max size: 1618.5

pfet(1.00, 3 * 1.00, "2_I23",       "Vdd", "I23/temp2",     "I23/X")
nfet(0.65, 3 * 0.65, "4_I23",      "Vgnd", "I23/temp2",     "I23/X")
#use_old = False

# timing for     I23/A2: 4.689 5.131 | 2.722 2.659 -1.967 -2.472
# timing for      I23/X: 4.847 5.246 | 2.832 2.728 -2.015 -2.518
# transition for  I23/X: 0.0221 0.0264
# timing for  I23/temp0: 4.719 5.694 | 2.741 3.006 -1.978 -2.688
# timing for  I23/temp1:
# timing for  I23/temp2: 4.802 5.185 | 2.803 2.694 -1.999 -2.491
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613


# ===  and2, A=1 ===
pfet(0.42, 0.36, "3_I24",       "Vdd",     "I24/A", "I24/temp1")                      # Max size: 300.0
pfet(0.42, 3 * 0.42, "0_I24",       "Vdd",     "I24/B", "I24/temp1")

nfet(0.42, 5 * 0.42, "2_I24",      "Vgnd",     "I24/A", "I24/temp0")                      # Max size: 300.0
nfet(0.42, 3 * 0.42, "5_I24", "I24/temp1",     "I24/B", "I24/temp0")

pfet(1.00, 3 * 1.00, "1_I24",       "Vdd", "I24/temp1",     "I24/X")
nfet(0.65, 3 * 0.65, "4_I24",      "Vgnd", "I24/temp1",     "I24/X")
#use_old = False 

# timing for      I24/B: 4.848 5.246 | 2.832 2.728 -2.016 -2.518
# timing for      I24/X: 5.007 5.419 | 2.929 2.806 -2.078 -2.613
# transition for  I24/X: 0.0278 0.0446
# timing for  I24/temp0:
# timing for  I24/temp1: 4.932 5.299 | 2.890 2.757 -2.042 -2.542
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613
# transition for  I25/D: 0.0278 0.0446


# ===  dfxtp ===
pfet(0.42, 0.42, "5_I25" ,       "Vdd",     "I25/D", "I25/temp10")
pfet(1.00, 1.00, "4_I25" ,       "Vdd", "I25/temp1",      "I25/Q")
pfet(0.42, 0.42, "17_I25",       "Vdd", "I25/temp1",  "I25/temp5")
pfet(1.00, 1.00, "7_I25" ,       "Vdd", "I25/temp2",  "I25/temp1")
pfet(0.42, 0.42, "2_I25" , "I25/temp6", "I25/temp3",  "I25/temp4")
pfet(0.42, 0.42, "15_I25", "I25/temp8", "I25/temp3",  "I25/temp2")
pfet(0.64, 0.64, "19_I25",       "Vdd", "I25/temp3",  "I25/temp9")
pfet(0.75, 0.75, "11_I25",       "Vdd", "I25/temp6",  "I25/temp8")
pfet(0.42, 0.42, "9_I25" ,       "Vdd", "I25/temp8",  "I25/temp4")
pfet(0.42, 0.42, "8_I25" , "I25/temp6", "I25/temp9", "I25/temp10")
pfet(0.42, 0.42, "12_I25", "I25/temp5", "I25/temp9",  "I25/temp2")
pfet(0.64, 0.64, "3_I25" ,       "Vdd",       "clk",  "I25/temp3")
nfet(0.42, 0.42, "22_I25",      "Vgnd",     "I25/D", "I25/temp10")
nfet(0.65, 0.65, "0_I25" ,      "Vgnd", "I25/temp1",      "I25/Q")
nfet(0.42, 0.42, "13_I25",      "Vgnd", "I25/temp1",  "I25/temp0")
nfet(0.65, 0.65, "21_I25",      "Vgnd", "I25/temp2",  "I25/temp1")
nfet(0.42, 0.42, "14_I25",      "Vgnd", "I25/temp3",  "I25/temp9")
nfet(0.36, 0.36, "18_I25", "I25/temp2", "I25/temp3",  "I25/temp0")
nfet(0.36, 0.36, "20_I25", "I25/temp6", "I25/temp3", "I25/temp10")
nfet(0.64, 0.64, "10_I25",      "Vgnd", "I25/temp6",  "I25/temp8")
nfet(0.42, 0.42, "6_I25" ,      "Vgnd", "I25/temp8",  "I25/temp7")
nfet(0.36, 0.36, "1_I25" , "I25/temp8", "I25/temp9",  "I25/temp2")
nfet(0.36, 0.36, "16_I25", "I25/temp7", "I25/temp9",  "I25/temp6")
nfet(0.42, 0.42, "23_I25",      "Vgnd",       "clk",  "I25/temp3")
# timing for      I25/D: 5.008 5.419 | 2.929 2.806 -2.079 -2.613

print(total_size_old, total_size, total_size / total_size_old)

plotline = None

for i,line in enumerate(spice):
    if len(line) == 0:
        continue
    if line.startswith("plot "):
        plotline = i
    if line[0] != 'X':
        continue
    name = line.split()[0][1:]
    if name in fets:
        spice[i] = fets[name]

spice[plotline] = ""

for name in timings_to_track:
    spice.insert(plotline+1, f"meas tran fall_{name} when V({name}) = {1.8 * 0.5}")
    spice.insert(plotline+1, f"meas tran fall_start_{name} when V({name}) = {1.8 * 0.2}")
    spice.insert(plotline+1, f"meas tran fall_end_{name} when V({name}) = {1.8 * 0.8}")
spice.insert(plotline+1,"run")
spice.insert(plotline+1,"reset")
spice.insert(plotline+1, "alterparam v_start=0")
spice.insert(plotline+1, "alterparam v_q_ic=1.8")

for name in timings_to_track:
    spice.insert(plotline+1, f"meas tran rise_{name} when V({name}) = {1.8 * 0.5}")
    spice.insert(plotline+1, f"meas tran rise_start_{name} when V({name}) = {1.8 * 0.2}")
    spice.insert(plotline+1, f"meas tran rise_end_{name} when V({name}) = {1.8 * 0.8}")
spice.insert(plotline+1, "run")
spice.insert(plotline+1, "alterparam v_start=1.8")
spice.insert(plotline+1, "alterparam v_q_ic=0")

spice.insert(0, "* Generated by python_spice")

spice = "\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
