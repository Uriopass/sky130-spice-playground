import bisect

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

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    closest_bin = bins_pfet[min(bisect.bisect_left(bins_pfet, W), len(bins_pfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    closest_bin = bins_nfet[min(bisect.bisect_left(bins_nfet, W), len(bins_nfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

with open("../../libs/ngspice/out.spice", 'r') as f:
    spice = f.read()

spice = spice.split('\n')

to_clear = [120, 122, 124, 125, 126, 127, 157, 158, 159, 161, 162, 163, 285, 287, 567, 568, 659, 662, 663, 664, 665, 666, 667, 668, 669, 670, 826, 828, 829, 831, 1062, 1064, 1065, 1067]
for line in to_clear: spice[line] = ''

# ===  dfxtp ===
spice[  26] = pfet(0.42, "5_I0" ,      "Vdd",     "I0/D", "I0/temp10")
spice[  25] = pfet(1.00, "4_I0" ,      "Vdd", "I0/temp1",      "I0/Q")
spice[  38] = pfet(0.42, "17_I0",      "Vdd", "I0/temp1",  "I0/temp5")
spice[  28] = pfet(1.00, "7_I0" ,      "Vdd", "I0/temp2",  "I0/temp1")
spice[  23] = pfet(0.42, "2_I0" , "I0/temp6", "I0/temp3",  "I0/temp4")
spice[  36] = pfet(0.42, "15_I0", "I0/temp8", "I0/temp3",  "I0/temp2")
spice[  40] = pfet(0.64, "19_I0",      "Vdd", "I0/temp3",  "I0/temp9")
spice[  32] = pfet(0.75, "11_I0",      "Vdd", "I0/temp6",  "I0/temp8")
spice[  30] = pfet(0.42, "9_I0" ,      "Vdd", "I0/temp8",  "I0/temp4")
spice[  29] = pfet(0.42, "8_I0" , "I0/temp6", "I0/temp9", "I0/temp10")
spice[  33] = pfet(0.42, "12_I0", "I0/temp5", "I0/temp9",  "I0/temp2")
spice[  24] = pfet(0.64, "3_I0" ,      "Vdd",      "clk",  "I0/temp3")
spice[  43] = nfet(0.42, "22_I0",     "Vgnd",     "I0/D", "I0/temp10")
spice[  21] = nfet(0.65, "0_I0" ,     "Vgnd", "I0/temp1",      "I0/Q")
spice[  34] = nfet(0.42, "13_I0",     "Vgnd", "I0/temp1",  "I0/temp0")
spice[  42] = nfet(0.65, "21_I0",     "Vgnd", "I0/temp2",  "I0/temp1")
spice[  35] = nfet(0.42, "14_I0",     "Vgnd", "I0/temp3",  "I0/temp9")
spice[  39] = nfet(0.36, "18_I0", "I0/temp2", "I0/temp3",  "I0/temp0")
spice[  41] = nfet(0.36, "20_I0", "I0/temp6", "I0/temp3", "I0/temp10")
spice[  31] = nfet(0.64, "10_I0",     "Vgnd", "I0/temp6",  "I0/temp8")
spice[  27] = nfet(0.42, "6_I0" ,     "Vgnd", "I0/temp8",  "I0/temp7")
spice[  22] = nfet(0.36, "1_I0" , "I0/temp8", "I0/temp9",  "I0/temp2")
spice[  37] = nfet(0.36, "16_I0", "I0/temp7", "I0/temp9",  "I0/temp6")
spice[  44] = nfet(0.42, "23_I0",     "Vgnd",      "clk",  "I0/temp3")
# timing for       I0/D:
# timing for       I0/Q: 0.03n 0.03n
# timing for   I0/temp0:
# timing for   I0/temp1:
# timing for  I0/temp10:
# timing for   I0/temp2:
# timing for   I0/temp3: 0.18n 0.18n
# timing for   I0/temp4: 0.52n 0.52n
# timing for   I0/temp5:
# timing for   I0/temp6:
# timing for   I0/temp7:
# timing for   I0/temp8:
# timing for   I0/temp9: 0.27n 0.27n
# timing for        clk: 0.10n 0.10n


# ===  clkbuf ===
spice[ 118] = pfet(1.00, "0_I1",  "Vdd",     "I1/A", "I1/temp0")
spice[ 121] = pfet(4.00, "3_I1",  "Vdd", "I1/temp0",     "I1/X")
spice[ 123] = nfet(0.42, "5_I1", "Vgnd",     "I1/A", "I1/temp0")
spice[ 119] = nfet(1.68, "1_I1", "Vgnd", "I1/temp0",     "I1/X")
# timing for       I1/A: 0.04n 0.04n
# timing for       I1/X: 0.20n 0.20n
# timing for   I1/temp0: 0.12n 0.12n


# ===  buf ===
spice[ 164] = pfet(1.00, "8_I2",  "Vdd",     "I2/A", "I2/temp0")
spice[ 156] = pfet(4.00, "0_I2",  "Vdd", "I2/temp0",     "I2/X")
spice[ 165] = nfet(0.65, "9_I2", "Vgnd",     "I2/A", "I2/temp0")
spice[ 160] = nfet(2.60, "4_I2", "Vgnd", "I2/temp0",     "I2/X")
# timing for       I2/A: 0.28n 0.28n
# timing for       I2/X: 0.47n 0.47n
# timing for   I2/temp0: 0.36n 0.36n


# ===  mux2, A0=1, A1=0 ===
spice[ 207] = pfet(0.42, "4_I3" , "I3/temp4",    "I3/A0", "I3/temp1")           # Max size: 68.389
spice[ 210] = pfet(0.42, "7_I3" , "I3/temp3",    "I3/A1", "I3/temp1")           # Max size: 167.513
spice[ 204] = pfet(0.42, "1_I3" ,      "Vdd",     "I3/S", "I3/temp5")
spice[ 205] = pfet(0.42, "2_I3" ,      "Vdd",     "I3/S", "I3/temp4")
spice[ 213] = pfet(1.00, "10_I3",      "Vdd", "I3/temp1",     "I3/X")
spice[ 203] = pfet(0.42, "0_I3" ,      "Vdd", "I3/temp5", "I3/temp3")
spice[ 209] = nfet(0.42, "6_I3" , "I3/temp1",    "I3/A0", "I3/temp0")           # Max size: 116.362
spice[ 211] = nfet(0.42, "8_I3" , "I3/temp2",    "I3/A1", "I3/temp1")           # Max size: 285.019
spice[ 208] = nfet(0.42, "5_I3" ,     "Vgnd",     "I3/S", "I3/temp5")
spice[ 212] = nfet(0.42, "9_I3" ,     "Vgnd",     "I3/S", "I3/temp2")
spice[ 214] = nfet(0.65, "11_I3",     "Vgnd", "I3/temp1",     "I3/X")
spice[ 206] = nfet(0.42, "3_I3" ,     "Vgnd", "I3/temp5", "I3/temp0")
# timing for      I3/A0:
# timing for      I3/A1:
# timing for       I3/S: 0.65n 0.65n
# timing for       I3/X: 1.01n 1.01n
# timing for   I3/temp0: 0.95n 0.95n
# timing for   I3/temp1: 0.93n 0.93n
# timing for   I3/temp2:
# timing for   I3/temp3: 0.74n 0.74n
# timing for   I3/temp4:
# timing for   I3/temp5: 0.71n 0.71n


# ===  mux2, S=0, A1=1 ===
spice[ 275] = pfet(0.64, "1_I4" , "I4/temp5",    "I4/A0", "I4/temp0")
spice[ 277] = pfet(0.64, "3_I4" , "I4/temp5",    "I4/A1", "I4/temp2")           # Max size: 71.979
spice[ 274] = pfet(0.64, "0_I4" ,      "Vdd",     "I4/S", "I4/temp0")           # Max size: 58.459
spice[ 286] = pfet(0.64, "12_I4",      "Vdd",     "I4/S", "I4/temp4")           # Max size: 58.459
spice[ 280] = pfet(0.64, "6_I4" ,      "Vdd", "I4/temp4", "I4/temp2")
spice[ 276] = pfet(2.00, "2_I4" ,      "Vdd", "I4/temp5",     "I4/X")
spice[ 281] = nfet(0.42, "7_I4" , "I4/temp5",    "I4/A0", "I4/temp1")
spice[ 284] = nfet(0.42, "10_I4", "I4/temp5",    "I4/A1", "I4/temp3")           # Max size: 122.471
spice[ 279] = nfet(0.42, "5_I4" ,     "Vgnd",     "I4/S", "I4/temp3")           # Max size: 99.467
spice[ 283] = nfet(0.42, "9_I4" ,     "Vgnd",     "I4/S", "I4/temp4")           # Max size: 99.467
spice[ 282] = nfet(0.42, "8_I4" ,     "Vgnd", "I4/temp4", "I4/temp1")
spice[ 278] = nfet(1.30, "4_I4" ,     "Vgnd", "I4/temp5",     "I4/X")
# timing for      I4/A0: 1.02n 1.02n
# timing for      I4/A1:
# timing for       I4/S:
# timing for       I4/X: 1.33n 1.33n
# timing for   I4/temp0:
# timing for   I4/temp1:
# timing for   I4/temp2:
# timing for   I4/temp3: 1.26n 1.26n
# timing for   I4/temp4:
# timing for   I4/temp5: 1.23n 1.23n


# ===  xor2, A=0 ===
spice[ 349] = pfet(1.00, "7_I5",      "Vdd",     "I5/A", "I5/temp2")            # Max size: 319.424
spice[ 350] = pfet(1.00, "8_I5",      "Vdd",     "I5/A", "I5/temp0")            # Max size: 319.424
spice[ 345] = pfet(1.00, "3_I5", "I5/temp3",     "I5/B", "I5/temp0")
spice[ 346] = pfet(1.00, "4_I5",      "Vdd",     "I5/B", "I5/temp2")
spice[ 342] = pfet(1.00, "0_I5", "I5/temp2", "I5/temp3",     "I5/X")
spice[ 347] = nfet(0.65, "5_I5",     "Vgnd",     "I5/A", "I5/temp3")            # Max size: 543.492
spice[ 351] = nfet(0.65, "9_I5",     "Vgnd",     "I5/A", "I5/temp1")            # Max size: 543.492
spice[ 343] = nfet(0.65, "1_I5", "I5/temp1",     "I5/B",     "I5/X")
spice[ 344] = nfet(0.65, "2_I5",     "Vgnd",     "I5/B", "I5/temp3")
spice[ 348] = nfet(0.65, "6_I5",     "Vgnd", "I5/temp3",     "I5/X")
# timing for       I5/A:
# timing for       I5/B: 1.45n 1.45n
# timing for       I5/X: 1.73n 1.73n
# timing for   I5/temp0:
# timing for   I5/temp1:
# timing for   I5/temp2:
# timing for   I5/temp3: 1.64n 1.64n


# ===  a21o, A1=1, B1=0 ===
spice[ 405] = pfet(1.00, "3_I6",      "Vdd",    "I6/A1", "I6/temp0")            # Max size: 71.979
spice[ 408] = pfet(1.00, "6_I6",      "Vdd",    "I6/A2", "I6/temp0")
spice[ 403] = pfet(1.00, "1_I6", "I6/temp2",    "I6/B1", "I6/temp0")            # Max size: 158.096
spice[ 404] = pfet(1.00, "2_I6",      "Vdd", "I6/temp2",     "I6/X")
spice[ 409] = nfet(0.65, "7_I6", "I6/temp2",    "I6/A1", "I6/temp1")            # Max size: 122.471
spice[ 407] = nfet(0.65, "5_I6",     "Vgnd",    "I6/A2", "I6/temp1")
spice[ 402] = nfet(0.65, "0_I6",     "Vgnd",    "I6/B1", "I6/temp2")            # Max size: 268.997
spice[ 406] = nfet(0.65, "4_I6",     "Vgnd", "I6/temp2",     "I6/X")
# timing for      I6/A1:
# timing for      I6/A2: 1.76n 1.76n
# timing for      I6/B1:
# timing for       I6/X: 2.00n 2.00n
# timing for   I6/temp0: 1.80n 1.80n
# timing for   I6/temp1: 1.93n 1.93n
# timing for   I6/temp2: 1.92n 1.92n


# ===  a211o, C1=0, A1=1, B1=0 ===
spice[ 478] = pfet(1.00, "6_I7",      "Vdd",    "I7/A1", "I7/temp3")            # Max size: 35.989
spice[ 474] = pfet(1.00, "2_I7",      "Vdd",    "I7/A2", "I7/temp3")
spice[ 480] = pfet(1.00, "8_I7", "I7/temp3",    "I7/B1", "I7/temp1")            # Max size: 198.255
spice[ 473] = pfet(1.00, "1_I7", "I7/temp2",    "I7/C1", "I7/temp1")            # Max size: 96.012
spice[ 472] = pfet(1.00, "0_I7",      "Vdd", "I7/temp2",     "I7/X")
spice[ 479] = nfet(0.65, "7_I7", "I7/temp2",    "I7/A1", "I7/temp0")            # Max size: 61.235
spice[ 477] = nfet(0.65, "5_I7",     "Vgnd",    "I7/A2", "I7/temp0")
spice[ 475] = nfet(0.65, "3_I7",     "Vgnd",    "I7/B1", "I7/temp2")            # Max size: 337.327
spice[ 481] = nfet(0.65, "9_I7",     "Vgnd",    "I7/C1", "I7/temp2")            # Max size: 163.362
spice[ 476] = nfet(0.65, "4_I7",     "Vgnd", "I7/temp2",     "I7/X")
# timing for      I7/A1:
# timing for      I7/A2: 2.05n 2.05n
# timing for      I7/B1:
# timing for      I7/C1:
# timing for       I7/X: 2.41n 2.41n
# timing for   I7/temp0: 2.33n 2.33n
# timing for   I7/temp1: 2.13n 2.13n
# timing for   I7/temp2: 2.31n 2.31n
# timing for   I7/temp3: 2.09n 2.09n


# ===  a311o, C1=0, A1=1, A2=1, B1=0 ===
spice[ 562] = pfet(1.00, "7_I8" ,      "Vdd",    "I8/A1", "I8/temp0")           # Max size: 71.979
spice[ 556] = pfet(1.00, "1_I8" ,      "Vdd",    "I8/A2", "I8/temp0")           # Max size: 33.669
spice[ 564] = pfet(1.00, "9_I8" ,      "Vdd",    "I8/A3", "I8/temp0")
spice[ 566] = pfet(1.00, "11_I8", "I8/temp3",    "I8/B1", "I8/temp0")           # Max size: 266.571
spice[ 555] = pfet(1.00, "0_I8" , "I8/temp3",    "I8/C1", "I8/temp2")           # Max size: 178.637
spice[ 561] = pfet(2.00, "6_I8" ,      "Vdd", "I8/temp2",     "I8/X")
spice[ 559] = nfet(0.65, "4_I8" , "I8/temp2",    "I8/A1", "I8/temp1")           # Max size: 122.471
spice[ 558] = nfet(0.65, "3_I8" , "I8/temp4",    "I8/A2", "I8/temp1")           # Max size: 57.287
spice[ 560] = nfet(0.65, "5_I8" ,     "Vgnd",    "I8/A3", "I8/temp4")
spice[ 557] = nfet(0.65, "2_I8" ,     "Vgnd",    "I8/B1", "I8/temp2")           # Max size: 453.565
spice[ 565] = nfet(0.65, "10_I8",     "Vgnd",    "I8/C1", "I8/temp2")           # Max size: 303.947
spice[ 563] = nfet(1.30, "8_I8" ,     "Vgnd", "I8/temp2",     "I8/X")
# timing for      I8/A1:
# timing for      I8/A2:
# timing for      I8/A3: 2.44n 2.44n
# timing for      I8/B1:
# timing for      I8/C1:
# timing for       I8/X: 2.87n 2.87n
# timing for   I8/temp0: 2.49n 2.49n
# timing for   I8/temp1: 2.82n 2.82n
# timing for   I8/temp2: 2.78n 2.78n
# timing for   I8/temp3: 2.52n 2.52n
# timing for   I8/temp4: 2.83n 2.83n


# ===  a221oi, B2=1, C1=0, A1=1, B1=0 ===
spice[ 657] = pfet(2.00, "6_I9" ,      "Vdd", "I9/A1", "I9/temp1")              # Max size: 71.979
spice[ 653] = pfet(2.00, "2_I9" ,      "Vdd", "I9/A2", "I9/temp1")
spice[ 652] = pfet(2.00, "1_I9" , "I9/temp1", "I9/B1", "I9/temp0")              # Max size: 292.19
spice[ 656] = pfet(2.00, "5_I9" , "I9/temp1", "I9/B2", "I9/temp0")              # Max size: 111.568
spice[ 660] = pfet(2.00, "9_I9" , "I9/temp0", "I9/C1",     "I9/Y")              # Max size: 289.421
spice[ 655] = nfet(1.30, "4_I9" , "I9/temp2", "I9/A1",     "I9/Y")              # Max size: 122.471
spice[ 658] = nfet(1.30, "7_I9" ,     "Vgnd", "I9/A2", "I9/temp2")
spice[ 651] = nfet(1.30, "0_I9" , "I9/temp3", "I9/B1",     "I9/Y")              # Max size: 497.154
spice[ 654] = nfet(1.30, "3_I9" ,     "Vgnd", "I9/B2", "I9/temp3")              # Max size: 189.831
spice[ 661] = nfet(1.30, "10_I9",     "Vgnd", "I9/C1",     "I9/Y")              # Max size: 492.442
# timing for      I9/A1:
# timing for      I9/A2: 2.92n 2.92n
# timing for      I9/B1:
# timing for      I9/B2:
# timing for      I9/C1:
# timing for       I9/Y: 3.23n 3.23n
# timing for   I9/temp0: 3.02n 3.02n
# timing for   I9/temp1: 2.98n 2.98n
# timing for   I9/temp2: 3.24n 3.24n
# timing for   I9/temp3:


# ===  or4, D=0, C=0, B=0 ===
spice[ 758] = pfet(0.42, "3_I10",       "Vdd",     "I10/A", "I10/temp3")
spice[ 757] = pfet(0.42, "2_I10", "I10/temp3",     "I10/B", "I10/temp1")        # Max size: 139.517
spice[ 760] = pfet(0.42, "5_I10", "I10/temp2",     "I10/C", "I10/temp1")        # Max size: 129.362
spice[ 763] = pfet(0.42, "8_I10", "I10/temp2",     "I10/D", "I10/temp0")        # Max size: 98.397
spice[ 761] = pfet(1.00, "6_I10",       "Vdd", "I10/temp0",     "I10/X")
spice[ 764] = nfet(0.42, "9_I10",      "Vgnd",     "I10/A", "I10/temp0")
spice[ 755] = nfet(0.42, "0_I10",      "Vgnd",     "I10/B", "I10/temp0")        # Max size: 237.385
spice[ 762] = nfet(0.42, "7_I10",      "Vgnd",     "I10/C", "I10/temp0")        # Max size: 220.106
spice[ 756] = nfet(0.42, "1_I10",      "Vgnd",     "I10/D", "I10/temp0")        # Max size: 167.42
spice[ 759] = nfet(0.65, "4_I10",      "Vgnd", "I10/temp0",     "I10/X")
# timing for      I10/A: 3.24n 3.24n
# timing for      I10/B:
# timing for      I10/C:
# timing for      I10/D:
# timing for      I10/X: 3.44n 3.44n
# timing for  I10/temp0: 3.34n 3.34n
# timing for  I10/temp1: 5.49n 5.49n
# timing for  I10/temp2: 4.59n 4.59n
# timing for  I10/temp3: 5.84n 5.84n


# ===  a21oi, A2=1, B1=0 ===
spice[ 825] = pfet(2.00, "5_I11" ,       "Vdd", "I11/A1", "I11/temp2")
spice[ 827] = pfet(2.00, "7_I11" ,       "Vdd", "I11/A2", "I11/temp2")          # Max size: 115.436
spice[ 824] = pfet(2.00, "4_I11" , "I11/temp2", "I11/B1",     "I11/Y")          # Max size: 180.253
spice[ 822] = nfet(0.65, "2_I11" , "I11/temp1", "I11/A1",     "I11/Y")
spice[ 830] = nfet(0.65, "10_I11", "I11/temp0", "I11/A1",     "I11/Y")
spice[ 820] = nfet(0.65, "0_I11" ,      "Vgnd", "I11/A2", "I11/temp0")          # Max size: 196.412
spice[ 823] = nfet(0.65, "3_I11" ,      "Vgnd", "I11/A2", "I11/temp1")          # Max size: 196.412
spice[ 821] = nfet(1.30, "1_I11" ,      "Vgnd", "I11/B1",     "I11/Y")          # Max size: 306.696
# timing for     I11/A1: 3.46n 3.46n
# timing for     I11/A2:
# timing for     I11/B1:
# timing for      I11/Y: 3.56n 3.56n
# timing for  I11/temp0:
# timing for  I11/temp1:
# timing for  I11/temp2: 4.12n 4.12n


# ===  o211a, A2=0, C1=1, B1=1 ===
spice[ 896] = pfet(1.00, "5_I12",       "Vdd",    "I12/A1", "I12/temp0")
spice[ 895] = pfet(1.00, "4_I12", "I12/temp2",    "I12/A2", "I12/temp0")        # Max size: 256.186
spice[ 894] = pfet(1.00, "3_I12",       "Vdd",    "I12/B1", "I12/temp2")        # Max size: 96.296
spice[ 893] = pfet(1.00, "2_I12",       "Vdd",    "I12/C1", "I12/temp2")        # Max size: 194.476
spice[ 898] = pfet(1.00, "7_I12",       "Vdd", "I12/temp2",     "I12/X")
spice[ 891] = nfet(0.65, "0_I12",      "Vgnd",    "I12/A1", "I12/temp3")
spice[ 900] = nfet(0.65, "9_I12",      "Vgnd",    "I12/A2", "I12/temp3")        # Max size: 435.893
spice[ 892] = nfet(0.65, "1_I12", "I12/temp3",    "I12/B1", "I12/temp1")        # Max size: 163.845
spice[ 897] = nfet(0.65, "6_I12", "I12/temp2",    "I12/C1", "I12/temp1")        # Max size: 330.896
spice[ 899] = nfet(0.65, "8_I12",      "Vgnd", "I12/temp2",     "I12/X")
# timing for     I12/A1: 3.61n 3.61n
# timing for     I12/A2:
# timing for     I12/B1:
# timing for     I12/C1:
# timing for      I12/X: 3.90n 3.90n
# timing for  I12/temp0: 3.65n 3.65n
# timing for  I12/temp1: 3.85n 3.85n
# timing for  I12/temp2: 3.81n 3.81n
# timing for  I12/temp3: 3.87n 3.87n


# ===  a41o, A3=1, A4=1, A2=1, B1=0 ===
spice[ 982] = pfet(1.00, "5_I13" ,       "Vdd",    "I13/A1", "I13/temp0")
spice[ 980] = pfet(1.00, "3_I13" ,       "Vdd",    "I13/A2", "I13/temp0")       # Max size: 231.566
spice[ 979] = pfet(1.00, "2_I13" ,       "Vdd",    "I13/A3", "I13/temp0")       # Max size: 155.502
spice[ 981] = pfet(1.00, "4_I13" ,       "Vdd",    "I13/A4", "I13/temp0")       # Max size: 143.006
spice[ 984] = pfet(1.00, "7_I13" , "I13/temp3",    "I13/B1", "I13/temp0")       # Max size: 454.441
spice[ 985] = pfet(1.00, "8_I13" ,       "Vdd", "I13/temp3",     "I13/X")
spice[ 983] = nfet(0.65, "6_I13" , "I13/temp3",    "I13/A1", "I13/temp2")
spice[ 977] = nfet(0.65, "0_I13" , "I13/temp2",    "I13/A2", "I13/temp1")       # Max size: 394.005
spice[ 988] = nfet(0.65, "11_I13", "I13/temp4",    "I13/A3", "I13/temp1")       # Max size: 264.582
spice[ 978] = nfet(0.65, "1_I13" ,      "Vgnd",    "I13/A4", "I13/temp4")       # Max size: 243.321
spice[ 986] = nfet(0.65, "9_I13" ,      "Vgnd",    "I13/B1", "I13/temp3")       # Max size: 773.22
spice[ 987] = nfet(0.65, "10_I13",      "Vgnd", "I13/temp3",     "I13/X")
# timing for     I13/A1: 3.95n 3.95n
# timing for     I13/A2:
# timing for     I13/A3:
# timing for     I13/A4:
# timing for     I13/B1:
# timing for      I13/X: 4.19n 4.19n
# timing for  I13/temp0: 4.01n 4.01n
# timing for  I13/temp1:
# timing for  I13/temp2:
# timing for  I13/temp3: 4.12n 4.12n
# timing for  I13/temp4:


# ===  a21oi, A2=1, B1=0 ===
spice[1061] = pfet(2.00, "5_I14" ,       "Vdd", "I14/A1", "I14/temp2")
spice[1063] = pfet(2.00, "7_I14" ,       "Vdd", "I14/A2", "I14/temp2")          # Max size: 166.609
spice[1060] = pfet(2.00, "4_I14" , "I14/temp2", "I14/B1",     "I14/Y")          # Max size: 598.228
spice[1058] = nfet(0.65, "2_I14" , "I14/temp1", "I14/A1",     "I14/Y")
spice[1066] = nfet(0.65, "10_I14", "I14/temp0", "I14/A1",     "I14/Y")
spice[1056] = nfet(0.65, "0_I14" ,      "Vgnd", "I14/A2", "I14/temp0")          # Max size: 283.481
spice[1059] = nfet(0.65, "3_I14" ,      "Vgnd", "I14/A2", "I14/temp1")          # Max size: 283.481
spice[1057] = nfet(1.30, "1_I14" ,      "Vgnd", "I14/B1",     "I14/Y")          # Max size: 1017.87
# timing for     I14/A1: 4.23n 4.23n
# timing for     I14/A2:
# timing for     I14/B1:
# timing for      I14/Y: 4.41n 4.41n
# timing for  I14/temp0:
# timing for  I14/temp1:
# timing for  I14/temp2: 4.27n 4.27n


# ===  nand2b, B=1 ===
spice[1120] = pfet(0.42, "5_I15",       "Vdd",   "I15/A_N", "I15/temp1")
spice[1119] = pfet(1.00, "4_I15",       "Vdd",     "I15/B",     "I15/Y")        # Max size: 222.145
spice[1118] = pfet(1.00, "3_I15",       "Vdd", "I15/temp1",     "I15/Y")
spice[1115] = nfet(0.42, "0_I15",      "Vgnd",   "I15/A_N", "I15/temp1")
spice[1117] = nfet(0.65, "2_I15",      "Vgnd",     "I15/B", "I15/temp0")        # Max size: 377.975
spice[1116] = nfet(0.65, "1_I15", "I15/temp0", "I15/temp1",     "I15/Y")
# timing for    I15/A_N: 4.42n 4.42n
# timing for      I15/B:
# timing for      I15/Y: 4.59n 4.59n
# timing for  I15/temp0:
# timing for  I15/temp1: 4.48n 4.48n


# ===  nor2, B=0 ===
spice[1159] = pfet(1.00, "0_I16",       "Vdd", "I16/A", "I16/temp0")
spice[1161] = pfet(1.00, "2_I16", "I16/temp0", "I16/B",     "I16/Y")            # Max size: 286.074
spice[1160] = nfet(0.65, "1_I16",      "Vgnd", "I16/A",     "I16/Y")
spice[1162] = nfet(0.65, "3_I16",      "Vgnd", "I16/B",     "I16/Y")            # Max size: 486.748
# timing for      I16/A: 4.63n 4.63n
# timing for      I16/B:
# timing for      I16/Y: 4.73n 4.73n
# timing for  I16/temp0: 5.05n 5.05n


# ===  a311o, A3=1, C1=0, A1=1, B1=0 ===
spice[1224] = pfet(1.00, "10_I17",       "Vdd",    "I17/A1", "I17/temp4")       # Max size: 71.979
spice[1223] = pfet(1.00, "9_I17" ,       "Vdd",    "I17/A2", "I17/temp4")
spice[1222] = pfet(1.00, "8_I17" ,       "Vdd",    "I17/A3", "I17/temp4")       # Max size: 242.971
spice[1220] = pfet(1.00, "6_I17" , "I17/temp4",    "I17/B1", "I17/temp0")       # Max size: 741.092
spice[1219] = pfet(1.00, "5_I17" , "I17/temp1",    "I17/C1", "I17/temp0")       # Max size: 726.551
spice[1221] = pfet(1.00, "7_I17" ,       "Vdd", "I17/temp1",     "I17/X")
spice[1218] = nfet(0.65, "4_I17" , "I17/temp3",    "I17/A1", "I17/temp1")       # Max size: 122.471
spice[1216] = nfet(0.65, "2_I17" , "I17/temp3",    "I17/A2", "I17/temp2")
spice[1215] = nfet(0.65, "1_I17" ,      "Vgnd",    "I17/A3", "I17/temp2")       # Max size: 413.41
spice[1217] = nfet(0.65, "3_I17" ,      "Vgnd",    "I17/B1", "I17/temp1")       # Max size: 1260.95
spice[1214] = nfet(0.65, "0_I17" ,      "Vgnd",    "I17/C1", "I17/temp1")       # Max size: 1236.21
spice[1225] = nfet(0.65, "11_I17",      "Vgnd", "I17/temp1",     "I17/X")
# timing for     I17/A1:
# timing for     I17/A2: 4.76n 4.76n
# timing for     I17/A3:
# timing for     I17/B1:
# timing for     I17/C1:
# timing for      I17/X: 5.11n 5.11n
# timing for  I17/temp0: 4.84n 4.84n
# timing for  I17/temp1: 5.02n 5.02n
# timing for  I17/temp2:
# timing for  I17/temp3: 5.03n 5.03n
# timing for  I17/temp4: 4.80n 4.80n


# ===  a21o, A2=1, B1=0 ===
spice[1301] = pfet(1.00, "3_I18",       "Vdd",    "I18/A1", "I18/temp0")
spice[1304] = pfet(1.00, "6_I18",       "Vdd",    "I18/A2", "I18/temp0")        # Max size: 148.907
spice[1299] = pfet(1.00, "1_I18", "I18/temp2",    "I18/B1", "I18/temp0")        # Max size: 729.552
spice[1300] = pfet(1.00, "2_I18",       "Vdd", "I18/temp2",     "I18/X")
spice[1305] = nfet(0.65, "7_I18", "I18/temp2",    "I18/A1", "I18/temp1")
spice[1303] = nfet(0.65, "5_I18",      "Vgnd",    "I18/A2", "I18/temp1")        # Max size: 253.361
spice[1298] = nfet(0.65, "0_I18",      "Vgnd",    "I18/B1", "I18/temp2")        # Max size: 1241.315
spice[1302] = nfet(0.65, "4_I18",      "Vgnd", "I18/temp2",     "I18/X")
# timing for     I18/A1: 5.12n 5.12n
# timing for     I18/A2:
# timing for     I18/B1:
# timing for      I18/X: 5.33n 5.33n
# timing for  I18/temp0: 5.17n 5.17n
# timing for  I18/temp1:
# timing for  I18/temp2: 5.26n 5.26n


# ===  o21a, A2=1, A1=1 ===
spice[1362] = pfet(1.00, "0_I19",       "Vdd",    "I19/A1", "I19/temp2")        # Max size: 71.979
spice[1368] = pfet(1.00, "6_I19", "I19/temp2",    "I19/A2", "I19/temp1")        # Max size: 323.301
spice[1367] = pfet(1.00, "5_I19",       "Vdd",    "I19/B1", "I19/temp1")
spice[1366] = pfet(1.00, "4_I19",       "Vdd", "I19/temp1",     "I19/X")
spice[1364] = nfet(0.65, "2_I19",      "Vgnd",    "I19/A1", "I19/temp0")        # Max size: 122.471
spice[1365] = nfet(0.65, "3_I19",      "Vgnd",    "I19/A2", "I19/temp0")        # Max size: 550.088
spice[1363] = nfet(0.65, "1_I19", "I19/temp1",    "I19/B1", "I19/temp0")
spice[1369] = nfet(0.65, "7_I19",      "Vgnd", "I19/temp1",     "I19/X")
# timing for     I19/A1:
# timing for     I19/A2:
# timing for     I19/B1: 5.36n 5.36n
# timing for      I19/X: 5.48n 5.48n
# timing for  I19/temp0:
# timing for  I19/temp1: 5.44n 5.44n
# timing for  I19/temp2:


# ===  a21oi, A2=0, A1=1 ===
spice[1428] = pfet(1.00, "3_I20",       "Vdd", "I20/A1", "I20/temp1")           # Max size: 71.979
spice[1426] = pfet(1.00, "1_I20",       "Vdd", "I20/A2", "I20/temp1")           # Max size: 826.949
spice[1429] = pfet(1.00, "4_I20", "I20/temp1", "I20/B1",     "I20/Y")
spice[1425] = nfet(0.65, "0_I20", "I20/temp0", "I20/A1",     "I20/Y")           # Max size: 122.471
spice[1430] = nfet(0.65, "5_I20",      "Vgnd", "I20/A2", "I20/temp0")           # Max size: 1407.033
spice[1427] = nfet(0.65, "2_I20",      "Vgnd", "I20/B1",     "I20/Y")
# timing for     I20/A1:
# timing for     I20/A2:
# timing for     I20/B1: 5.49n 5.49n
# timing for      I20/Y: 5.65n 5.65n
# timing for  I20/temp0: 5.66n 5.66n
# timing for  I20/temp1:


# ===  xnor2, B=0 ===
spice[1474] = pfet(1.00, "0_I21",       "Vdd",     "I21/A", "I21/temp3")
spice[1480] = pfet(1.00, "6_I21",       "Vdd",     "I21/A", "I21/temp2")
spice[1475] = pfet(1.00, "1_I21",       "Vdd",     "I21/B", "I21/temp2")        # Max size: 411.859
spice[1482] = pfet(1.00, "8_I21", "I21/temp3",     "I21/B",     "I21/Y")        # Max size: 411.859
spice[1481] = pfet(1.00, "7_I21",       "Vdd", "I21/temp2",     "I21/Y")
spice[1479] = nfet(0.65, "5_I21",      "Vgnd",     "I21/A", "I21/temp1")
spice[1483] = nfet(0.65, "9_I21",      "Vgnd",     "I21/A", "I21/temp0")
spice[1476] = nfet(0.65, "2_I21", "I21/temp2",     "I21/B", "I21/temp1")        # Max size: 700.768
spice[1477] = nfet(0.65, "3_I21",      "Vgnd",     "I21/B", "I21/temp0")        # Max size: 700.768
spice[1478] = nfet(0.65, "4_I21", "I21/temp0", "I21/temp2",     "I21/Y")
# timing for      I21/A: 5.66n 5.66n
# timing for      I21/B:
# timing for      I21/Y: 5.76n 5.76n
# timing for  I21/temp0: 5.68n 5.68n
# timing for  I21/temp1:
# timing for  I21/temp2:
# timing for  I21/temp3: 6.09n 6.09n


# ===  a22o, A2=0, B2=1, A1=1 ===
spice[1542] = pfet(1.00, "5_I22",       "Vdd",    "I22/A1", "I22/temp1")        # Max size: 71.979
spice[1537] = pfet(1.00, "0_I22",       "Vdd",    "I22/A2", "I22/temp1")        # Max size: 114.13
spice[1541] = pfet(1.00, "4_I22", "I22/temp1",    "I22/B1", "I22/temp0")
spice[1545] = pfet(1.00, "8_I22", "I22/temp1",    "I22/B2", "I22/temp0")        # Max size: 382.407
spice[1540] = pfet(1.00, "3_I22",       "Vdd", "I22/temp0",     "I22/X")
spice[1543] = nfet(0.65, "6_I22", "I22/temp2",    "I22/A1", "I22/temp0")        # Max size: 122.471
spice[1539] = nfet(0.65, "2_I22",      "Vgnd",    "I22/A2", "I22/temp2")        # Max size: 194.189
spice[1538] = nfet(0.65, "1_I22", "I22/temp3",    "I22/B1", "I22/temp0")
spice[1546] = nfet(0.65, "9_I22",      "Vgnd",    "I22/B2", "I22/temp3")        # Max size: 650.656
spice[1544] = nfet(0.65, "7_I22",      "Vgnd", "I22/temp0",     "I22/X")
# timing for     I22/A1:
# timing for     I22/A2:
# timing for     I22/B1: 5.77n 5.77n
# timing for     I22/B2:
# timing for      I22/X: 5.95n 5.95n
# timing for  I22/temp0: 5.90n 5.90n
# timing for  I22/temp1:
# timing for  I22/temp2: 5.91n 5.91n
# timing for  I22/temp3:


# ===  a21o, A1=1, B1=0 ===
spice[1610] = pfet(1.00, "3_I23",       "Vdd",    "I23/A1", "I23/temp0")        # Max size: 71.979
spice[1613] = pfet(1.00, "6_I23",       "Vdd",    "I23/A2", "I23/temp0")
spice[1608] = pfet(1.00, "1_I23", "I23/temp2",    "I23/B1", "I23/temp0")        # Max size: 868.031
spice[1609] = pfet(1.00, "2_I23",       "Vdd", "I23/temp2",     "I23/X")
spice[1614] = nfet(0.65, "7_I23", "I23/temp2",    "I23/A1", "I23/temp1")        # Max size: 122.471
spice[1612] = nfet(0.65, "5_I23",      "Vgnd",    "I23/A2", "I23/temp1")
spice[1607] = nfet(0.65, "0_I23",      "Vgnd",    "I23/B1", "I23/temp2")        # Max size: 1476.933
spice[1611] = nfet(0.65, "4_I23",      "Vgnd", "I23/temp2",     "I23/X")
# timing for     I23/A1:
# timing for     I23/A2: 5.95n 5.95n
# timing for     I23/B1:
# timing for      I23/X: 6.13n 6.13n
# timing for  I23/temp0: 5.99n 5.99n
# timing for  I23/temp1: 6.10n 6.10n
# timing for  I23/temp2: 6.09n 6.09n


# ===  and2, A=1 ===
spice[1667] = pfet(0.42, "3_I24",       "Vdd",     "I24/A", "I24/temp1")        # Max size: 0.0
spice[1664] = pfet(0.42, "0_I24",       "Vdd",     "I24/B", "I24/temp1")
spice[1665] = pfet(1.00, "1_I24",       "Vdd", "I24/temp1",     "I24/X")
spice[1669] = nfet(0.42, "5_I24", "I24/temp1",     "I24/A", "I24/temp0")        # Max size: 0.0
spice[1666] = nfet(0.42, "2_I24",      "Vgnd",     "I24/B", "I24/temp0")
spice[1668] = nfet(0.65, "4_I24",      "Vgnd", "I24/temp1",     "I24/X")
# timing for      I24/A:
# timing for      I24/B: 6.14n 6.14n
# timing for      I24/X: 6.31n 6.31n
# timing for  I24/temp0: 6.26n 6.26n
# timing for  I24/temp1: 6.24n 6.24n


# ===  dfxtp ===
spice[1708] = pfet(0.42, "5_I25" ,       "Vdd",     "I25/D", "I25/temp10")
spice[1707] = pfet(1.00, "4_I25" ,       "Vdd", "I25/temp1",      "I25/Q")
spice[1720] = pfet(0.42, "17_I25",       "Vdd", "I25/temp1",  "I25/temp5")
spice[1710] = pfet(1.00, "7_I25" ,       "Vdd", "I25/temp2",  "I25/temp1")
spice[1705] = pfet(0.42, "2_I25" , "I25/temp6", "I25/temp3",  "I25/temp4")
spice[1718] = pfet(0.42, "15_I25", "I25/temp8", "I25/temp3",  "I25/temp2")
spice[1722] = pfet(0.64, "19_I25",       "Vdd", "I25/temp3",  "I25/temp9")
spice[1714] = pfet(0.75, "11_I25",       "Vdd", "I25/temp6",  "I25/temp8")
spice[1712] = pfet(0.42, "9_I25" ,       "Vdd", "I25/temp8",  "I25/temp4")
spice[1711] = pfet(0.42, "8_I25" , "I25/temp6", "I25/temp9", "I25/temp10")
spice[1715] = pfet(0.42, "12_I25", "I25/temp5", "I25/temp9",  "I25/temp2")
spice[1706] = pfet(0.64, "3_I25" ,       "Vdd",       "clk",  "I25/temp3")
spice[1725] = nfet(0.42, "22_I25",      "Vgnd",     "I25/D", "I25/temp10")
spice[1703] = nfet(0.65, "0_I25" ,      "Vgnd", "I25/temp1",      "I25/Q")
spice[1716] = nfet(0.42, "13_I25",      "Vgnd", "I25/temp1",  "I25/temp0")
spice[1724] = nfet(0.65, "21_I25",      "Vgnd", "I25/temp2",  "I25/temp1")
spice[1717] = nfet(0.42, "14_I25",      "Vgnd", "I25/temp3",  "I25/temp9")
spice[1721] = nfet(0.36, "18_I25", "I25/temp2", "I25/temp3",  "I25/temp0")
spice[1723] = nfet(0.36, "20_I25", "I25/temp6", "I25/temp3", "I25/temp10")
spice[1713] = nfet(0.64, "10_I25",      "Vgnd", "I25/temp6",  "I25/temp8")
spice[1709] = nfet(0.42, "6_I25" ,      "Vgnd", "I25/temp8",  "I25/temp7")
spice[1704] = nfet(0.36, "1_I25" , "I25/temp8", "I25/temp9",  "I25/temp2")
spice[1719] = nfet(0.36, "16_I25", "I25/temp7", "I25/temp9",  "I25/temp6")
spice[1726] = nfet(0.42, "23_I25",      "Vgnd",       "clk",  "I25/temp3")
# timing for      I25/D: 6.33n 6.33n
# timing for      I25/Q: 0.39n 0.39n
# timing for  I25/temp0:
# timing for  I25/temp1: 0.35n 0.35n
# timing for I25/temp10: 6.39n 6.39n
# timing for  I25/temp2: 0.30n 0.30n
# timing for  I25/temp3: 0.18n 0.18n
# timing for  I25/temp4: 0.56n 0.56n
# timing for  I25/temp5: 0.38n 0.38n
# timing for  I25/temp6:
# timing for  I25/temp7:
# timing for  I25/temp8:
# timing for  I25/temp9: 0.26n 0.26n
# timing for        clk: 0.10n 0.10n




spice[1854] = ""

for name in timings_to_track:
    spice.insert(1854+1, f"meas tran fall_{name} when V({name}) = 0.9")
spice.insert(1854+1,"run")
spice.insert(1854+1,"reset")
spice.insert(1854+1, "alterparam v_start=0")
spice.insert(1854+1, "alterparam v_q_ic=1.8")

for name in timings_to_track:
    spice.insert(1854+1, f"meas tran rise_{name} when V({name}) = 0.9")
spice.insert(1854+1, "run")
spice.insert(1854+1, "alterparam v_start=1.8")
spice.insert(1854+1, "alterparam v_q_ic=0")

spice = "\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
    