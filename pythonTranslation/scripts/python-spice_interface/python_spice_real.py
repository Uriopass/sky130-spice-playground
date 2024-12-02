
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

def find_bin(bins, W):
    bestbin = bins[0]
    binscore = 1
    for bin in bins:
        mult = W / bin
        score = abs(mult - round(mult))
        if score <= binscore:
            bestbin = bin
            binscore = score

    return bestbin, W / bestbin

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)
    
    closest_bin, mult = find_bin(bins_pfet, W)

    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)
    
    closest_bin, mult = find_bin(bins_nfet, W)
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

with open("../../libs/ngspice/out.spice", 'r') as f:
    spice = f.read()

spice = spice.split('\n')

to_clear = ['2_I1', '4_I1', '6_I1', '7_I1', '8_I1', '9_I1', '1_I2', '2_I2', '3_I2', '5_I2', '6_I2', '7_I2', '11_I4', '13_I4', '12_I8', '13_I8', '8_I9', '11_I9', '12_I9', '13_I9', '14_I9', '15_I9', '16_I9', '17_I9', '18_I9', '19_I9', '6_I11', '8_I11', '9_I11', '11_I11', '6_I14', '8_I14', '9_I14', '11_I14']
for name in to_clear: fets[name] = ''

# ===  dfxtp ===
pfet(0.42, "5_I0" ,      "Vdd",     "I0/D", "I0/temp10")
pfet(1.00, "4_I0" ,      "Vdd", "I0/temp1",      "I0/Q")
pfet(0.42, "17_I0",      "Vdd", "I0/temp1",  "I0/temp5")
pfet(1.00, "7_I0" ,      "Vdd", "I0/temp2",  "I0/temp1")
pfet(0.42, "2_I0" , "I0/temp6", "I0/temp3",  "I0/temp4")
pfet(0.42, "15_I0", "I0/temp8", "I0/temp3",  "I0/temp2")
pfet(0.64, "19_I0",      "Vdd", "I0/temp3",  "I0/temp9")
pfet(0.75, "11_I0",      "Vdd", "I0/temp6",  "I0/temp8")
pfet(0.42, "9_I0" ,      "Vdd", "I0/temp8",  "I0/temp4")
pfet(0.42, "8_I0" , "I0/temp6", "I0/temp9", "I0/temp10")
pfet(0.42, "12_I0", "I0/temp5", "I0/temp9",  "I0/temp2")
pfet(0.64, "3_I0" ,      "Vdd",      "clk",  "I0/temp3")
nfet(0.42, "22_I0",     "Vgnd",     "I0/D", "I0/temp10")
nfet(0.65, "0_I0" ,     "Vgnd", "I0/temp1",      "I0/Q")
nfet(0.42, "13_I0",     "Vgnd", "I0/temp1",  "I0/temp0")
nfet(0.65, "21_I0",     "Vgnd", "I0/temp2",  "I0/temp1")
nfet(0.42, "14_I0",     "Vgnd", "I0/temp3",  "I0/temp9")
nfet(0.36, "18_I0", "I0/temp2", "I0/temp3",  "I0/temp0")
nfet(0.36, "20_I0", "I0/temp6", "I0/temp3", "I0/temp10")
nfet(0.64, "10_I0",     "Vgnd", "I0/temp6",  "I0/temp8")
nfet(0.42, "6_I0" ,     "Vgnd", "I0/temp8",  "I0/temp7")
nfet(0.36, "1_I0" , "I0/temp8", "I0/temp9",  "I0/temp2")
nfet(0.36, "16_I0", "I0/temp7", "I0/temp9",  "I0/temp6")
nfet(0.42, "23_I0",     "Vgnd",      "clk",  "I0/temp3")
# timing for       I0/D:
# timing for       I0/Q: 0.038 0.423 | 0.074 0.438 +0.036 +0.015
# timing for        clk: 0.100 0.100 | 0.100 0.100


# ===  clkbuf ===
pfet(4.0 * 1.00, "0_I1",  "Vdd",     "I1/A", "I1/temp0")
nfet(4.0 * 0.42, "5_I1", "Vgnd",     "I1/A", "I1/temp0")
pfet(4.0 * 4.00, "3_I1",  "Vdd", "I1/temp0",     "I1/X")
nfet(4.0 * 1.68, "1_I1", "Vgnd", "I1/temp0",     "I1/X")
# timing for       I1/A: 0.038 0.423 | 0.074 0.438 +0.036 +0.015
# timing for       I1/X: 0.211 0.590 | 0.204 0.567 -0.007 -0.023
# timing for       I1/temp0: 0.110 0.510 | 0.149 0.525 +0.039 +0.015
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  buf ===
pfet(4.0 * 1.00, "8_I2",  "Vdd",     "I2/A", "I2/temp0")
nfet(4.0 * 0.65, "9_I2", "Vgnd",     "I2/A", "I2/temp0")
pfet(4.0 * 4.00, "0_I2",  "Vdd", "I2/temp0",     "I2/X")
nfet(4.0 * 2.60, "4_I2", "Vgnd", "I2/temp0",     "I2/X")
# timing for       I2/A: 0.212 0.591 | 0.206 0.568 -0.006 -0.023
# timing for   I2/temp0: 0.276 0.701 | 0.249 0.652 -0.027 -0.049
# timing for       I2/X: 0.406 0.787 | 0.303 0.694 -0.103 -0.093
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  mux2, A0=1, A1=0 ===

