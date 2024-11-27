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
# === dfxtp ===
spice[  18] = nfet(0.65, "0_I0", "I0/Q", "I0/temp1", "Vgnd")
spice[  19] = nfet(0.36, "1_I0", "I0/temp2", "I0/temp9", "I0/temp8")
spice[  20] = pfet(0.42, "2_I0", "I0/temp4", "I0/temp3", "I0/temp6")
spice[  21] = pfet(0.64, "3_I0", "Vdd", "clk", "I0/temp3")
spice[  22] = pfet(1.00, "4_I0", "I0/Q", "I0/temp1", "Vdd")
spice[  23] = pfet(0.42, "5_I0", "I0/temp10", "I0/D", "Vdd")
spice[  24] = nfet(0.42, "6_I0", "Vgnd", "I0/temp8", "I0/temp7")
spice[  25] = pfet(1.00, "7_I0", "Vdd", "I0/temp2", "I0/temp1")
spice[  26] = pfet(0.42, "8_I0", "I0/temp6", "I0/temp9", "I0/temp10")
spice[  27] = pfet(0.42, "9_I0", "Vdd", "I0/temp8", "I0/temp4")
spice[  28] = nfet(0.64, "10_I0", "I0/temp8", "I0/temp6", "Vgnd")
spice[  29] = pfet(0.75, "11_I0", "I0/temp8", "I0/temp6", "Vdd")
spice[  30] = pfet(0.42, "12_I0", "I0/temp5", "I0/temp9", "I0/temp2")
spice[  31] = nfet(0.42, "13_I0", "Vgnd", "I0/temp1", "I0/temp0")
spice[  32] = nfet(0.42, "14_I0", "I0/temp9", "I0/temp3", "Vgnd")
spice[  33] = pfet(0.42, "15_I0", "I0/temp2", "I0/temp3", "I0/temp8")
spice[  34] = nfet(0.36, "16_I0", "I0/temp7", "I0/temp9", "I0/temp6")
spice[  35] = pfet(0.42, "17_I0", "Vdd", "I0/temp1", "I0/temp5")
spice[  36] = nfet(0.36, "18_I0", "I0/temp0", "I0/temp3", "I0/temp2")
spice[  37] = pfet(0.64, "19_I0", "I0/temp9", "I0/temp3", "Vdd")
spice[  38] = nfet(0.36, "20_I0", "I0/temp6", "I0/temp3", "I0/temp10")
spice[  39] = nfet(0.65, "21_I0", "Vgnd", "I0/temp2", "I0/temp1")
spice[  40] = nfet(0.42, "22_I0", "I0/temp10", "I0/D", "Vgnd")
spice[  41] = nfet(0.42, "23_I0", "Vgnd", "clk", "I0/temp3")
# timing for   I0/temp7:
# timing for   I0/temp3:
# timing for   I0/temp9:
# timing for        clk:
# timing for   I0/temp8:
# timing for       I0/Q:
# timing for   I0/temp2:
# timing for   I0/temp0:
# timing for   I0/temp6:
# timing for   I0/temp5:
# timing for  I0/temp10:
# timing for   I0/temp4:
# timing for       I0/D:
# timing for   I0/temp1:


# === clkbuf ===
spice[ 116] = pfet(1.00, "0_I1", "Vdd", "I1/A", "I1/temp0")
spice[ 117] = nfet(0.42, "1_I1", "Vgnd", "I1/temp0", "I1/X")
spice[ 118] = nfet(0.42, "2_I1", "Vgnd", "I1/temp0", "I1/X")
spice[ 119] = pfet(1.00, "3_I1", "I1/X", "I1/temp0", "Vdd")
spice[ 120] = nfet(0.42, "4_I1", "I1/X", "I1/temp0", "Vgnd")
spice[ 121] = nfet(0.42, "5_I1", "Vgnd", "I1/A", "I1/temp0")
spice[ 122] = pfet(1.00, "6_I1", "Vdd", "I1/temp0", "I1/X")
spice[ 123] = nfet(0.42, "7_I1", "I1/X", "I1/temp0", "Vgnd")
spice[ 124] = pfet(1.00, "8_I1", "I1/X", "I1/temp0", "Vdd")
spice[ 125] = pfet(1.00, "9_I1", "Vdd", "I1/temp0", "I1/X")
# timing for   I1/temp0:
# timing for       I1/A:
# timing for       I1/X:


# === buf ===
spice[ 154] = pfet(1.00, "0_I2", "Vdd", "I2/temp0", "I2/X")
spice[ 155] = pfet(1.00, "1_I2", "I2/X", "I2/temp0", "Vdd")
spice[ 156] = pfet(1.00, "2_I2", "Vdd", "I2/temp0", "I2/X")
spice[ 157] = pfet(1.00, "3_I2", "I2/X", "I2/temp0", "Vdd")
spice[ 158] = nfet(0.65, "4_I2", "I2/X", "I2/temp0", "Vgnd")
spice[ 159] = nfet(0.65, "5_I2", "I2/X", "I2/temp0", "Vgnd")
spice[ 160] = nfet(0.65, "6_I2", "Vgnd", "I2/temp0", "I2/X")
spice[ 161] = nfet(0.65, "7_I2", "Vgnd", "I2/temp0", "I2/X")
spice[ 162] = pfet(1.00, "8_I2", "Vdd", "I2/A", "I2/temp0")
spice[ 163] = nfet(0.65, "9_I2", "Vgnd", "I2/A", "I2/temp0")
# timing for       I2/X:
# timing for   I2/temp0:
# timing for       I2/A:


