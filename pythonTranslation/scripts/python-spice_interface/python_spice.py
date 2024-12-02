
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
# timing for       I0/Q:
# timing for   I0/temp0:
# timing for   I0/temp1:
# timing for  I0/temp10:
# timing for   I0/temp2:
# timing for   I0/temp3:
# timing for   I0/temp4:
# timing for   I0/temp5:
# timing for   I0/temp6:
# timing for   I0/temp7:
# timing for   I0/temp8:
# timing for   I0/temp9:
# timing for        clk:


# ===  clkbuf ===
pfet(1.00, "0_I1",  "Vdd",     "I1/A", "I1/temp0")
pfet(4.00, "3_I1",  "Vdd", "I1/temp0",     "I1/X")
nfet(0.42, "5_I1", "Vgnd",     "I1/A", "I1/temp0")
nfet(1.68, "1_I1", "Vgnd", "I1/temp0",     "I1/X")
# timing for       I1/A:
# timing for       I1/X:
# timing for   I1/temp0:


# ===  buf ===
pfet(1.00, "8_I2",  "Vdd",     "I2/A", "I2/temp0")
pfet(4.00, "0_I2",  "Vdd", "I2/temp0",     "I2/X")
nfet(0.65, "9_I2", "Vgnd",     "I2/A", "I2/temp0")
nfet(2.60, "4_I2", "Vgnd", "I2/temp0",     "I2/X")
# timing for       I2/A:
# timing for       I2/X:
# timing for   I2/temp0:


# ===  mux2, A0=1, A1=0 ===
pfet(0.42, "4_I3" , "I3/temp4",    "I3/A0", "I3/temp1")                         # Max size: 68.389
pfet(0.42, "7_I3" , "I3/temp3",    "I3/A1", "I3/temp1")                         # Max size: 167.513
pfet(0.42, "1_I3" ,      "Vdd",     "I3/S", "I3/temp5")
pfet(0.42, "2_I3" ,      "Vdd",     "I3/S", "I3/temp4")
pfet(1.00, "10_I3",      "Vdd", "I3/temp1",     "I3/X")
pfet(0.42, "0_I3" ,      "Vdd", "I3/temp5", "I3/temp3")
nfet(0.42, "6_I3" , "I3/temp1",    "I3/A0", "I3/temp0")                         # Max size: 116.362
nfet(0.42, "8_I3" , "I3/temp2",    "I3/A1", "I3/temp1")                         # Max size: 285.019
nfet(0.42, "5_I3" ,     "Vgnd",     "I3/S", "I3/temp5")
nfet(0.42, "9_I3" ,     "Vgnd",     "I3/S", "I3/temp2")
nfet(0.65, "11_I3",     "Vgnd", "I3/temp1",     "I3/X")
nfet(0.42, "3_I3" ,     "Vgnd", "I3/temp5", "I3/temp0")
# timing for      I3/A0:
# timing for      I3/A1:
# timing for       I3/S:
# timing for       I3/X:
# timing for   I3/temp0:
# timing for   I3/temp1:
# timing for   I3/temp2:
# timing for   I3/temp3:
# timing for   I3/temp4:
# timing for   I3/temp5:


# ===  mux2, S=0, A1=1 ===
pfet(0.64, "1_I4" , "I4/temp5",    "I4/A0", "I4/temp0")
pfet(0.64, "3_I4" , "I4/temp5",    "I4/A1", "I4/temp2")                         # Max size: 71.979
pfet(0.64, "0_I4" ,      "Vdd",     "I4/S", "I4/temp0")                         # Max size: 58.459
pfet(0.64, "12_I4",      "Vdd",     "I4/S", "I4/temp4")                         # Max size: 58.459
pfet(0.64, "6_I4" ,      "Vdd", "I4/temp4", "I4/temp2")
pfet(2.00, "2_I4" ,      "Vdd", "I4/temp5",     "I4/X")
nfet(0.42, "7_I4" , "I4/temp5",    "I4/A0", "I4/temp1")
nfet(0.42, "10_I4", "I4/temp5",    "I4/A1", "I4/temp3")                         # Max size: 122.471
nfet(0.42, "5_I4" ,     "Vgnd",     "I4/S", "I4/temp3")                         # Max size: 99.467
nfet(0.42, "9_I4" ,     "Vgnd",     "I4/S", "I4/temp4")                         # Max size: 99.467
nfet(0.42, "8_I4" ,     "Vgnd", "I4/temp4", "I4/temp1")
nfet(1.30, "4_I4" ,     "Vgnd", "I4/temp5",     "I4/X")
# timing for      I4/A0:
# timing for      I4/A1:
# timing for       I4/S:
# timing for       I4/X:
# timing for   I4/temp0:
# timing for   I4/temp1:
# timing for   I4/temp2:
# timing for   I4/temp3:
# timing for   I4/temp4:
# timing for   I4/temp5:


# ===  xor2, A=0 ===
pfet(1.00, "7_I5",      "Vdd",     "I5/A", "I5/temp2")                          # Max size: 319.424
pfet(1.00, "8_I5",      "Vdd",     "I5/A", "I5/temp0")                          # Max size: 319.424
pfet(1.00, "3_I5", "I5/temp3",     "I5/B", "I5/temp0")
pfet(1.00, "4_I5",      "Vdd",     "I5/B", "I5/temp2")
pfet(1.00, "0_I5", "I5/temp2", "I5/temp3",     "I5/X")
nfet(0.65, "5_I5",     "Vgnd",     "I5/A", "I5/temp3")                          # Max size: 543.492
nfet(0.65, "9_I5",     "Vgnd",     "I5/A", "I5/temp1")                          # Max size: 543.492
nfet(0.65, "1_I5", "I5/temp1",     "I5/B",     "I5/X")
nfet(0.65, "2_I5",     "Vgnd",     "I5/B", "I5/temp3")
nfet(0.65, "6_I5",     "Vgnd", "I5/temp3",     "I5/X")
# timing for       I5/A:
# timing for       I5/B:
# timing for       I5/X:
# timing for   I5/temp0:
# timing for   I5/temp1:
# timing for   I5/temp2:
# timing for   I5/temp3:


# ===  a21o, A1=1, B1=0 ===
pfet(1.00, "3_I6",      "Vdd",    "I6/A1", "I6/temp0")                          # Max size: 71.979
pfet(1.00, "6_I6",      "Vdd",    "I6/A2", "I6/temp0")
pfet(1.00, "1_I6", "I6/temp2",    "I6/B1", "I6/temp0")                          # Max size: 158.096
pfet(1.00, "2_I6",      "Vdd", "I6/temp2",     "I6/X")
nfet(0.65, "7_I6", "I6/temp2",    "I6/A1", "I6/temp1")                          # Max size: 122.471
nfet(0.65, "5_I6",     "Vgnd",    "I6/A2", "I6/temp1")
nfet(0.65, "0_I6",     "Vgnd",    "I6/B1", "I6/temp2")                          # Max size: 268.997
nfet(0.65, "4_I6",     "Vgnd", "I6/temp2",     "I6/X")
# timing for      I6/A1:
# timing for      I6/A2:
# timing for      I6/B1:
# timing for       I6/X:
# timing for   I6/temp0:
# timing for   I6/temp1:
# timing for   I6/temp2:


# ===  a211o, C1=0, A1=1, B1=0 ===
pfet(1.00, "6_I7",      "Vdd",    "I7/A1", "I7/temp3")                          # Max size: 35.989
pfet(1.00, "2_I7",      "Vdd",    "I7/A2", "I7/temp3")
pfet(1.00, "8_I7", "I7/temp3",    "I7/B1", "I7/temp1")                          # Max size: 198.255
pfet(1.00, "1_I7", "I7/temp2",    "I7/C1", "I7/temp1")                          # Max size: 96.012
pfet(1.00, "0_I7",      "Vdd", "I7/temp2",     "I7/X")
nfet(0.65, "7_I7", "I7/temp2",    "I7/A1", "I7/temp0")                          # Max size: 61.235
nfet(0.65, "5_I7",     "Vgnd",    "I7/A2", "I7/temp0")
nfet(0.65, "3_I7",     "Vgnd",    "I7/B1", "I7/temp2")                          # Max size: 337.327
nfet(0.65, "9_I7",     "Vgnd",    "I7/C1", "I7/temp2")                          # Max size: 163.362
nfet(0.65, "4_I7",     "Vgnd", "I7/temp2",     "I7/X")
# timing for      I7/A1:
# timing for      I7/A2:
# timing for      I7/B1:
# timing for      I7/C1:
# timing for       I7/X:
# timing for   I7/temp0:
# timing for   I7/temp1:
# timing for   I7/temp2:
# timing for   I7/temp3:


# ===  a311o, C1=0, A1=1, A2=1, B1=0 ===
pfet(1.00, "7_I8" ,      "Vdd",    "I8/A1", "I8/temp0")                         # Max size: 71.979
pfet(1.00, "1_I8" ,      "Vdd",    "I8/A2", "I8/temp0")                         # Max size: 33.669
pfet(1.00, "9_I8" ,      "Vdd",    "I8/A3", "I8/temp0")
pfet(1.00, "11_I8", "I8/temp3",    "I8/B1", "I8/temp0")                         # Max size: 266.571
pfet(1.00, "0_I8" , "I8/temp3",    "I8/C1", "I8/temp2")                         # Max size: 178.637
pfet(2.00, "6_I8" ,      "Vdd", "I8/temp2",     "I8/X")
nfet(0.65, "4_I8" , "I8/temp2",    "I8/A1", "I8/temp1")                         # Max size: 122.471
nfet(0.65, "3_I8" , "I8/temp4",    "I8/A2", "I8/temp1")                         # Max size: 57.287
nfet(0.65, "5_I8" ,     "Vgnd",    "I8/A3", "I8/temp4")
nfet(0.65, "2_I8" ,     "Vgnd",    "I8/B1", "I8/temp2")                         # Max size: 453.565
nfet(0.65, "10_I8",     "Vgnd",    "I8/C1", "I8/temp2")                         # Max size: 303.947
nfet(1.30, "8_I8" ,     "Vgnd", "I8/temp2",     "I8/X")
# timing for      I8/A1:
# timing for      I8/A2:
# timing for      I8/A3:
# timing for      I8/B1:
# timing for      I8/C1:
# timing for       I8/X:
# timing for   I8/temp0:
# timing for   I8/temp1:
# timing for   I8/temp2:
# timing for   I8/temp3:
# timing for   I8/temp4:


# ===  a221oi, B2=1, C1=0, A1=1, B1=0 ===
pfet(2.00, "6_I9" ,      "Vdd", "I9/A1", "I9/temp1")                            # Max size: 71.979
pfet(2.00, "2_I9" ,      "Vdd", "I9/A2", "I9/temp1")
pfet(2.00, "1_I9" , "I9/temp1", "I9/B1", "I9/temp0")                            # Max size: 292.19
pfet(2.00, "5_I9" , "I9/temp1", "I9/B2", "I9/temp0")                            # Max size: 111.568
pfet(2.00, "9_I9" , "I9/temp0", "I9/C1",     "I9/Y")                            # Max size: 289.421
nfet(1.30, "4_I9" , "I9/temp2", "I9/A1",     "I9/Y")                            # Max size: 122.471
nfet(1.30, "7_I9" ,     "Vgnd", "I9/A2", "I9/temp2")
nfet(1.30, "0_I9" , "I9/temp3", "I9/B1",     "I9/Y")                            # Max size: 497.154
nfet(1.30, "3_I9" ,     "Vgnd", "I9/B2", "I9/temp3")                            # Max size: 189.831
nfet(1.30, "10_I9",     "Vgnd", "I9/C1",     "I9/Y")                            # Max size: 492.442
# timing for      I9/A1:
# timing for      I9/A2:
# timing for      I9/B1:
# timing for      I9/B2:
# timing for      I9/C1:
# timing for       I9/Y:
# timing for   I9/temp0:
# timing for   I9/temp1:
# timing for   I9/temp2:
# timing for   I9/temp3:


# ===  or4, D=0, C=0, B=0 ===
pfet(0.42, "3_I10",       "Vdd",     "I10/A", "I10/temp3")
pfet(0.42, "2_I10", "I10/temp3",     "I10/B", "I10/temp1")                      # Max size: 139.517
pfet(0.42, "5_I10", "I10/temp2",     "I10/C", "I10/temp1")                      # Max size: 129.362
pfet(0.42, "8_I10", "I10/temp2",     "I10/D", "I10/temp0")                      # Max size: 98.397
pfet(1.00, "6_I10",       "Vdd", "I10/temp0",     "I10/X")
nfet(0.42, "9_I10",      "Vgnd",     "I10/A", "I10/temp0")
nfet(0.42, "0_I10",      "Vgnd",     "I10/B", "I10/temp0")                      # Max size: 237.385
nfet(0.42, "7_I10",      "Vgnd",     "I10/C", "I10/temp0")                      # Max size: 220.106
nfet(0.42, "1_I10",      "Vgnd",     "I10/D", "I10/temp0")                      # Max size: 167.42
nfet(0.65, "4_I10",      "Vgnd", "I10/temp0",     "I10/X")
# timing for      I10/A:
# timing for      I10/B:
# timing for      I10/C:
# timing for      I10/D:
# timing for      I10/X:
# timing for  I10/temp0:
# timing for  I10/temp1:
# timing for  I10/temp2:
# timing for  I10/temp3:


# ===  a21oi, A2=1, B1=0 ===
pfet(2.00, "5_I11" ,       "Vdd", "I11/A1", "I11/temp2")
pfet(2.00, "7_I11" ,       "Vdd", "I11/A2", "I11/temp2")                        # Max size: 115.436
pfet(2.00, "4_I11" , "I11/temp2", "I11/B1",     "I11/Y")                        # Max size: 180.253
nfet(0.65, "2_I11" , "I11/temp1", "I11/A1",     "I11/Y")
nfet(0.65, "10_I11", "I11/temp0", "I11/A1",     "I11/Y")
nfet(0.65, "0_I11" ,      "Vgnd", "I11/A2", "I11/temp0")                        # Max size: 196.412
nfet(0.65, "3_I11" ,      "Vgnd", "I11/A2", "I11/temp1")                        # Max size: 196.412
nfet(1.30, "1_I11" ,      "Vgnd", "I11/B1",     "I11/Y")                        # Max size: 306.696
# timing for     I11/A1:
# timing for     I11/A2:
# timing for     I11/B1:
# timing for      I11/Y:
# timing for  I11/temp0:
# timing for  I11/temp1:
# timing for  I11/temp2:


# ===  o211a, A2=0, C1=1, B1=1 ===
pfet(1.00, "5_I12",       "Vdd",    "I12/A1", "I12/temp0")
pfet(1.00, "4_I12", "I12/temp2",    "I12/A2", "I12/temp0")                      # Max size: 256.186
pfet(1.00, "3_I12",       "Vdd",    "I12/B1", "I12/temp2")                      # Max size: 96.296
pfet(1.00, "2_I12",       "Vdd",    "I12/C1", "I12/temp2")                      # Max size: 194.476
pfet(1.00, "7_I12",       "Vdd", "I12/temp2",     "I12/X")
nfet(0.65, "0_I12",      "Vgnd",    "I12/A1", "I12/temp3")
nfet(0.65, "9_I12",      "Vgnd",    "I12/A2", "I12/temp3")                      # Max size: 435.893
nfet(0.65, "1_I12", "I12/temp3",    "I12/B1", "I12/temp1")                      # Max size: 163.845
nfet(0.65, "6_I12", "I12/temp2",    "I12/C1", "I12/temp1")                      # Max size: 330.896
nfet(0.65, "8_I12",      "Vgnd", "I12/temp2",     "I12/X")
# timing for     I12/A1:
# timing for     I12/A2:
# timing for     I12/B1:
# timing for     I12/C1:
# timing for      I12/X:
# timing for  I12/temp0:
# timing for  I12/temp1:
# timing for  I12/temp2:
# timing for  I12/temp3:


# ===  a41o, A3=1, A4=1, A2=1, B1=0 ===
pfet(1.00, "5_I13" ,       "Vdd",    "I13/A1", "I13/temp0")
pfet(1.00, "3_I13" ,       "Vdd",    "I13/A2", "I13/temp0")                     # Max size: 231.566
pfet(1.00, "2_I13" ,       "Vdd",    "I13/A3", "I13/temp0")                     # Max size: 155.502
pfet(1.00, "4_I13" ,       "Vdd",    "I13/A4", "I13/temp0")                     # Max size: 143.006
pfet(1.00, "7_I13" , "I13/temp3",    "I13/B1", "I13/temp0")                     # Max size: 454.441
pfet(1.00, "8_I13" ,       "Vdd", "I13/temp3",     "I13/X")
nfet(0.65, "6_I13" , "I13/temp3",    "I13/A1", "I13/temp2")
nfet(0.65, "0_I13" , "I13/temp2",    "I13/A2", "I13/temp1")                     # Max size: 394.005
nfet(0.65, "11_I13", "I13/temp4",    "I13/A3", "I13/temp1")                     # Max size: 264.582
nfet(0.65, "1_I13" ,      "Vgnd",    "I13/A4", "I13/temp4")                     # Max size: 243.321
nfet(0.65, "9_I13" ,      "Vgnd",    "I13/B1", "I13/temp3")                     # Max size: 773.22
nfet(0.65, "10_I13",      "Vgnd", "I13/temp3",     "I13/X")
# timing for     I13/A1:
# timing for     I13/A2:
# timing for     I13/A3:
# timing for     I13/A4:
# timing for     I13/B1:
# timing for      I13/X:
# timing for  I13/temp0:
# timing for  I13/temp1:
# timing for  I13/temp2:
# timing for  I13/temp3:
# timing for  I13/temp4:


# ===  a21oi, A2=1, B1=0 ===
pfet(2.00, "5_I14" ,       "Vdd", "I14/A1", "I14/temp2")
pfet(2.00, "7_I14" ,       "Vdd", "I14/A2", "I14/temp2")                        # Max size: 166.609
pfet(2.00, "4_I14" , "I14/temp2", "I14/B1",     "I14/Y")                        # Max size: 598.228
nfet(0.65, "2_I14" , "I14/temp1", "I14/A1",     "I14/Y")
nfet(0.65, "10_I14", "I14/temp0", "I14/A1",     "I14/Y")
nfet(0.65, "0_I14" ,      "Vgnd", "I14/A2", "I14/temp0")                        # Max size: 283.481
nfet(0.65, "3_I14" ,      "Vgnd", "I14/A2", "I14/temp1")                        # Max size: 283.481
nfet(1.30, "1_I14" ,      "Vgnd", "I14/B1",     "I14/Y")                        # Max size: 1017.87
# timing for     I14/A1:
# timing for     I14/A2:
# timing for     I14/B1:
# timing for      I14/Y:
# timing for  I14/temp0:
# timing for  I14/temp1:
# timing for  I14/temp2:


# ===  nand2b, B=1 ===
pfet(0.42, "5_I15",       "Vdd",   "I15/A_N", "I15/temp1")
pfet(1.00, "4_I15",       "Vdd",     "I15/B",     "I15/Y")                      # Max size: 222.145
pfet(1.00, "3_I15",       "Vdd", "I15/temp1",     "I15/Y")
nfet(0.42, "0_I15",      "Vgnd",   "I15/A_N", "I15/temp1")
nfet(0.65, "2_I15",      "Vgnd",     "I15/B", "I15/temp0")                      # Max size: 377.975
nfet(0.65, "1_I15", "I15/temp0", "I15/temp1",     "I15/Y")
# timing for    I15/A_N:
# timing for      I15/B:
# timing for      I15/Y:
# timing for  I15/temp0:
# timing for  I15/temp1:


# ===  nor2, B=0 ===
pfet(1.00, "0_I16",       "Vdd", "I16/A", "I16/temp0")
pfet(1.00, "2_I16", "I16/temp0", "I16/B",     "I16/Y")                          # Max size: 286.074
nfet(0.65, "1_I16",      "Vgnd", "I16/A",     "I16/Y")
nfet(0.65, "3_I16",      "Vgnd", "I16/B",     "I16/Y")                          # Max size: 486.748
# timing for      I16/A:
# timing for      I16/B:
# timing for      I16/Y:
# timing for  I16/temp0:


# ===  a311o, A3=1, C1=0, A1=1, B1=0 ===
pfet(1.00, "10_I17",       "Vdd",    "I17/A1", "I17/temp4")                     # Max size: 71.979
pfet(1.00, "9_I17" ,       "Vdd",    "I17/A2", "I17/temp4")
pfet(1.00, "8_I17" ,       "Vdd",    "I17/A3", "I17/temp4")                     # Max size: 242.971
pfet(1.00, "6_I17" , "I17/temp4",    "I17/B1", "I17/temp0")                     # Max size: 741.092
pfet(1.00, "5_I17" , "I17/temp1",    "I17/C1", "I17/temp0")                     # Max size: 726.551
pfet(1.00, "7_I17" ,       "Vdd", "I17/temp1",     "I17/X")
nfet(0.65, "4_I17" , "I17/temp3",    "I17/A1", "I17/temp1")                     # Max size: 122.471
nfet(0.65, "2_I17" , "I17/temp3",    "I17/A2", "I17/temp2")
nfet(0.65, "1_I17" ,      "Vgnd",    "I17/A3", "I17/temp2")                     # Max size: 413.41
nfet(0.65, "3_I17" ,      "Vgnd",    "I17/B1", "I17/temp1")                     # Max size: 1260.95
nfet(0.65, "0_I17" ,      "Vgnd",    "I17/C1", "I17/temp1")                     # Max size: 1236.21
nfet(0.65, "11_I17",      "Vgnd", "I17/temp1",     "I17/X")
# timing for     I17/A1:
# timing for     I17/A2:
# timing for     I17/A3:
# timing for     I17/B1:
# timing for     I17/C1:
# timing for      I17/X:
# timing for  I17/temp0:
# timing for  I17/temp1:
# timing for  I17/temp2:
# timing for  I17/temp3:
# timing for  I17/temp4:


# ===  a21o, A2=1, B1=0 ===
pfet(1.00, "3_I18",       "Vdd",    "I18/A1", "I18/temp0")
pfet(1.00, "6_I18",       "Vdd",    "I18/A2", "I18/temp0")                      # Max size: 148.907
pfet(1.00, "1_I18", "I18/temp2",    "I18/B1", "I18/temp0")                      # Max size: 729.552
pfet(1.00, "2_I18",       "Vdd", "I18/temp2",     "I18/X")
nfet(0.65, "7_I18", "I18/temp2",    "I18/A1", "I18/temp1")
nfet(0.65, "5_I18",      "Vgnd",    "I18/A2", "I18/temp1")                      # Max size: 253.361
nfet(0.65, "0_I18",      "Vgnd",    "I18/B1", "I18/temp2")                      # Max size: 1241.315
nfet(0.65, "4_I18",      "Vgnd", "I18/temp2",     "I18/X")
# timing for     I18/A1:
# timing for     I18/A2:
# timing for     I18/B1:
# timing for      I18/X:
# timing for  I18/temp0:
# timing for  I18/temp1:
# timing for  I18/temp2:


# ===  o21a, A2=1, A1=1 ===
pfet(1.00, "0_I19",       "Vdd",    "I19/A1", "I19/temp2")                      # Max size: 71.979
pfet(1.00, "6_I19", "I19/temp2",    "I19/A2", "I19/temp1")                      # Max size: 323.301
pfet(1.00, "5_I19",       "Vdd",    "I19/B1", "I19/temp1")
pfet(1.00, "4_I19",       "Vdd", "I19/temp1",     "I19/X")
nfet(0.65, "2_I19",      "Vgnd",    "I19/A1", "I19/temp0")                      # Max size: 122.471
nfet(0.65, "3_I19",      "Vgnd",    "I19/A2", "I19/temp0")                      # Max size: 550.088
nfet(0.65, "1_I19", "I19/temp1",    "I19/B1", "I19/temp0")
nfet(0.65, "7_I19",      "Vgnd", "I19/temp1",     "I19/X")
# timing for     I19/A1:
# timing for     I19/A2:
# timing for     I19/B1:
# timing for      I19/X:
# timing for  I19/temp0:
# timing for  I19/temp1:
# timing for  I19/temp2:


# ===  a21oi, A2=0, A1=1 ===
pfet(1.00, "3_I20",       "Vdd", "I20/A1", "I20/temp1")                         # Max size: 71.979
pfet(1.00, "1_I20",       "Vdd", "I20/A2", "I20/temp1")                         # Max size: 826.949
pfet(1.00, "4_I20", "I20/temp1", "I20/B1",     "I20/Y")
nfet(0.65, "0_I20", "I20/temp0", "I20/A1",     "I20/Y")                         # Max size: 122.471
nfet(0.65, "5_I20",      "Vgnd", "I20/A2", "I20/temp0")                         # Max size: 1407.033
nfet(0.65, "2_I20",      "Vgnd", "I20/B1",     "I20/Y")
# timing for     I20/A1:
# timing for     I20/A2:
# timing for     I20/B1:
# timing for      I20/Y:
# timing for  I20/temp0:
# timing for  I20/temp1:


# ===  xnor2, B=0 ===
pfet(1.00, "0_I21",       "Vdd",     "I21/A", "I21/temp3")
pfet(1.00, "6_I21",       "Vdd",     "I21/A", "I21/temp2")
pfet(1.00, "1_I21",       "Vdd",     "I21/B", "I21/temp2")                      # Max size: 411.859
pfet(1.00, "8_I21", "I21/temp3",     "I21/B",     "I21/Y")                      # Max size: 411.859
pfet(1.00, "7_I21",       "Vdd", "I21/temp2",     "I21/Y")
nfet(0.65, "5_I21",      "Vgnd",     "I21/A", "I21/temp1")
nfet(0.65, "9_I21",      "Vgnd",     "I21/A", "I21/temp0")
nfet(0.65, "2_I21", "I21/temp2",     "I21/B", "I21/temp1")                      # Max size: 700.768
nfet(0.65, "3_I21",      "Vgnd",     "I21/B", "I21/temp0")                      # Max size: 700.768
nfet(0.65, "4_I21", "I21/temp0", "I21/temp2",     "I21/Y")
# timing for      I21/A:
# timing for      I21/B:
# timing for      I21/Y:
# timing for  I21/temp0:
# timing for  I21/temp1:
# timing for  I21/temp2:
# timing for  I21/temp3:


# ===  a22o, A2=0, B2=1, A1=1 ===
pfet(1.00, "5_I22",       "Vdd",    "I22/A1", "I22/temp1")                      # Max size: 71.979
pfet(1.00, "0_I22",       "Vdd",    "I22/A2", "I22/temp1")                      # Max size: 114.13
pfet(1.00, "4_I22", "I22/temp1",    "I22/B1", "I22/temp0")
pfet(1.00, "8_I22", "I22/temp1",    "I22/B2", "I22/temp0")                      # Max size: 382.407
pfet(1.00, "3_I22",       "Vdd", "I22/temp0",     "I22/X")
nfet(0.65, "6_I22", "I22/temp2",    "I22/A1", "I22/temp0")                      # Max size: 122.471
nfet(0.65, "2_I22",      "Vgnd",    "I22/A2", "I22/temp2")                      # Max size: 194.189
nfet(0.65, "1_I22", "I22/temp3",    "I22/B1", "I22/temp0")
nfet(0.65, "9_I22",      "Vgnd",    "I22/B2", "I22/temp3")                      # Max size: 650.656
nfet(0.65, "7_I22",      "Vgnd", "I22/temp0",     "I22/X")
# timing for     I22/A1:
# timing for     I22/A2:
# timing for     I22/B1:
# timing for     I22/B2:
# timing for      I22/X:
# timing for  I22/temp0:
# timing for  I22/temp1:
# timing for  I22/temp2:
# timing for  I22/temp3:


# ===  a21o, A1=1, B1=0 ===
pfet(1.00, "3_I23",       "Vdd",    "I23/A1", "I23/temp0")                      # Max size: 71.979
pfet(1.00, "6_I23",       "Vdd",    "I23/A2", "I23/temp0")
pfet(1.00, "1_I23", "I23/temp2",    "I23/B1", "I23/temp0")                      # Max size: 868.031
pfet(1.00, "2_I23",       "Vdd", "I23/temp2",     "I23/X")
nfet(0.65, "7_I23", "I23/temp2",    "I23/A1", "I23/temp1")                      # Max size: 122.471
nfet(0.65, "5_I23",      "Vgnd",    "I23/A2", "I23/temp1")
nfet(0.65, "0_I23",      "Vgnd",    "I23/B1", "I23/temp2")                      # Max size: 1476.933
nfet(0.65, "4_I23",      "Vgnd", "I23/temp2",     "I23/X")
# timing for     I23/A1:
# timing for     I23/A2:
# timing for     I23/B1:
# timing for      I23/X:
# timing for  I23/temp0:
# timing for  I23/temp1:
# timing for  I23/temp2:


# ===  and2, A=1 ===
pfet(0.42, "3_I24",       "Vdd",     "I24/A", "I24/temp1")                      # Max size: 0.0
pfet(0.42, "0_I24",       "Vdd",     "I24/B", "I24/temp1")
pfet(1.00, "1_I24",       "Vdd", "I24/temp1",     "I24/X")
nfet(0.42, "5_I24", "I24/temp1",     "I24/A", "I24/temp0")                      # Max size: 0.0
nfet(0.42, "2_I24",      "Vgnd",     "I24/B", "I24/temp0")
nfet(0.65, "4_I24",      "Vgnd", "I24/temp1",     "I24/X")
# timing for      I24/A:
# timing for      I24/B:
# timing for      I24/X:
# timing for  I24/temp0:
# timing for  I24/temp1:


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
# timing for      I25/D:
# timing for      I25/Q:
# timing for  I25/temp0:
# timing for  I25/temp1:
# timing for I25/temp10:
# timing for  I25/temp2:
# timing for  I25/temp3:
# timing for  I25/temp4:
# timing for  I25/temp5:
# timing for  I25/temp6:
# timing for  I25/temp7:
# timing for  I25/temp8:
# timing for  I25/temp9:
# timing for        clk:




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
    