pfet(0.42, "1_I3" ,      "Vdd",     "I3/S", "I3/s_neg")
nfet(0.42, "5_I3" ,     "Vgnd",     "I3/S", "I3/s_neg")
pfet(0.42, "0_I3" ,      "Vdd", "I3/s_neg", "I3/temp3")
nfet(0.42, "3_I3" ,     "Vgnd", "I3/s_neg", "I3/temp0")

pfet(0.42, "7_I3" , "I3/temp3",    "I3/A1", "I3/inv")                         # Max size: 406.743
nfet(0.42, "9_I3" ,     "Vgnd",     "I3/S", "I3/temp2")
nfet(0.42, "8_I3" , "I3/temp2",    "I3/A1", "I3/inv")                         # Max size: 692.063

pfet(0.42, "2_I3" ,      "Vdd",     "I3/S", "I3/temp4")
pfet(0.42, "4_I3" , "I3/temp4",    "I3/A0", "I3/inv")                         # Max size: 155.188
nfet(0.42, "6_I3" , "I3/temp0",    "I3/A0", "I3/inv")                         # Max size: 264.048

pfet(1.00, "10_I3",      "Vdd", "I3/inv",     "I3/X")
nfet(0.65, "11_I3",     "Vgnd", "I3/inv",     "I3/X")
# timing for       I3/S: 0.408 0.789 | 0.305 0.696 -0.103 -0.093
# timing for       I3/X: 0.748 1.034 | 0.576 0.883 -0.172 -0.151
# timing for   I3/temp0: 0.684 0.883 | 0.521 0.752 -0.163 -0.131
# timing for   I3/inv: 0.661 0.936 | 0.498 0.792 -0.163 -0.144
# timing for   I3/temp2:
# timing for   I3/temp3: 0.479 1.220 | 0.344 1.077 -0.135 -0.143
# timing for   I3/temp4:
# timing for   I3/s_neg: 0.456 0.872 | 0.329 0.742 -0.127 -0.130
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  mux2, S=0, A1=1 ===
pfet(0.64, "1_I4" , "I4/temp5",    "I4/A0", "I4/temp0")
pfet(0.64, "3_I4" , "I4/temp5",    "I4/A1", "I4/temp2")                         # Max size: 185.518
pfet(0.64, "0_I4" ,      "Vdd",     "I4/S", "I4/temp0")                         # Max size: 195.958
pfet(0.64, "12_I4",      "Vdd",     "I4/S", "I4/temp4")                         # Max size: 195.958
pfet(0.64, "6_I4" ,      "Vdd", "I4/temp4", "I4/temp2")
pfet(2.00, "2_I4" ,      "Vdd", "I4/temp5",     "I4/X")
nfet(0.42, "7_I4" , "I4/temp5",    "I4/A0", "I4/temp1")
nfet(0.42, "10_I4", "I4/temp5",    "I4/A1", "I4/temp3")                         # Max size: 315.654
nfet(0.42, "5_I4" ,     "Vgnd",     "I4/S", "I4/temp3")                         # Max size: 333.418
nfet(0.42, "9_I4" ,     "Vgnd",     "I4/S", "I4/temp4")                         # Max size: 333.418
nfet(0.42, "8_I4" ,     "Vgnd", "I4/temp4", "I4/temp1")
nfet(1.30, "4_I4" ,     "Vgnd", "I4/temp5",     "I4/X")
# timing for      I4/A0: 0.748 1.034 | 0.576 0.883 -0.172 -0.151
# timing for       I4/X: 1.085 1.316 | 0.909 1.164 -0.176 -0.152
# timing for   I4/temp0:
# timing for   I4/temp1:
# timing for   I4/temp2:
# timing for   I4/temp3: 0.975 1.149 | 0.800 0.998 -0.175 -0.151
# timing for   I4/temp4:
# timing for   I4/temp5: 0.952 1.127 | 0.777 0.976 -0.175 -0.151
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  xor2, A=0 ===
pfet(1.00, "7_I5",      "Vdd",     "I5/A", "I5/temp2")                          # Max size: 494.061
pfet(1.00, "8_I5",      "Vdd",     "I5/A", "I5/temp0")                          # Max size: 494.061
pfet(1.00, "3_I5", "I5/temp3",     "I5/B", "I5/temp0")
pfet(1.00, "4_I5",      "Vdd",     "I5/B", "I5/temp2")
pfet(1.00, "0_I5", "I5/temp2", "I5/temp3",     "I5/X")
nfet(0.65, "5_I5",     "Vgnd",     "I5/A", "I5/temp3")                          # Max size: 840.633
nfet(0.65, "9_I5",     "Vgnd",     "I5/A", "I5/temp1")                          # Max size: 840.633
nfet(0.65, "1_I5", "I5/temp1",     "I5/B",     "I5/X")
nfet(0.65, "2_I5",     "Vgnd",     "I5/B", "I5/temp3")
nfet(0.65, "6_I5",     "Vgnd", "I5/temp3",     "I5/X")
# timing for       I5/B: 1.086 1.317 | 0.911 1.166 -0.175 -0.151
# timing for       I5/X: 1.293 1.627 | 1.117 1.476 -0.176 -0.151
# timing for   I5/temp0:
# timing for   I5/temp1: 1.647 | 1.496
# timing for   I5/temp2:
# timing for   I5/temp3: 1.205 1.370 | 1.030 1.219 -0.175 -0.151
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21o, A1=1, B1=0 ===
pfet(1.00, "3_I6",      "Vdd",    "I6/A1", "I6/temp0")                          # Max size: 103.535
pfet(1.00, "6_I6",      "Vdd",    "I6/A2", "I6/temp0")
pfet(1.00, "1_I6", "I6/temp2",    "I6/B1", "I6/temp0")                          # Max size: 359.621
pfet(1.00, "2_I6",      "Vdd", "I6/temp2",     "I6/X")
nfet(0.65, "7_I6", "I6/temp2",    "I6/A1", "I6/temp1")                          # Max size: 176.163
nfet(0.65, "5_I6",     "Vgnd",    "I6/A2", "I6/temp1")
nfet(0.65, "0_I6",     "Vgnd",    "I6/B1", "I6/temp2")                          # Max size: 611.887
nfet(0.65, "4_I6",     "Vgnd", "I6/temp2",     "I6/X")
# timing for      I6/A2: 1.293 1.628 | 1.118 1.477 -0.175 -0.151
# timing for       I6/X: 1.543 1.897 | 1.367 1.746 -0.176 -0.151
# timing for   I6/temp0: 1.333 2.289 | 1.158 2.138 -0.175 -0.151
# timing for   I6/temp1: 1.453 1.623 | 1.277 1.472 -0.176 -0.151
# timing for   I6/temp2: 1.440 1.727 | 1.265 1.576 -0.175 -0.151
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a211o, C1=0, A1=1, B1=0 ===
pfet(1.00, "6_I7",      "Vdd",    "I7/A1", "I7/temp3")                          # Max size: 61.726
pfet(1.00, "2_I7",      "Vdd",    "I7/A2", "I7/temp3")
pfet(1.00, "8_I7", "I7/temp3",    "I7/B1", "I7/temp1")                          # Max size: 393.087
pfet(1.00, "1_I7", "I7/temp2",    "I7/C1", "I7/temp1")                          # Max size: 307.884
pfet(1.00, "0_I7",      "Vdd", "I7/temp2",     "I7/X")
nfet(0.65, "7_I7", "I7/temp2",    "I7/A1", "I7/temp0")                          # Max size: 105.026
nfet(0.65, "5_I7",     "Vgnd",    "I7/A2", "I7/temp0")
nfet(0.65, "3_I7",     "Vgnd",    "I7/B1", "I7/temp2")                          # Max size: 668.828
nfet(0.65, "9_I7",     "Vgnd",    "I7/C1", "I7/temp2")                          # Max size: 523.858
nfet(0.65, "4_I7",     "Vgnd", "I7/temp2",     "I7/X")
# timing for      I7/A2: 1.543 1.898 | 1.368 1.746 -0.175 -0.152
# timing for       I7/X: 1.897 2.133 | 1.722 1.982 -0.175 -0.151
# timing for   I7/temp0: 1.800 1.904 | 1.625 1.753 -0.175 -0.151
# timing for   I7/temp1: 1.616 2.990 | 1.441 2.839 -0.175 -0.151
# timing for   I7/temp2: 1.789 1.993 | 1.613 1.842 -0.176 -0.151
# timing for   I7/temp3: 1.584 3.837 | 1.409 3.685 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a311o, C1=0, A1=1, A2=1, B1=0 ===
pfet(1.00, "7_I8" ,      "Vdd",    "I8/A1", "I8/temp0")                         # Max size: 147.006
pfet(1.00, "1_I8" ,      "Vdd",    "I8/A2", "I8/temp0")                         # Max size: 77.015
pfet(1.00, "9_I8" ,      "Vdd",    "I8/A3", "I8/temp0")
pfet(1.00, "11_I8", "I8/temp3",    "I8/B1", "I8/temp0")                         # Max size: 450.017
pfet(1.00, "0_I8" , "I8/temp3",    "I8/C1", "I8/temp2")                         # Max size: 376.739
pfet(2.00, "6_I8" ,      "Vdd", "I8/temp2",     "I8/X")
nfet(0.65, "4_I8" , "I8/temp2",    "I8/A1", "I8/temp1")                         # Max size: 250.127
nfet(0.65, "3_I8" , "I8/temp4",    "I8/A2", "I8/temp1")                         # Max size: 131.04
nfet(0.65, "5_I8" ,     "Vgnd",    "I8/A3", "I8/temp4")
nfet(0.65, "2_I8" ,     "Vgnd",    "I8/B1", "I8/temp2")                         # Max size: 765.693
nfet(0.65, "10_I8",     "Vgnd",    "I8/C1", "I8/temp2")                         # Max size: 641.012
nfet(1.30, "8_I8" ,     "Vgnd", "I8/temp2",     "I8/X")
# timing for      I8/A3: 1.897 2.133 | 1.722 1.982 -0.175 -0.151
# timing for       I8/X: 2.335 2.389 | 2.159 2.237 -0.176 -0.152
# timing for   I8/temp0: 1.941 4.420 | 1.766 4.269 -0.175 -0.151
# timing for   I8/temp1: 2.262 2.158 | 2.086 2.006 -0.176 -0.152
# timing for   I8/temp2: 2.228 2.254 | 2.053 2.102 -0.175 -0.152
# timing for   I8/temp3: 1.974 3.370 | 1.799 3.219 -0.175 -0.151
# timing for   I8/temp4: 2.277 2.141 | 2.102 1.990 -0.175 -0.151
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a221oi, B2=1, C1=0, A1=1, B1=0 ===
pfet(2.00, "6_I9" ,      "Vdd", "I9/A1", "I9/temp1")                            # Max size: 174.774
pfet(2.00, "2_I9" ,      "Vdd", "I9/A2", "I9/temp1")
pfet(2.00, "1_I9" , "I9/temp1", "I9/B1", "I9/temp0")                            # Max size: 471.366
pfet(2.00, "5_I9" , "I9/temp1", "I9/B2", "I9/temp0")                            # Max size: 190.889
pfet(2.00, "9_I9" , "I9/temp0", "I9/C1",     "I9/Y")                            # Max size: 469.058
nfet(1.30, "4_I9" , "I9/temp2", "I9/A1",     "I9/Y")                            # Max size: 297.374
nfet(1.30, "7_I9" ,     "Vgnd", "I9/A2", "I9/temp2")
nfet(1.30, "0_I9" , "I9/temp3", "I9/B1",     "I9/Y")                            # Max size: 802.018
nfet(1.30, "3_I9" ,     "Vgnd", "I9/B2", "I9/temp3")                            # Max size: 324.794
nfet(1.30, "10_I9",     "Vgnd", "I9/C1",     "I9/Y")                            # Max size: 798.091
# timing for      I9/A2: 2.335 2.390 | 2.160 2.238 -0.175 -0.152
# timing for       I9/Y: 2.619 2.480 | 2.444 2.328 -0.175 -0.152
# timing for   I9/temp0: 2.418 3.908 | 2.243 3.757 -0.175 -0.151
# timing for   I9/temp1: 2.381 5.339 | 2.206 5.188 -0.175 -0.151
# timing for   I9/temp2: 2.633 2.401 | 2.458 2.250 -0.175 -0.151
# timing for   I9/temp3:
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152