# === mux2 ===
spice[ 201] = pfet(0.42, "0_I3", "Vdd", "I3/temp5", "I3/temp3")
spice[ 202] = pfet(0.42, "1_I3", "I3/temp5", "I3/S", "Vdd")
spice[ 203] = pfet(0.42, "2_I3", "I3/temp4", "I3/S", "Vdd")
spice[ 204] = nfet(0.42, "3_I3", "Vgnd", "I3/temp5", "I3/temp0")
spice[ 205] = pfet(0.42, "4_I3", "I3/temp1", "I3/A0", "I3/temp4")      # Max size: 68.389
spice[ 206] = nfet(0.42, "5_I3", "I3/temp5", "I3/S", "Vgnd")
spice[ 207] = nfet(0.42, "6_I3", "I3/temp0", "I3/A0", "I3/temp1")      # Max size: 68.389
spice[ 208] = pfet(0.42, "7_I3", "I3/temp3", "I3/A1", "I3/temp1")      # Max size: 167.513
spice[ 209] = nfet(0.42, "8_I3", "I3/temp1", "I3/A1", "I3/temp2")      # Max size: 167.513
spice[ 210] = nfet(0.42, "9_I3", "I3/temp2", "I3/S", "Vgnd")
spice[ 211] = pfet(1.00, "10_I3", "Vdd", "I3/temp1", "I3/X")
spice[ 212] = nfet(0.65, "11_I3", "Vgnd", "I3/temp1", "I3/X")
# timing for      I3/A0:
# timing for       I3/S:
# timing for       I3/X:
# timing for   I3/temp5:
# timing for   I3/temp4:
# timing for   I3/temp0:
# timing for   I3/temp3:
# timing for   I3/temp1:
# timing for      I3/A1:
# timing for   I3/temp2:


# === mux2 ===
spice[ 272] = pfet(0.64, "0_I4", "Vdd", "I4/S", "I4/temp0")            # Max size: 58.459
spice[ 273] = pfet(0.64, "1_I4", "I4/temp0", "I4/A0", "I4/temp5")
spice[ 274] = pfet(1.00, "2_I4", "Vdd", "I4/temp5", "I4/X")
spice[ 275] = pfet(0.64, "3_I4", "I4/temp5", "I4/A1", "I4/temp2")      # Max size: 71.979
spice[ 276] = nfet(0.65, "4_I4", "Vgnd", "I4/temp5", "I4/X")
spice[ 277] = nfet(0.42, "5_I4", "Vgnd", "I4/S", "I4/temp3")           # Max size: 58.459
spice[ 278] = pfet(0.64, "6_I4", "I4/temp2", "I4/temp4", "Vdd")
spice[ 279] = nfet(0.42, "7_I4", "I4/temp5", "I4/A0", "I4/temp1")
spice[ 280] = nfet(0.42, "8_I4", "I4/temp1", "I4/temp4", "Vgnd")
spice[ 281] = nfet(0.42, "9_I4", "I4/temp4", "I4/S", "Vgnd")           # Max size: 58.459
spice[ 282] = nfet(0.42, "10_I4", "I4/temp3", "I4/A1", "I4/temp5")     # Max size: 71.979
spice[ 283] = pfet(1.00, "11_I4", "I4/X", "I4/temp5", "Vdd")
spice[ 284] = pfet(0.64, "12_I4", "I4/temp4", "I4/S", "Vdd")           # Max size: 58.459
spice[ 285] = nfet(0.65, "13_I4", "I4/X", "I4/temp5", "Vgnd")
# timing for      I4/A0:
# timing for   I4/temp2:
# timing for       I4/S:
# timing for   I4/temp3:
# timing for   I4/temp1:
# timing for   I4/temp5:
# timing for       I4/X:
# timing for   I4/temp0:
# timing for      I4/A1:
# timing for   I4/temp4:


# === xor2 ===
spice[ 340] = pfet(1.00, "0_I5", "I5/X", "I5/temp3", "I5/temp2")
spice[ 341] = nfet(0.65, "1_I5", "I5/X", "I5/B", "I5/temp1")
spice[ 342] = nfet(0.65, "2_I5", "I5/temp3", "I5/B", "Vgnd")
spice[ 343] = pfet(1.00, "3_I5", "I5/temp0", "I5/B", "I5/temp3")
spice[ 344] = pfet(1.00, "4_I5", "Vdd", "I5/B", "I5/temp2")
spice[ 345] = nfet(0.65, "5_I5", "Vgnd", "I5/A", "I5/temp3")           # Max size: 319.424
spice[ 346] = nfet(0.65, "6_I5", "Vgnd", "I5/temp3", "I5/X")
spice[ 347] = pfet(1.00, "7_I5", "I5/temp2", "I5/A", "Vdd")            # Max size: 319.424
spice[ 348] = pfet(1.00, "8_I5", "Vdd", "I5/A", "I5/temp0")            # Max size: 319.424
spice[ 349] = nfet(0.65, "9_I5", "I5/temp1", "I5/A", "Vgnd")           # Max size: 319.424
# timing for       I5/A:
# timing for       I5/B:
# timing for   I5/temp0:
# timing for   I5/temp1:
# timing for   I5/temp2:
# timing for       I5/X:
# timing for   I5/temp3:


# === a21o ===
spice[ 400] = nfet(0.65, "0_I6", "I6/temp2", "I6/B1", "Vgnd")          # Max size: 158.096
spice[ 401] = pfet(1.00, "1_I6", "I6/temp0", "I6/B1", "I6/temp2")      # Max size: 158.096
spice[ 402] = pfet(1.00, "2_I6", "Vdd", "I6/temp2", "I6/X")
spice[ 403] = pfet(1.00, "3_I6", "Vdd", "I6/A1", "I6/temp0")           # Max size: 71.979
spice[ 404] = nfet(0.65, "4_I6", "Vgnd", "I6/temp2", "I6/X")
spice[ 405] = nfet(0.65, "5_I6", "Vgnd", "I6/A2", "I6/temp1")
spice[ 406] = pfet(1.00, "6_I6", "I6/temp0", "I6/A2", "Vdd")
spice[ 407] = nfet(0.65, "7_I6", "I6/temp1", "I6/A1", "I6/temp2")      # Max size: 71.979
# timing for      I6/A1:
# timing for      I6/B1:
# timing for   I6/temp1:
# timing for   I6/temp2:
# timing for      I6/A2:
# timing for       I6/X:
# timing for   I6/temp0:


# === a211o ===
spice[ 470] = pfet(1.00, "0_I7", "Vdd", "I7/temp2", "I7/X")
spice[ 471] = pfet(1.00, "1_I7", "I7/temp2", "I7/C1", "I7/temp1")      # Max size: 96.012
spice[ 472] = pfet(1.00, "2_I7", "Vdd", "I7/A2", "I7/temp3")
spice[ 473] = nfet(0.65, "3_I7", "Vgnd", "I7/B1", "I7/temp2")          # Max size: 198.255
spice[ 474] = nfet(0.65, "4_I7", "Vgnd", "I7/temp2", "I7/X")
spice[ 475] = nfet(0.65, "5_I7", "I7/temp0", "I7/A2", "Vgnd")
spice[ 476] = pfet(1.00, "6_I7", "I7/temp3", "I7/A1", "Vdd")           # Max size: 35.989
spice[ 477] = nfet(0.65, "7_I7", "I7/temp2", "I7/A1", "I7/temp0")      # Max size: 35.989
spice[ 478] = pfet(1.00, "8_I7", "I7/temp1", "I7/B1", "I7/temp3")      # Max size: 198.255
spice[ 479] = nfet(0.65, "9_I7", "I7/temp2", "I7/C1", "Vgnd")          # Max size: 96.012
# timing for   I7/temp0:
# timing for   I7/temp1:
# timing for      I7/C1:
# timing for      I7/A2:
# timing for   I7/temp3:
# timing for   I7/temp2:
# timing for      I7/B1:
# timing for      I7/A1:
# timing for       I7/X:


# === a311o ===
spice[ 553] = pfet(1.00, "0_I8", "I8/temp2", "I8/C1", "I8/temp3")      # Max size: 178.637
spice[ 554] = pfet(1.00, "1_I8", "Vdd", "I8/A2", "I8/temp0")           # Max size: 33.669
spice[ 555] = nfet(0.65, "2_I8", "Vgnd", "I8/B1", "I8/temp2")          # Max size: 266.571
spice[ 556] = nfet(0.65, "3_I8", "I8/temp1", "I8/A2", "I8/temp4")      # Max size: 33.669
spice[ 557] = nfet(0.65, "4_I8", "I8/temp2", "I8/A1", "I8/temp1")      # Max size: 71.979
spice[ 558] = nfet(0.65, "5_I8", "I8/temp4", "I8/A3", "Vgnd")
spice[ 559] = pfet(1.00, "6_I8", "Vdd", "I8/temp2", "I8/X")
spice[ 560] = pfet(1.00, "7_I8", "I8/temp0", "I8/A1", "Vdd")           # Max size: 71.979
spice[ 561] = nfet(0.65, "8_I8", "Vgnd", "I8/temp2", "I8/X")
spice[ 562] = pfet(1.00, "9_I8", "I8/temp0", "I8/A3", "Vdd")
spice[ 563] = nfet(0.65, "10_I8", "I8/temp2", "I8/C1", "Vgnd")         # Max size: 178.637
spice[ 564] = pfet(1.00, "11_I8", "I8/temp3", "I8/B1", "I8/temp0")     # Max size: 266.571
spice[ 565] = pfet(1.00, "12_I8", "I8/X", "I8/temp2", "Vdd")
spice[ 566] = nfet(0.65, "13_I8", "I8/X", "I8/temp2", "Vgnd")
# timing for      I8/A1:
# timing for       I8/X:
# timing for      I8/A3:
# timing for      I8/C1:
# timing for   I8/temp2:
# timing for   I8/temp4:
# timing for      I8/B1:
# timing for   I8/temp1:
# timing for   I8/temp3:
# timing for      I8/A2:
# timing for   I8/temp0:


# === a221oi ===
spice[ 649] = nfet(0.65, "0_I9", "I9/Y", "I9/B1", "I9/temp3")          # Max size: 292.19
spice[ 650] = pfet(1.00, "1_I9", "I9/temp1", "I9/B1", "I9/temp0")      # Max size: 292.19
spice[ 651] = pfet(1.00, "2_I9", "I9/temp1", "I9/A2", "Vdd")
spice[ 652] = nfet(0.65, "3_I9", "Vgnd", "I9/B2", "I9/temp3")          # Max size: 111.568
spice[ 653] = nfet(0.65, "4_I9", "I9/Y", "I9/A1", "I9/temp2")          # Max size: 71.979
spice[ 654] = pfet(1.00, "5_I9", "I9/temp0", "I9/B2", "I9/temp1")      # Max size: 111.568
spice[ 655] = pfet(1.00, "6_I9", "Vdd", "I9/A1", "I9/temp1")           # Max size: 71.979
spice[ 656] = nfet(0.65, "7_I9", "Vgnd", "I9/A2", "I9/temp2")
spice[ 657] = pfet(1.00, "8_I9", "I9/temp1", "I9/A1", "Vdd")           # Max size: 71.979
spice[ 658] = pfet(1.00, "9_I9", "I9/Y", "I9/C1", "I9/temp0")          # Max size: 289.421
spice[ 659] = nfet(0.65, "10_I9", "Vgnd", "I9/C1", "I9/Y")             # Max size: 289.421
spice[ 660] = nfet(0.65, "11_I9", "I9/Y", "I9/C1", "Vgnd")             # Max size: 289.421
spice[ 661] = pfet(1.00, "12_I9", "Vdd", "I9/A2", "I9/temp1")
spice[ 662] = nfet(0.65, "13_I9", "I9/temp3", "I9/B2", "Vgnd")         # Max size: 111.568
spice[ 663] = nfet(0.65, "14_I9", "I9/temp3", "I9/B1", "I9/Y")         # Max size: 292.19
spice[ 664] = nfet(0.65, "15_I9", "I9/temp2", "I9/A2", "Vgnd")
spice[ 665] = pfet(1.00, "16_I9", "I9/temp0", "I9/C1", "I9/Y")         # Max size: 289.421
spice[ 666] = pfet(1.00, "17_I9", "I9/temp1", "I9/B2", "I9/temp0")     # Max size: 111.568
spice[ 667] = nfet(0.65, "18_I9", "I9/temp2", "I9/A1", "I9/Y")         # Max size: 71.979
spice[ 668] = pfet(1.00, "19_I9", "I9/temp0", "I9/B1", "I9/temp1")     # Max size: 292.19
# timing for      I9/C1:
# timing for   I9/temp2:
# timing for   I9/temp3:
# timing for   I9/temp1:
# timing for      I9/A1:
# timing for   I9/temp0:
# timing for       I9/Y:
# timing for      I9/B2:
# timing for      I9/A2:
# timing for      I9/B1:


# === or4 ===
spice[ 753] = nfet(0.42, "0_I10", "I10/temp0", "I10/B", "Vgnd")        # Max size: 139.517
spice[ 754] = nfet(0.42, "1_I10", "I10/temp0", "I10/D", "Vgnd")        # Max size: 98.397
spice[ 755] = pfet(0.42, "2_I10", "I10/temp3", "I10/B", "I10/temp1")   # Max size: 139.517
spice[ 756] = pfet(0.42, "3_I10", "Vdd", "I10/A", "I10/temp3")
spice[ 757] = nfet(0.65, "4_I10", "I10/X", "I10/temp0", "Vgnd")
spice[ 758] = pfet(0.42, "5_I10", "I10/temp1", "I10/C", "I10/temp2")   # Max size: 129.362
spice[ 759] = pfet(1.00, "6_I10", "I10/X", "I10/temp0", "Vdd")
spice[ 760] = nfet(0.42, "7_I10", "Vgnd", "I10/C", "I10/temp0")        # Max size: 129.362
spice[ 761] = pfet(0.42, "8_I10", "I10/temp2", "I10/D", "I10/temp0")   # Max size: 98.397
spice[ 762] = nfet(0.42, "9_I10", "Vgnd", "I10/A", "I10/temp0")
# timing for      I10/C:
# timing for  I10/temp3:
# timing for  I10/temp0:
# timing for      I10/B:
# timing for  I10/temp2:
# timing for  I10/temp1:
# timing for      I10/X:
# timing for      I10/D:
# timing for      I10/A:


# === a21oi ===
spice[ 818] = nfet(0.65, "0_I11", "Vgnd", "I11/A2", "I11/temp0")       # Max size: 115.436
spice[ 819] = nfet(0.65, "1_I11", "Vgnd", "I11/B1", "I11/Y")           # Max size: 180.253
spice[ 820] = nfet(0.65, "2_I11", "I11/Y", "I11/A1", "I11/temp1")
spice[ 821] = nfet(0.65, "3_I11", "I11/temp1", "I11/A2", "Vgnd")       # Max size: 115.436
spice[ 822] = pfet(1.00, "4_I11", "I11/temp2", "I11/B1", "I11/Y")      # Max size: 180.253
spice[ 823] = pfet(1.00, "5_I11", "I11/temp2", "I11/A1", "Vdd")
spice[ 824] = pfet(1.00, "6_I11", "I11/Y", "I11/B1", "I11/temp2")      # Max size: 180.253
spice[ 825] = pfet(1.00, "7_I11", "Vdd", "I11/A2", "I11/temp2")        # Max size: 115.436
spice[ 826] = pfet(1.00, "8_I11", "I11/temp2", "I11/A2", "Vdd")        # Max size: 115.436
spice[ 827] = pfet(1.00, "9_I11", "Vdd", "I11/A1", "I11/temp2")
spice[ 828] = nfet(0.65, "10_I11", "I11/temp0", "I11/A1", "I11/Y")
spice[ 829] = nfet(0.65, "11_I11", "I11/Y", "I11/B1", "Vgnd")          # Max size: 180.253
# timing for  I11/temp0:
# timing for     I11/A1:
# timing for  I11/temp1:
# timing for     I11/A2:
# timing for      I11/Y:
# timing for  I11/temp2:
# timing for     I11/B1:


# === o211a ===
spice[ 889] = nfet(0.65, "0_I12", "Vgnd", "I12/A1", "I12/temp3")
spice[ 890] = nfet(0.65, "1_I12", "I12/temp1", "I12/B1", "I12/temp3")  # Max size: 96.296
spice[ 891] = pfet(1.00, "2_I12", "I12/temp2", "I12/C1", "Vdd")        # Max size: 194.476
spice[ 892] = pfet(1.00, "3_I12", "Vdd", "I12/B1", "I12/temp2")        # Max size: 96.296
spice[ 893] = pfet(1.00, "4_I12", "I12/temp2", "I12/A2", "I12/temp0")  # Max size: 256.186
spice[ 894] = pfet(1.00, "5_I12", "I12/temp0", "I12/A1", "Vdd")
spice[ 895] = nfet(0.65, "6_I12", "I12/temp2", "I12/C1", "I12/temp1")  # Max size: 194.476
spice[ 896] = pfet(1.00, "7_I12", "Vdd", "I12/temp2", "I12/X")
spice[ 897] = nfet(0.65, "8_I12", "Vgnd", "I12/temp2", "I12/X")
spice[ 898] = nfet(0.65, "9_I12", "I12/temp3", "I12/A2", "Vgnd")       # Max size: 256.186
# timing for      I12/X:
# timing for  I12/temp0:
# timing for  I12/temp3:
# timing for  I12/temp1:
# timing for     I12/B1:
# timing for     I12/A2:
# timing for  I12/temp2:
# timing for     I12/A1:
# timing for     I12/C1:


# === a41o ===
spice[ 975] = nfet(0.65, "0_I13", "I13/temp1", "I13/A2", "I13/temp2")  # Max size: 231.566
spice[ 976] = nfet(0.65, "1_I13", "Vgnd", "I13/A4", "I13/temp4")       # Max size: 143.006
spice[ 977] = pfet(1.00, "2_I13", "Vdd", "I13/A3", "I13/temp0")        # Max size: 155.502
spice[ 978] = pfet(1.00, "3_I13", "I13/temp0", "I13/A2", "Vdd")        # Max size: 231.566
spice[ 979] = pfet(1.00, "4_I13", "I13/temp0", "I13/A4", "Vdd")        # Max size: 143.006
spice[ 980] = pfet(1.00, "5_I13", "Vdd", "I13/A1", "I13/temp0")
spice[ 981] = nfet(0.65, "6_I13", "I13/temp2", "I13/A1", "I13/temp3")
spice[ 982] = pfet(1.00, "7_I13", "I13/temp0", "I13/B1", "I13/temp3")  # Max size: 454.441
spice[ 983] = pfet(1.00, "8_I13", "Vdd", "I13/temp3", "I13/X")
spice[ 984] = nfet(0.65, "9_I13", "I13/temp3", "I13/B1", "Vgnd")       # Max size: 454.441
spice[ 985] = nfet(0.65, "10_I13", "Vgnd", "I13/temp3", "I13/X")
spice[ 986] = nfet(0.65, "11_I13", "I13/temp4", "I13/A3", "I13/temp1") # Max size: 155.502
# timing for  I13/temp3:
# timing for      I13/X:
# timing for  I13/temp0:
# timing for     I13/A2:
# timing for     I13/A3:
# timing for  I13/temp2:
# timing for     I13/B1:
# timing for  I13/temp4:
# timing for     I13/A1:
# timing for  I13/temp1:
# timing for     I13/A4:


# === a21oi ===
spice[1054] = nfet(0.65, "0_I14", "Vgnd", "I14/A2", "I14/temp0")       # Max size: 166.609
spice[1055] = nfet(0.65, "1_I14", "Vgnd", "I14/B1", "I14/Y")           # Max size: 598.228
spice[1056] = nfet(0.65, "2_I14", "I14/Y", "I14/A1", "I14/temp1")
spice[1057] = nfet(0.65, "3_I14", "I14/temp1", "I14/A2", "Vgnd")       # Max size: 166.609
spice[1058] = pfet(1.00, "4_I14", "I14/temp2", "I14/B1", "I14/Y")      # Max size: 598.228
spice[1059] = pfet(1.00, "5_I14", "I14/temp2", "I14/A1", "Vdd")
spice[1060] = pfet(1.00, "6_I14", "I14/Y", "I14/B1", "I14/temp2")      # Max size: 598.228
spice[1061] = pfet(1.00, "7_I14", "Vdd", "I14/A2", "I14/temp2")        # Max size: 166.609
spice[1062] = pfet(1.00, "8_I14", "I14/temp2", "I14/A2", "Vdd")        # Max size: 166.609
spice[1063] = pfet(1.00, "9_I14", "Vdd", "I14/A1", "I14/temp2")
spice[1064] = nfet(0.65, "10_I14", "I14/temp0", "I14/A1", "I14/Y")
spice[1065] = nfet(0.65, "11_I14", "I14/Y", "I14/B1", "Vgnd")          # Max size: 598.228
# timing for  I14/temp0:
# timing for     I14/A1:
# timing for  I14/temp1:
# timing for     I14/B1:
# timing for      I14/Y:
# timing for  I14/temp2:
# timing for     I14/A2:


# === nand2b ===
spice[1113] = nfet(0.42, "0_I15", "Vgnd", "I15/A_N", "I15/temp1")
spice[1114] = nfet(0.65, "1_I15", "I15/Y", "I15/temp1", "I15/temp0")
spice[1115] = nfet(0.65, "2_I15", "I15/temp0", "I15/B", "Vgnd")        # Max size: 222.145
spice[1116] = pfet(1.00, "3_I15", "Vdd", "I15/temp1", "I15/Y")
spice[1117] = pfet(1.00, "4_I15", "I15/Y", "I15/B", "Vdd")             # Max size: 222.145
spice[1118] = pfet(0.42, "5_I15", "Vdd", "I15/A_N", "I15/temp1")
# timing for      I15/Y:
# timing for  I15/temp1:
# timing for    I15/A_N:
# timing for  I15/temp0:
# timing for      I15/B:


# === nor2 ===
spice[1157] = pfet(1.00, "0_I16", "Vdd", "I16/A", "I16/temp0")
spice[1158] = nfet(0.65, "1_I16", "Vgnd", "I16/A", "I16/Y")
spice[1159] = pfet(1.00, "2_I16", "I16/temp0", "I16/B", "I16/Y")       # Max size: 286.074
spice[1160] = nfet(0.65, "3_I16", "I16/Y", "I16/B", "Vgnd")            # Max size: 286.074
# timing for      I16/B:
# timing for      I16/A:
# timing for  I16/temp0:
# timing for      I16/Y:


# === a311o ===
spice[1212] = nfet(0.65, "0_I17", "I17/temp1", "I17/C1", "Vgnd")       # Max size: 726.551
spice[1213] = nfet(0.65, "1_I17", "I17/temp2", "I17/A3", "Vgnd")       # Max size: 242.971
spice[1214] = nfet(0.65, "2_I17", "I17/temp3", "I17/A2", "I17/temp2")
spice[1215] = nfet(0.65, "3_I17", "Vgnd", "I17/B1", "I17/temp1")       # Max size: 741.092
spice[1216] = nfet(0.65, "4_I17", "I17/temp1", "I17/A1", "I17/temp3")  # Max size: 71.979
spice[1217] = pfet(1.00, "5_I17", "I17/temp1", "I17/C1", "I17/temp0")  # Max size: 726.551
spice[1218] = pfet(1.00, "6_I17", "I17/temp0", "I17/B1", "I17/temp4")  # Max size: 741.092
spice[1219] = pfet(1.00, "7_I17", "Vdd", "I17/temp1", "I17/X")
spice[1220] = pfet(1.00, "8_I17", "I17/temp4", "I17/A3", "Vdd")        # Max size: 242.971
spice[1221] = pfet(1.00, "9_I17", "Vdd", "I17/A2", "I17/temp4")
spice[1222] = pfet(1.00, "10_I17", "I17/temp4", "I17/A1", "Vdd")       # Max size: 71.979
spice[1223] = nfet(0.65, "11_I17", "Vgnd", "I17/temp1", "I17/X")
# timing for      I17/X:
# timing for  I17/temp1:
# timing for     I17/A1:
# timing for  I17/temp4:
# timing for  I17/temp2:
# timing for     I17/C1:
# timing for  I17/temp0:
# timing for     I17/B1:
# timing for     I17/A3:
# timing for     I17/A2:
# timing for  I17/temp3:


# === a21o ===
spice[1296] = nfet(0.65, "0_I18", "I18/temp2", "I18/B1", "Vgnd")       # Max size: 729.552
spice[1297] = pfet(1.00, "1_I18", "I18/temp0", "I18/B1", "I18/temp2")  # Max size: 729.552
spice[1298] = pfet(1.00, "2_I18", "Vdd", "I18/temp2", "I18/X")
spice[1299] = pfet(1.00, "3_I18", "Vdd", "I18/A1", "I18/temp0")
spice[1300] = nfet(0.65, "4_I18", "Vgnd", "I18/temp2", "I18/X")
spice[1301] = nfet(0.65, "5_I18", "Vgnd", "I18/A2", "I18/temp1")       # Max size: 148.907
spice[1302] = pfet(1.00, "6_I18", "I18/temp0", "I18/A2", "Vdd")        # Max size: 148.907
spice[1303] = nfet(0.65, "7_I18", "I18/temp1", "I18/A1", "I18/temp2")
# timing for     I18/A1:
# timing for  I18/temp1:
# timing for     I18/B1:
# timing for  I18/temp2:
# timing for     I18/A2:
# timing for      I18/X:
# timing for  I18/temp0:


# === o21a ===
spice[1359] = pfet(1.00, "0_I19", "Vdd", "I19/A1", "I19/temp2")        # Max size: 71.979
spice[1360] = nfet(0.65, "1_I19", "I19/temp0", "I19/B1", "I19/temp1")
spice[1361] = nfet(0.65, "2_I19", "I19/temp0", "I19/A1", "Vgnd")       # Max size: 71.979
spice[1362] = nfet(0.65, "3_I19", "Vgnd", "I19/A2", "I19/temp0")       # Max size: 323.301
spice[1363] = pfet(1.00, "4_I19", "Vdd", "I19/temp1", "I19/X")
spice[1364] = pfet(1.00, "5_I19", "I19/temp1", "I19/B1", "Vdd")
spice[1365] = pfet(1.00, "6_I19", "I19/temp2", "I19/A2", "I19/temp1")  # Max size: 323.301
spice[1366] = nfet(0.65, "7_I19", "Vgnd", "I19/temp1", "I19/X")
# timing for     I19/A2:
# timing for  I19/temp1:
# timing for      I19/X:
# timing for  I19/temp2:
# timing for     I19/B1:
# timing for     I19/A1:
# timing for  I19/temp0:


# === a21oi ===
spice[1422] = nfet(0.65, "0_I20", "I20/temp0", "I20/A1", "I20/Y")      # Max size: 71.979
spice[1423] = pfet(1.00, "1_I20", "I20/temp1", "I20/A2", "Vdd")        # Max size: 826.949
spice[1424] = nfet(0.65, "2_I20", "I20/Y", "I20/B1", "Vgnd")
spice[1425] = pfet(1.00, "3_I20", "Vdd", "I20/A1", "I20/temp1")        # Max size: 71.979
spice[1426] = pfet(1.00, "4_I20", "I20/temp1", "I20/B1", "I20/Y")
spice[1427] = nfet(0.65, "5_I20", "Vgnd", "I20/A2", "I20/temp0")       # Max size: 826.949
# timing for     I20/A2:
# timing for      I20/Y:
# timing for  I20/temp0:
# timing for     I20/A1:
# timing for  I20/temp1:
# timing for     I20/B1:


# === xnor2 ===
spice[1471] = pfet(1.00, "0_I21", "I21/temp3", "I21/A", "Vdd")
spice[1472] = pfet(1.00, "1_I21", "I21/temp2", "I21/B", "Vdd")         # Max size: 411.859
spice[1473] = nfet(0.65, "2_I21", "I21/temp1", "I21/B", "I21/temp2")   # Max size: 411.859
spice[1474] = nfet(0.65, "3_I21", "I21/temp0", "I21/B", "Vgnd")        # Max size: 411.859
spice[1475] = nfet(0.65, "4_I21", "I21/Y", "I21/temp2", "I21/temp0")
spice[1476] = nfet(0.65, "5_I21", "Vgnd", "I21/A", "I21/temp1")
spice[1477] = pfet(1.00, "6_I21", "Vdd", "I21/A", "I21/temp2")
spice[1478] = pfet(1.00, "7_I21", "Vdd", "I21/temp2", "I21/Y")
spice[1479] = pfet(1.00, "8_I21", "I21/Y", "I21/B", "I21/temp3")       # Max size: 411.859
spice[1480] = nfet(0.65, "9_I21", "I21/temp0", "I21/A", "Vgnd")
# timing for  I21/temp1:
# timing for      I21/A:
# timing for      I21/Y:
# timing for  I21/temp3:
# timing for  I21/temp2:
# timing for      I21/B:
# timing for  I21/temp0:


# === a22o ===
spice[1534] = pfet(1.00, "0_I22", "Vdd", "I22/A2", "I22/temp1")        # Max size: 114.13
spice[1535] = nfet(0.65, "1_I22", "I22/temp0", "I22/B1", "I22/temp3")
spice[1536] = nfet(0.65, "2_I22", "Vgnd", "I22/A2", "I22/temp2")       # Max size: 114.13
spice[1537] = pfet(1.00, "3_I22", "I22/X", "I22/temp0", "Vdd")
spice[1538] = pfet(1.00, "4_I22", "I22/temp0", "I22/B1", "I22/temp1")
spice[1539] = pfet(1.00, "5_I22", "I22/temp1", "I22/A1", "Vdd")        # Max size: 71.979
spice[1540] = nfet(0.65, "6_I22", "I22/temp2", "I22/A1", "I22/temp0")  # Max size: 71.979
spice[1541] = nfet(0.65, "7_I22", "I22/X", "I22/temp0", "Vgnd")
spice[1542] = pfet(1.00, "8_I22", "I22/temp1", "I22/B2", "I22/temp0")  # Max size: 382.407
spice[1543] = nfet(0.65, "9_I22", "I22/temp3", "I22/B2", "Vgnd")       # Max size: 382.407
# timing for     I22/B1:
# timing for  I22/temp0:
# timing for  I22/temp3:
# timing for     I22/B2:
# timing for      I22/X:
# timing for     I22/A2:
# timing for  I22/temp2:
# timing for     I22/A1:
# timing for  I22/temp1:


# === a21o ===
spice[1604] = nfet(0.65, "0_I23", "I23/temp2", "I23/B1", "Vgnd")       # Max size: 868.031
spice[1605] = pfet(1.00, "1_I23", "I23/temp0", "I23/B1", "I23/temp2")  # Max size: 868.031
spice[1606] = pfet(1.00, "2_I23", "Vdd", "I23/temp2", "I23/X")
spice[1607] = pfet(1.00, "3_I23", "Vdd", "I23/A1", "I23/temp0")        # Max size: 71.979
spice[1608] = nfet(0.65, "4_I23", "Vgnd", "I23/temp2", "I23/X")
spice[1609] = nfet(0.65, "5_I23", "Vgnd", "I23/A2", "I23/temp1")
spice[1610] = pfet(1.00, "6_I23", "I23/temp0", "I23/A2", "Vdd")
spice[1611] = nfet(0.65, "7_I23", "I23/temp1", "I23/A1", "I23/temp2")  # Max size: 71.979
# timing for     I23/B1:
# timing for     I23/A2:
# timing for  I23/temp1:
# timing for  I23/temp0:
# timing for  I23/temp2:
# timing for      I23/X:
# timing for     I23/A1:


# === and2 ===
spice[1662] = pfet(0.42, "0_I24", "Vdd", "I24/B", "I24/temp1")
spice[1663] = pfet(1.00, "1_I24", "I24/X", "I24/temp1", "Vdd")
spice[1664] = nfet(0.42, "2_I24", "Vgnd", "I24/B", "I24/temp0")
spice[1665] = pfet(0.42, "3_I24", "I24/temp1", "I24/A", "Vdd")         # Max size: 0.0
spice[1666] = nfet(0.65, "4_I24", "I24/X", "I24/temp1", "Vgnd")
spice[1667] = nfet(0.42, "5_I24", "I24/temp0", "I24/A", "I24/temp1")   # Max size: 0.0
# timing for      I24/X:
# timing for  I24/temp0:
# timing for      I24/A:
# timing for      I24/B:
# timing for  I24/temp1:


# === dfxtp ===
spice[1701] = nfet(0.65, "0_I25", "I25/Q", "I25/temp1", "Vgnd")
spice[1702] = nfet(0.36, "1_I25", "I25/temp2", "I25/temp9", "I25/temp8")
spice[1703] = pfet(0.42, "2_I25", "I25/temp4", "I25/temp3", "I25/temp6")
spice[1704] = pfet(0.64, "3_I25", "Vdd", "clk", "I25/temp3")
spice[1705] = pfet(1.00, "4_I25", "I25/Q", "I25/temp1", "Vdd")
spice[1706] = pfet(0.42, "5_I25", "I25/temp10", "I25/D", "Vdd")
spice[1707] = nfet(0.42, "6_I25", "Vgnd", "I25/temp8", "I25/temp7")
spice[1708] = pfet(1.00, "7_I25", "Vdd", "I25/temp2", "I25/temp1")
spice[1709] = pfet(0.42, "8_I25", "I25/temp6", "I25/temp9", "I25/temp10")
spice[1710] = pfet(0.42, "9_I25", "Vdd", "I25/temp8", "I25/temp4")
spice[1711] = nfet(0.64, "10_I25", "I25/temp8", "I25/temp6", "Vgnd")
spice[1712] = pfet(0.75, "11_I25", "I25/temp8", "I25/temp6", "Vdd")
spice[1713] = pfet(0.42, "12_I25", "I25/temp5", "I25/temp9", "I25/temp2")
spice[1714] = nfet(0.42, "13_I25", "Vgnd", "I25/temp1", "I25/temp0")
spice[1715] = nfet(0.42, "14_I25", "I25/temp9", "I25/temp3", "Vgnd")
spice[1716] = pfet(0.42, "15_I25", "I25/temp2", "I25/temp3", "I25/temp8")
spice[1717] = nfet(0.36, "16_I25", "I25/temp7", "I25/temp9", "I25/temp6")
spice[1718] = pfet(0.42, "17_I25", "Vdd", "I25/temp1", "I25/temp5")
spice[1719] = nfet(0.36, "18_I25", "I25/temp0", "I25/temp3", "I25/temp2")
spice[1720] = pfet(0.64, "19_I25", "I25/temp9", "I25/temp3", "Vdd")
spice[1721] = nfet(0.36, "20_I25", "I25/temp6", "I25/temp3", "I25/temp10")
spice[1722] = nfet(0.65, "21_I25", "Vgnd", "I25/temp2", "I25/temp1")
spice[1723] = nfet(0.42, "22_I25", "I25/temp10", "I25/D", "Vgnd")
spice[1724] = nfet(0.42, "23_I25", "Vgnd", "clk", "I25/temp3")
# timing for  I25/temp9:
# timing for  I25/temp2:
# timing for  I25/temp8:
# timing for        clk:
# timing for      I25/D:
# timing for  I25/temp7:
# timing for  I25/temp1:
# timing for  I25/temp5:
# timing for  I25/temp0:
# timing for  I25/temp4:
# timing for  I25/temp3:
# timing for      I25/Q:
# timing for  I25/temp6:
# timing for I25/temp10:




spice[1851] = ""
for name in timings_to_track:
    spice.insert(1851, f"meas tran {name} when V({name}) = 0.9")

spice = "\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
    