# ===  or4, D=0, C=0, B=0 ===
pfet(0.42, "3_I10",       "Vdd",     "I10/A", "I10/temp3")
pfet(0.42, "2_I10", "I10/temp3",     "I10/B", "I10/temp1")                      # Max size: 230.202
pfet(0.42, "5_I10", "I10/temp2",     "I10/C", "I10/temp1")                      # Max size: 221.739
pfet(0.42, "8_I10", "I10/temp2",     "I10/D", "I10/temp0")                      # Max size: 157.955
pfet(1.00, "6_I10",       "Vdd", "I10/temp0",     "I10/X")
nfet(0.42, "9_I10",      "Vgnd",     "I10/A", "I10/temp0")
nfet(0.42, "0_I10",      "Vgnd",     "I10/B", "I10/temp0")                      # Max size: 391.682
nfet(0.42, "7_I10",      "Vgnd",     "I10/C", "I10/temp0")                      # Max size: 377.283
nfet(0.42, "1_I10",      "Vgnd",     "I10/D", "I10/temp0")                      # Max size: 268.757
nfet(0.65, "4_I10",      "Vgnd", "I10/temp0",     "I10/X")
# timing for      I10/A: 2.619 2.480 | 2.444 2.328 -0.175 -0.152
# timing for      I10/X: 2.829 3.079 | 2.654 2.927 -0.175 -0.152
# timing for  I10/temp0: 2.710 2.949 | 2.535 2.797 -0.175 -0.152
# timing for  I10/temp1: 4.863 2.533 | 4.687 2.382 -0.176 -0.151
# timing for  I10/temp2: 3.968 2.567 | 3.793 2.416 -0.175 -0.151
# timing for  I10/temp3: 5.216 2.507 | 5.041 2.356 -0.175 -0.151
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21oi, A2=1, B1=0 ===
pfet(2.00, "5_I11" ,       "Vdd", "I11/A1", "I11/temp2")
pfet(2.00, "7_I11" ,       "Vdd", "I11/A2", "I11/temp2")                        # Max size: 194.113
pfet(2.00, "4_I11" , "I11/temp2", "I11/B1",     "I11/Y")                        # Max size: 264.148
nfet(0.65, "2_I11" , "I11/temp1", "I11/A1",     "I11/Y")
nfet(0.65, "10_I11", "I11/temp0", "I11/A1",     "I11/Y")
nfet(0.65, "0_I11" ,      "Vgnd", "I11/A2", "I11/temp0")                        # Max size: 330.278
nfet(0.65, "3_I11" ,      "Vgnd", "I11/A2", "I11/temp1")                        # Max size: 330.278
nfet(1.30, "1_I11" ,      "Vgnd", "I11/B1",     "I11/Y")                        # Max size: 449.442
# timing for     I11/A1: 2.829 3.079 | 2.654 2.927 -0.175 -0.152
# timing for      I11/Y: 2.936 3.316 | 2.761 3.164 -0.175 -0.152
# timing for  I11/temp0:
# timing for  I11/temp1:
# timing for  I11/temp2: 3.482 3.129 | 3.306 2.976 -0.176 -0.153
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  o211a, A2=0, C1=1, B1=1 ===
pfet(1.00, "5_I12",       "Vdd",    "I12/A1", "I12/temp0")
pfet(1.00, "4_I12", "I12/temp2",    "I12/A2", "I12/temp0")                      # Max size: 327.425
pfet(1.00, "3_I12",       "Vdd",    "I12/B1", "I12/temp2")                      # Max size: 129.204
pfet(1.00, "2_I12",       "Vdd",    "I12/C1", "I12/temp2")                      # Max size: 259.979
pfet(1.00, "7_I12",       "Vdd", "I12/temp2",     "I12/X")
nfet(0.65, "0_I12",      "Vgnd",    "I12/A1", "I12/temp3")
nfet(0.65, "9_I12",      "Vgnd",    "I12/A2", "I12/temp3")                      # Max size: 557.106
nfet(0.65, "1_I12", "I12/temp3",    "I12/B1", "I12/temp1")                      # Max size: 219.838
nfet(0.65, "6_I12", "I12/temp2",    "I12/C1", "I12/temp1")                      # Max size: 442.348
nfet(0.65, "8_I12",      "Vgnd", "I12/temp2",     "I12/X")
# timing for     I12/A1: 2.937 3.317 | 2.761 3.165 -0.176 -0.152
# timing for      I12/X: 3.230 3.606 | 3.055 3.454 -0.175 -0.152
# timing for  I12/temp0: 2.970 3.764 | 2.795 3.612 -0.175 -0.152
# timing for  I12/temp1: 3.158 3.351 | 2.983 3.198 -0.175 -0.153
# timing for  I12/temp2: 3.119 3.429 | 2.944 3.277 -0.175 -0.152
# timing for  I12/temp3: 3.179 3.330 | 3.004 3.178 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a41o, A3=1, A4=1, A2=1, B1=0 ===
pfet(1.00, "5_I13" ,       "Vdd",    "I13/A1", "I13/temp0")
pfet(1.00, "3_I13" ,       "Vdd",    "I13/A2", "I13/temp0")                     # Max size: 290.888
pfet(1.00, "2_I13" ,       "Vdd",    "I13/A3", "I13/temp0")                     # Max size: 227.5
pfet(1.00, "4_I13" ,       "Vdd",    "I13/A4", "I13/temp0")                     # Max size: 217.087
pfet(1.00, "7_I13" , "I13/temp3",    "I13/B1", "I13/temp0")                     # Max size: 606.575
pfet(1.00, "8_I13" ,       "Vdd", "I13/temp3",     "I13/X")
nfet(0.65, "6_I13" , "I13/temp3",    "I13/A1", "I13/temp2")
nfet(0.65, "0_I13" , "I13/temp2",    "I13/A2", "I13/temp1")                     # Max size: 494.939
nfet(0.65, "11_I13", "I13/temp4",    "I13/A3", "I13/temp1")                     # Max size: 387.086
nfet(0.65, "1_I13" ,      "Vgnd",    "I13/A4", "I13/temp4")                     # Max size: 369.369
nfet(0.65, "9_I13" ,      "Vgnd",    "I13/B1", "I13/temp3")                     # Max size: 1032.073
nfet(0.65, "10_I13",      "Vgnd", "I13/temp3",     "I13/X")
# timing for     I13/A1: 3.231 3.607 | 3.056 3.454 -0.175 -0.153
# timing for      I13/X: 3.468 3.891 | 3.293 3.739 -0.175 -0.152
# timing for  I13/temp0: 3.282 4.469 | 3.107 4.317 -0.175 -0.152
# timing for  I13/temp1:
# timing for  I13/temp2:
# timing for  I13/temp3: 3.376 3.721 | 3.201 3.569 -0.175 -0.152
# timing for  I13/temp4:
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21oi, A2=1, B1=0 ===
pfet(2.00, "5_I14" ,       "Vdd", "I14/A1", "I14/temp2")
pfet(2.00, "7_I14" ,       "Vdd", "I14/A2", "I14/temp2")                        # Max size: 236.756
pfet(2.00, "4_I14" , "I14/temp2", "I14/B1",     "I14/Y")                        # Max size: 726.398
nfet(0.65, "2_I14" , "I14/temp1", "I14/A1",     "I14/Y")
nfet(0.65, "10_I14", "I14/temp0", "I14/A1",     "I14/Y")
nfet(0.65, "0_I14" ,      "Vgnd", "I14/A2", "I14/temp0")                        # Max size: 402.835
nfet(0.65, "3_I14" ,      "Vgnd", "I14/A2", "I14/temp1")                        # Max size: 402.835
nfet(1.30, "1_I14" ,      "Vgnd", "I14/B1",     "I14/Y")                        # Max size: 1235.948
# timing for     I14/A1: 3.468 3.891 | 3.293 3.739 -0.175 -0.152
# timing for      I14/Y: 3.632 3.990 | 3.457 3.838 -0.175 -0.152
# timing for  I14/temp0:
# timing for  I14/temp1:
# timing for  I14/temp2: 3.508 4.557 | 3.333 4.405 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  nand2b, B=1 ===
pfet(0.42, "5_I15",       "Vdd",   "I15/A_N", "I15/temp1")
pfet(1.00, "4_I15",       "Vdd",     "I15/B",     "I15/Y")                      # Max size: 283.037
pfet(1.00, "3_I15",       "Vdd", "I15/temp1",     "I15/Y")
nfet(0.42, "0_I15",      "Vgnd",   "I15/A_N", "I15/temp1")
nfet(0.65, "2_I15",      "Vgnd",     "I15/B", "I15/temp0")                      # Max size: 481.58
nfet(0.65, "1_I15", "I15/temp0", "I15/temp1",     "I15/Y")
# timing for    I15/A_N: 3.632 3.990 | 3.457 3.838 -0.175 -0.152
# timing for      I15/Y: 3.822 4.192 | 3.647 4.040 -0.175 -0.152
# timing for  I15/temp0:
# timing for  I15/temp1: 3.687 4.085 | 3.512 3.933 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  nor2, B=0 ===
pfet(1.00, "0_I16",       "Vdd", "I16/A", "I16/temp0")
pfet(1.00, "2_I16", "I16/temp0", "I16/B",     "I16/Y")                          # Max size: 352.332
nfet(0.65, "1_I16",      "Vgnd", "I16/A",     "I16/Y")
nfet(0.65, "3_I16",      "Vgnd", "I16/B",     "I16/Y")                          # Max size: 599.484
# timing for      I16/A: 3.822 4.192 | 3.647 4.040 -0.175 -0.152
# timing for      I16/Y: 3.930 4.476 | 3.755 4.324 -0.175 -0.152
# timing for  I16/temp0: 4.242 4.230 | 4.067 4.078 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a311o, A3=1, C1=0, A1=1, B1=0 ===
pfet(1.00, "10_I17",       "Vdd",    "I17/A1", "I17/temp4")                     # Max size: 303.532
pfet(1.00, "9_I17" ,       "Vdd",    "I17/A2", "I17/temp4")
pfet(1.00, "8_I17" ,       "Vdd",    "I17/A3", "I17/temp4")                     # Max size: 300.392
pfet(1.00, "6_I17" , "I17/temp4",    "I17/B1", "I17/temp0")                     # Max size: 845.451
pfet(1.00, "5_I17" , "I17/temp1",    "I17/C1", "I17/temp0")                     # Max size: 833.334
pfet(1.00, "7_I17" ,       "Vdd", "I17/temp1",     "I17/X")
nfet(0.65, "4_I17" , "I17/temp3",    "I17/A1", "I17/temp1")                     # Max size: 516.453
nfet(0.65, "2_I17" , "I17/temp3",    "I17/A2", "I17/temp2")
nfet(0.65, "1_I17" ,      "Vgnd",    "I17/A3", "I17/temp2")                     # Max size: 511.109
nfet(0.65, "3_I17" ,      "Vgnd",    "I17/B1", "I17/temp1")                     # Max size: 1438.514
nfet(0.65, "0_I17" ,      "Vgnd",    "I17/C1", "I17/temp1")                     # Max size: 1417.897
nfet(0.65, "11_I17",      "Vgnd", "I17/temp1",     "I17/X")
# timing for     I17/A2: 3.930 4.476 | 3.755 4.324 -0.175 -0.152
# timing for      I17/X: 4.275 4.750 | 4.100 4.597 -0.175 -0.153
# timing for  I17/temp0: 4.004 5.747 | 3.829 5.595 -0.175 -0.152
# timing for  I17/temp1: 4.177 4.612 | 4.002 4.459 -0.175 -0.153
# timing for  I17/temp2:
# timing for  I17/temp3: 4.192 4.480 | 4.017 4.327 -0.175 -0.153
# timing for  I17/temp4: 3.972 6.807 | 3.797 6.655 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21o, A2=1, B1=0 ===
pfet(1.00, "3_I18",       "Vdd",    "I18/A1", "I18/temp0")
pfet(1.00, "6_I18",       "Vdd",    "I18/A2", "I18/temp0")                      # Max size: 173.047
pfet(1.00, "1_I18", "I18/temp2",    "I18/B1", "I18/temp0")                      # Max size: 835.834
pfet(1.00, "2_I18",       "Vdd", "I18/temp2",     "I18/X")
nfet(0.65, "7_I18", "I18/temp2",    "I18/A1", "I18/temp1")
nfet(0.65, "5_I18",      "Vgnd",    "I18/A2", "I18/temp1")                      # Max size: 294.435
nfet(0.65, "0_I18",      "Vgnd",    "I18/B1", "I18/temp2")                      # Max size: 1422.152
nfet(0.65, "4_I18",      "Vgnd", "I18/temp2",     "I18/X")
# timing for     I18/A1: 4.275 4.750 | 4.100 4.597 -0.175 -0.153
# timing for      I18/X: 4.490 4.953 | 4.315 4.801 -0.175 -0.152
# timing for  I18/temp0: 4.317 5.338 | 4.142 5.186 -0.175 -0.152
# timing for  I18/temp1:
# timing for  I18/temp2: 4.405 4.821 | 4.230 4.669 -0.175 -0.152
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  o21a, A2=1, A1=1 ===
pfet(1.00, "0_I19",       "Vdd",    "I19/A1", "I19/temp2")                      # Max size: 365.845
pfet(1.00, "6_I19", "I19/temp2",    "I19/A2", "I19/temp1")                      # Max size: 367.333
pfet(1.00, "5_I19",       "Vdd",    "I19/B1", "I19/temp1")
pfet(1.00, "4_I19",       "Vdd", "I19/temp1",     "I19/X")
nfet(0.65, "2_I19",      "Vgnd",    "I19/A1", "I19/temp0")                      # Max size: 622.477
nfet(0.65, "3_I19",      "Vgnd",    "I19/A2", "I19/temp0")                      # Max size: 625.008
nfet(0.65, "1_I19", "I19/temp1",    "I19/B1", "I19/temp0")
nfet(0.65, "7_I19",      "Vgnd", "I19/temp1",     "I19/X")
# timing for     I19/B1: 4.490 4.954 | 4.315 4.801 -0.175 -0.153
# timing for      I19/X: 4.599 5.076 | 4.424 4.923 -0.175 -0.153
# timing for  I19/temp0:
# timing for  I19/temp1: 4.560 5.008 | 4.385 4.855 -0.175 -0.153
# timing for  I19/temp2:
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21oi, A2=0, A1=1 ===
pfet(1.00, "3_I20",       "Vdd", "I20/A1", "I20/temp1")                         # Max size: 365.845
pfet(1.00, "1_I20",       "Vdd", "I20/A2", "I20/temp1")                         # Max size: 916.998
pfet(1.00, "4_I20", "I20/temp1", "I20/B1",     "I20/Y")
nfet(0.65, "0_I20", "I20/temp0", "I20/A1",     "I20/Y")                         # Max size: 622.477
nfet(0.65, "5_I20",      "Vgnd", "I20/A2", "I20/temp0")                         # Max size: 1560.25
nfet(0.65, "2_I20",      "Vgnd", "I20/B1",     "I20/Y")
# timing for     I20/B1: 4.599 5.076 | 4.424 4.924 -0.175 -0.152
# timing for      I20/Y: 4.767 5.129 | 4.593 4.977 -0.174 -0.152
# timing for  I20/temp0: 4.782 5.143 | 4.607 4.991 -0.175 -0.152
# timing for  I20/temp1:
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  xnor2, B=0 ===
pfet(1.00, "0_I21",       "Vdd",     "I21/A", "I21/temp3")
pfet(1.00, "6_I21",       "Vdd",     "I21/A", "I21/temp2")
pfet(1.00, "1_I21",       "Vdd",     "I21/B", "I21/temp2")                      # Max size: 457.153
pfet(1.00, "8_I21", "I21/temp3",     "I21/B",     "I21/Y")                      # Max size: 457.153
pfet(1.00, "7_I21",       "Vdd", "I21/temp2",     "I21/Y")
nfet(0.65, "5_I21",      "Vgnd",     "I21/A", "I21/temp1")
nfet(0.65, "9_I21",      "Vgnd",     "I21/A", "I21/temp0")
nfet(0.65, "2_I21", "I21/temp2",     "I21/B", "I21/temp1")                      # Max size: 777.834
nfet(0.65, "3_I21",      "Vgnd",     "I21/B", "I21/temp0")                      # Max size: 777.834
nfet(0.65, "4_I21", "I21/temp0", "I21/temp2",     "I21/Y")
# timing for      I21/A: 4.768 5.129 | 4.593 4.977 -0.175 -0.152
# timing for      I21/Y: 4.869 5.300 | 4.694 5.148 -0.175 -0.152
# timing for  I21/temp0: 4.783 5.324 | 4.608 5.172 -0.175 -0.152
# timing for  I21/temp1:
# timing for  I21/temp2:
# timing for  I21/temp3: 5.196 5.156 | 5.021 5.003 -0.175 -0.153
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a22o, A2=0, B2=1, A1=1 ===
pfet(1.00, "5_I22",       "Vdd",    "I22/A1", "I22/temp1")                      # Max size: 163.039
pfet(1.00, "0_I22",       "Vdd",    "I22/A2", "I22/temp1")                      # Max size: 209.045
pfet(1.00, "4_I22", "I22/temp1",    "I22/B1", "I22/temp0")
pfet(1.00, "8_I22", "I22/temp1",    "I22/B2", "I22/temp0")                      # Max size: 416.588
pfet(1.00, "3_I22",       "Vdd", "I22/temp0",     "I22/X")
nfet(0.65, "6_I22", "I22/temp2",    "I22/A1", "I22/temp0")                      # Max size: 277.406
nfet(0.65, "2_I22",      "Vgnd",    "I22/A2", "I22/temp2")                      # Max size: 355.685
nfet(0.65, "1_I22", "I22/temp3",    "I22/B1", "I22/temp0")
nfet(0.65, "9_I22",      "Vgnd",    "I22/B2", "I22/temp3")                      # Max size: 708.815
nfet(0.65, "7_I22",      "Vgnd", "I22/temp0",     "I22/X")
# timing for     I22/B1: 4.869 5.300 | 4.694 5.148 -0.175 -0.152
# timing for      I22/X: 5.049 5.450 | 4.874 5.297 -0.175 -0.153
# timing for  I22/temp0: 4.995 5.367 | 4.820 5.215 -0.175 -0.152
# timing for  I22/temp1:
# timing for  I22/temp2: 5.009 5.384 | 4.834 5.232 -0.175 -0.152
# timing for  I22/temp3:
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  a21o, A1=1, B1=0 ===
pfet(1.00, "3_I23",       "Vdd",    "I23/A1", "I23/temp0")                      # Max size: 431.381
pfet(1.00, "6_I23",       "Vdd",    "I23/A2", "I23/temp0")
pfet(1.00, "1_I23", "I23/temp2",    "I23/B1", "I23/temp0")                      # Max size: 951.233
pfet(1.00, "2_I23",       "Vdd", "I23/temp2",     "I23/X")
nfet(0.65, "7_I23", "I23/temp2",    "I23/A1", "I23/temp1")                      # Max size: 733.985
nfet(0.65, "5_I23",      "Vgnd",    "I23/A2", "I23/temp1")
nfet(0.65, "0_I23",      "Vgnd",    "I23/B1", "I23/temp2")                      # Max size: 1618.5
nfet(0.65, "4_I23",      "Vgnd", "I23/temp2",     "I23/X")
# timing for     I23/A2: 5.049 5.450 | 4.874 5.297 -0.175 -0.153
# timing for      I23/X: 5.228 5.567 | 5.053 5.415 -0.175 -0.152
# timing for  I23/temp0: 5.079 6.019 | 4.904 5.866 -0.175 -0.153
# timing for  I23/temp1: 5.194 5.461 | 5.019 5.308 -0.175 -0.153
# timing for  I23/temp2: 5.181 5.507 | 5.006 5.354 -0.175 -0.153
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  and2, A=1 ===
pfet(0.42, "3_I24",       "Vdd",     "I24/A", "I24/temp1")                      # Max size: 0.0
pfet(0.42, "0_I24",       "Vdd",     "I24/B", "I24/temp1")
pfet(1.00, "1_I24",       "Vdd", "I24/temp1",     "I24/X")
nfet(0.42, "5_I24", "I24/temp1",     "I24/A", "I24/temp0")                      # Max size: 0.0
nfet(0.42, "2_I24",      "Vgnd",     "I24/B", "I24/temp0")
nfet(0.65, "4_I24",      "Vgnd", "I24/temp1",     "I24/X")
# timing for      I24/B: 5.228 5.567 | 5.053 5.415 -0.175 -0.152
# timing for      I24/X: 5.404 5.743 | 5.229 5.591 -0.175 -0.152
# timing for  I24/temp0: 5.347 5.579 | 5.172 5.426 -0.175 -0.153
# timing for  I24/temp1: 5.326 5.624 | 5.151 5.471 -0.175 -0.153
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


# ===  dfxtp ===
pfet(0.42, "5_I25" ,       "Vdd",     "I25/D", "I25/temp10")
pfet(1.00, "4_I25" ,       "Vdd", "I25/temp1",      "I25/Q")
pfet(0.42, "17_I25",       "Vdd", "I25/temp1",  "I25/temp5")
pfet(1.00, "7_I25" ,       "Vdd", "I25/temp2",  "I25/temp1")
pfet(0.42, "2_I25" , "I25/temp6", "I25/temp3",  "I25/temp4")
pfet(0.42, "15_I25", "I25/temp8", "I25/temp3",  "I25/temp2")
pfet(0.64, "19_I25",       "Vdd", "I25/temp3",  "I25/temp9")
pfet(0.75, "11_I25",       "Vdd", "I25/temp6",  "I25/temp8")
pfet(0.42, "9_I25" ,       "Vdd", "I25/temp8",  "I25/temp4")
pfet(0.42, "8_I25" , "I25/temp6", "I25/temp9", "I25/temp10")
pfet(0.42, "12_I25", "I25/temp5", "I25/temp9",  "I25/temp2")
pfet(0.64, "3_I25" ,       "Vdd",       "clk",  "I25/temp3")
nfet(0.42, "22_I25",      "Vgnd",     "I25/D", "I25/temp10")
nfet(0.65, "0_I25" ,      "Vgnd", "I25/temp1",      "I25/Q")
nfet(0.42, "13_I25",      "Vgnd", "I25/temp1",  "I25/temp0")
nfet(0.65, "21_I25",      "Vgnd", "I25/temp2",  "I25/temp1")
nfet(0.42, "14_I25",      "Vgnd", "I25/temp3",  "I25/temp9")
nfet(0.36, "18_I25", "I25/temp2", "I25/temp3",  "I25/temp0")
nfet(0.36, "20_I25", "I25/temp6", "I25/temp3", "I25/temp10")
nfet(0.64, "10_I25",      "Vgnd", "I25/temp6",  "I25/temp8")
nfet(0.42, "6_I25" ,      "Vgnd", "I25/temp8",  "I25/temp7")
nfet(0.36, "1_I25" , "I25/temp8", "I25/temp9",  "I25/temp2")
nfet(0.36, "16_I25", "I25/temp7", "I25/temp9",  "I25/temp6")
nfet(0.42, "23_I25",      "Vgnd",       "clk",  "I25/temp3")
# timing for      I25/D: 5.404 5.743 | 5.229 5.591 -0.175 -0.152


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
    spice.insert(plotline+1, f"meas tran fall_{name} when V({name}) = 0.9")
spice.insert(plotline+1,"run")
spice.insert(plotline+1,"reset")
spice.insert(plotline+1, "alterparam v_start=0")
spice.insert(plotline+1, "alterparam v_q_ic=1.8")

for name in timings_to_track:
    spice.insert(plotline+1, f"meas tran rise_{name} when V({name}) = 0.9")
spice.insert(plotline+1, "run")
spice.insert(plotline+1, "alterparam v_start=1.8")
spice.insert(plotline+1, "alterparam v_q_ic=0")

spice.insert(0, "* Generated by python_spice")

spice = "\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
    