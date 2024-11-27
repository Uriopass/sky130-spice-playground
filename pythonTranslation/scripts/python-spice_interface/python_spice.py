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

def area(W):
    return 0.15 * W

def perim(W):
    return 2*(W + 0.15)

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    closest_bin = bins_pfet[min(bisect.bisect_left(bins_pfet, W), len(bins_pfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    closest_bin = bins_nfet[min(bisect.bisect_left(bins_nfet, W), len(bins_nfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

with open("../../libs/ngspice/out.spice", 'r') as f:
    spice = f.read()

spice = spice.split('\n')
spice[  16] = nfet(0.65, "0_I0", "I0/Q", "I0/temp1", "Vgnd")
spice[  17] = nfet(0.36, "1_I0", "I0/temp2", "I0/temp9", "I0/temp8")
spice[  18] = pfet(0.42, "2_I0", "I0/temp4", "I0/temp3", "I0/temp6")
spice[  19] = pfet(0.64, "3_I0", "Vdd", "clk", "I0/temp3")
spice[  20] = pfet(1.00, "4_I0", "I0/Q", "I0/temp1", "Vdd")
spice[  21] = pfet(0.42, "5_I0", "I0/temp10", "I0/D", "Vdd")
spice[  22] = nfet(0.42, "6_I0", "Vgnd", "I0/temp8", "I0/temp7")
spice[  23] = pfet(1.00, "7_I0", "Vdd", "I0/temp2", "I0/temp1")
spice[  24] = pfet(0.42, "8_I0", "I0/temp6", "I0/temp9", "I0/temp10")
spice[  25] = pfet(0.42, "9_I0", "Vdd", "I0/temp8", "I0/temp4")
spice[  26] = nfet(0.64, "10_I0", "I0/temp8", "I0/temp6", "Vgnd")
spice[  27] = pfet(0.75, "11_I0", "I0/temp8", "I0/temp6", "Vdd")
spice[  28] = pfet(0.42, "12_I0", "I0/temp5", "I0/temp9", "I0/temp2")
spice[  29] = nfet(0.42, "13_I0", "Vgnd", "I0/temp1", "I0/temp0")
spice[  30] = nfet(0.42, "14_I0", "I0/temp9", "I0/temp3", "Vgnd")
spice[  31] = pfet(0.42, "15_I0", "I0/temp2", "I0/temp3", "I0/temp8")
spice[  32] = nfet(0.36, "16_I0", "I0/temp7", "I0/temp9", "I0/temp6")
spice[  33] = pfet(0.42, "17_I0", "Vdd", "I0/temp1", "I0/temp5")
spice[  34] = nfet(0.36, "18_I0", "I0/temp0", "I0/temp3", "I0/temp2")
spice[  35] = pfet(0.64, "19_I0", "I0/temp9", "I0/temp3", "Vdd")
spice[  36] = nfet(0.36, "20_I0", "I0/temp6", "I0/temp3", "I0/temp10")
spice[  37] = nfet(0.65, "21_I0", "Vgnd", "I0/temp2", "I0/temp1")
spice[  38] = nfet(0.42, "22_I0", "I0/temp10", "I0/D", "Vgnd")
spice[  39] = nfet(0.42, "23_I0", "Vgnd", "clk", "I0/temp3")


spice[ 112] = pfet(1.00, "0_I1", "Vdd", "I1/A", "I1/temp0")
spice[ 113] = nfet(0.42, "1_I1", "Vgnd", "I1/temp0", "I1/X")
spice[ 114] = nfet(0.42, "2_I1", "Vgnd", "I1/temp0", "I1/X")
spice[ 115] = pfet(1.00, "3_I1", "I1/X", "I1/temp0", "Vdd")
spice[ 116] = nfet(0.42, "4_I1", "I1/X", "I1/temp0", "Vgnd")
spice[ 117] = nfet(0.42, "5_I1", "Vgnd", "I1/A", "I1/temp0")
spice[ 118] = pfet(1.00, "6_I1", "Vdd", "I1/temp0", "I1/X")
spice[ 119] = nfet(0.42, "7_I1", "I1/X", "I1/temp0", "Vgnd")
spice[ 120] = pfet(1.00, "8_I1", "I1/X", "I1/temp0", "Vdd")
spice[ 121] = pfet(1.00, "9_I1", "Vdd", "I1/temp0", "I1/X")


spice[ 148] = pfet(1.00, "0_I2", "Vdd", "I2/temp0", "I2/X")
spice[ 149] = pfet(1.00, "1_I2", "I2/X", "I2/temp0", "Vdd")
spice[ 150] = pfet(1.00, "2_I2", "Vdd", "I2/temp0", "I2/X")
spice[ 151] = pfet(1.00, "3_I2", "I2/X", "I2/temp0", "Vdd")
spice[ 152] = nfet(0.65, "4_I2", "I2/X", "I2/temp0", "Vgnd")
spice[ 153] = nfet(0.65, "5_I2", "I2/X", "I2/temp0", "Vgnd")
spice[ 154] = nfet(0.65, "6_I2", "Vgnd", "I2/temp0", "I2/X")
spice[ 155] = nfet(0.65, "7_I2", "Vgnd", "I2/temp0", "I2/X")
spice[ 156] = pfet(1.00, "8_I2", "Vdd", "I2/A", "I2/temp0")
spice[ 157] = nfet(0.65, "9_I2", "Vgnd", "I2/A", "I2/temp0")


spice[ 193] = pfet(0.42, "0_I3", "Vdd", "I3/temp5", "I3/temp3")
spice[ 194] = pfet(0.42, "1_I3", "I3/temp5", "I3/S", "Vdd")
spice[ 195] = pfet(0.42, "2_I3", "I3/temp4", "I3/S", "Vdd")
spice[ 196] = nfet(0.42, "3_I3", "Vgnd", "I3/temp5", "I3/temp0")
spice[ 197] = pfet(0.42, "4_I3", "I3/temp1", "I3/A0", "I3/temp4")      # Max size: 68.389
spice[ 198] = nfet(0.42, "5_I3", "I3/temp5", "I3/S", "Vgnd")
spice[ 199] = nfet(0.42, "6_I3", "I3/temp0", "I3/A0", "I3/temp1")      # Max size: 68.389
spice[ 200] = pfet(0.42, "7_I3", "I3/temp3", "I3/A1", "I3/temp1")      # Max size: 167.513
spice[ 201] = nfet(0.42, "8_I3", "I3/temp1", "I3/A1", "I3/temp2")      # Max size: 167.513
spice[ 202] = nfet(0.42, "9_I3", "I3/temp2", "I3/S", "Vgnd")
spice[ 203] = pfet(1.00, "10_I3", "Vdd", "I3/temp1", "I3/X")
spice[ 204] = nfet(0.65, "11_I3", "Vgnd", "I3/temp1", "I3/X")


spice[ 262] = pfet(0.64, "0_I4", "Vdd", "I4/S", "I4/temp0")            # Max size: 58.459
spice[ 263] = pfet(0.64, "1_I4", "I4/temp0", "I4/A0", "I4/temp5")
spice[ 264] = pfet(1.00, "2_I4", "Vdd", "I4/temp5", "I4/X")
spice[ 265] = pfet(0.64, "3_I4", "I4/temp5", "I4/A1", "I4/temp2")      # Max size: 71.979
spice[ 266] = nfet(0.65, "4_I4", "Vgnd", "I4/temp5", "I4/X")
spice[ 267] = nfet(0.42, "5_I4", "Vgnd", "I4/S", "I4/temp3")           # Max size: 58.459
spice[ 268] = pfet(0.64, "6_I4", "I4/temp2", "I4/temp4", "Vdd")
spice[ 269] = nfet(0.42, "7_I4", "I4/temp5", "I4/A0", "I4/temp1")
spice[ 270] = nfet(0.42, "8_I4", "I4/temp1", "I4/temp4", "Vgnd")
spice[ 271] = nfet(0.42, "9_I4", "I4/temp4", "I4/S", "Vgnd")           # Max size: 58.459
spice[ 272] = nfet(0.42, "10_I4", "I4/temp3", "I4/A1", "I4/temp5")     # Max size: 71.979
spice[ 273] = pfet(1.00, "11_I4", "I4/X", "I4/temp5", "Vdd")
spice[ 274] = pfet(0.64, "12_I4", "I4/temp4", "I4/S", "Vdd")           # Max size: 58.459
spice[ 275] = nfet(0.65, "13_I4", "I4/X", "I4/temp5", "Vgnd")


spice[ 328] = pfet(1.00, "0_I5", "I5/X", "I5/temp3", "I5/temp2")
spice[ 329] = nfet(0.65, "1_I5", "I5/X", "I5/B", "I5/temp1")
spice[ 330] = nfet(0.65, "2_I5", "I5/temp3", "I5/B", "Vgnd")
spice[ 331] = pfet(1.00, "3_I5", "I5/temp0", "I5/B", "I5/temp3")
spice[ 332] = pfet(1.00, "4_I5", "Vdd", "I5/B", "I5/temp2")
spice[ 333] = nfet(0.65, "5_I5", "Vgnd", "I5/A", "I5/temp3")           # Max size: 319.424
spice[ 334] = nfet(0.65, "6_I5", "Vgnd", "I5/temp3", "I5/X")
spice[ 335] = pfet(1.00, "7_I5", "I5/temp2", "I5/A", "Vdd")            # Max size: 319.424
spice[ 336] = pfet(1.00, "8_I5", "Vdd", "I5/A", "I5/temp0")            # Max size: 319.424
spice[ 337] = nfet(0.65, "9_I5", "I5/temp1", "I5/A", "Vgnd")           # Max size: 319.424


spice[ 386] = nfet(0.65, "0_I6", "I6/temp2", "I6/B1", "Vgnd")          # Max size: 158.096
spice[ 387] = pfet(1.00, "1_I6", "I6/temp0", "I6/B1", "I6/temp2")      # Max size: 158.096
spice[ 388] = pfet(1.00, "2_I6", "Vdd", "I6/temp2", "I6/X")
spice[ 389] = pfet(1.00, "3_I6", "Vdd", "I6/A1", "I6/temp0")           # Max size: 71.979
spice[ 390] = nfet(0.65, "4_I6", "Vgnd", "I6/temp2", "I6/X")
spice[ 391] = nfet(0.65, "5_I6", "Vgnd", "I6/A2", "I6/temp1")
spice[ 392] = pfet(1.00, "6_I6", "I6/temp0", "I6/A2", "Vdd")
spice[ 393] = nfet(0.65, "7_I6", "I6/temp1", "I6/A1", "I6/temp2")      # Max size: 71.979


spice[ 454] = pfet(1.00, "0_I7", "Vdd", "I7/temp2", "I7/X")
spice[ 455] = pfet(1.00, "1_I7", "I7/temp2", "I7/C1", "I7/temp1")      # Max size: 96.012
spice[ 456] = pfet(1.00, "2_I7", "Vdd", "I7/A2", "I7/temp3")
spice[ 457] = nfet(0.65, "3_I7", "Vgnd", "I7/B1", "I7/temp2")          # Max size: 198.255
spice[ 458] = nfet(0.65, "4_I7", "Vgnd", "I7/temp2", "I7/X")
spice[ 459] = nfet(0.65, "5_I7", "I7/temp0", "I7/A2", "Vgnd")
spice[ 460] = pfet(1.00, "6_I7", "I7/temp3", "I7/A1", "Vdd")           # Max size: 35.989
spice[ 461] = nfet(0.65, "7_I7", "I7/temp2", "I7/A1", "I7/temp0")      # Max size: 35.989
spice[ 462] = pfet(1.00, "8_I7", "I7/temp1", "I7/B1", "I7/temp3")      # Max size: 198.255
spice[ 463] = nfet(0.65, "9_I7", "I7/temp2", "I7/C1", "Vgnd")          # Max size: 96.012


spice[ 535] = pfet(1.00, "0_I8", "I8/temp2", "I8/C1", "I8/temp3")      # Max size: 178.637
spice[ 536] = pfet(1.00, "1_I8", "Vdd", "I8/A2", "I8/temp0")           # Max size: 33.669
spice[ 537] = nfet(0.65, "2_I8", "Vgnd", "I8/B1", "I8/temp2")          # Max size: 266.571
spice[ 538] = nfet(0.65, "3_I8", "I8/temp1", "I8/A2", "I8/temp4")      # Max size: 33.669
spice[ 539] = nfet(0.65, "4_I8", "I8/temp2", "I8/A1", "I8/temp1")      # Max size: 71.979
spice[ 540] = nfet(0.65, "5_I8", "I8/temp4", "I8/A3", "Vgnd")
spice[ 541] = pfet(1.00, "6_I8", "Vdd", "I8/temp2", "I8/X")
spice[ 542] = pfet(1.00, "7_I8", "I8/temp0", "I8/A1", "Vdd")           # Max size: 71.979
spice[ 543] = nfet(0.65, "8_I8", "Vgnd", "I8/temp2", "I8/X")
spice[ 544] = pfet(1.00, "9_I8", "I8/temp0", "I8/A3", "Vdd")
spice[ 545] = nfet(0.65, "10_I8", "I8/temp2", "I8/C1", "Vgnd")         # Max size: 178.637
spice[ 546] = pfet(1.00, "11_I8", "I8/temp3", "I8/B1", "I8/temp0")     # Max size: 266.571
spice[ 547] = pfet(1.00, "12_I8", "I8/X", "I8/temp2", "Vdd")
spice[ 548] = nfet(0.65, "13_I8", "I8/X", "I8/temp2", "Vgnd")


spice[ 629] = nfet(0.65, "0_I9", "I9/Y", "I9/B1", "I9/temp3")          # Max size: 292.19
spice[ 630] = pfet(1.00, "1_I9", "I9/temp1", "I9/B1", "I9/temp0")      # Max size: 292.19
spice[ 631] = pfet(1.00, "2_I9", "I9/temp1", "I9/A2", "Vdd")
spice[ 632] = nfet(0.65, "3_I9", "Vgnd", "I9/B2", "I9/temp3")          # Max size: 111.568
spice[ 633] = nfet(0.65, "4_I9", "I9/Y", "I9/A1", "I9/temp2")          # Max size: 71.979
spice[ 634] = pfet(1.00, "5_I9", "I9/temp0", "I9/B2", "I9/temp1")      # Max size: 111.568
spice[ 635] = pfet(1.00, "6_I9", "Vdd", "I9/A1", "I9/temp1")           # Max size: 71.979
spice[ 636] = nfet(0.65, "7_I9", "Vgnd", "I9/A2", "I9/temp2")
spice[ 637] = pfet(1.00, "8_I9", "I9/temp1", "I9/A1", "Vdd")           # Max size: 71.979
spice[ 638] = pfet(1.00, "9_I9", "I9/Y", "I9/C1", "I9/temp0")          # Max size: 289.421
spice[ 639] = nfet(0.65, "10_I9", "Vgnd", "I9/C1", "I9/Y")             # Max size: 289.421
spice[ 640] = nfet(0.65, "11_I9", "I9/Y", "I9/C1", "Vgnd")             # Max size: 289.421
spice[ 641] = pfet(1.00, "12_I9", "Vdd", "I9/A2", "I9/temp1")
spice[ 642] = nfet(0.65, "13_I9", "I9/temp3", "I9/B2", "Vgnd")         # Max size: 111.568
spice[ 643] = nfet(0.65, "14_I9", "I9/temp3", "I9/B1", "I9/Y")         # Max size: 292.19
spice[ 644] = nfet(0.65, "15_I9", "I9/temp2", "I9/A2", "Vgnd")
spice[ 645] = pfet(1.00, "16_I9", "I9/temp0", "I9/C1", "I9/Y")         # Max size: 289.421
spice[ 646] = pfet(1.00, "17_I9", "I9/temp1", "I9/B2", "I9/temp0")     # Max size: 111.568
spice[ 647] = nfet(0.65, "18_I9", "I9/temp2", "I9/A1", "I9/Y")         # Max size: 71.979
spice[ 648] = pfet(1.00, "19_I9", "I9/temp0", "I9/B1", "I9/temp1")     # Max size: 292.19


spice[ 731] = nfet(0.42, "0_I10", "I10/temp0", "I10/B", "Vgnd")        # Max size: 139.517
spice[ 732] = nfet(0.42, "1_I10", "I10/temp0", "I10/D", "Vgnd")        # Max size: 98.397
spice[ 733] = pfet(0.42, "2_I10", "I10/temp3", "I10/B", "I10/temp1")   # Max size: 139.517
spice[ 734] = pfet(0.42, "3_I10", "Vdd", "I10/A", "I10/temp3")
spice[ 735] = nfet(0.65, "4_I10", "I10/X", "I10/temp0", "Vgnd")
spice[ 736] = pfet(0.42, "5_I10", "I10/temp1", "I10/C", "I10/temp2")   # Max size: 129.362
spice[ 737] = pfet(1.00, "6_I10", "I10/X", "I10/temp0", "Vdd")
spice[ 738] = nfet(0.42, "7_I10", "Vgnd", "I10/C", "I10/temp0")        # Max size: 129.362
spice[ 739] = pfet(0.42, "8_I10", "I10/temp2", "I10/D", "I10/temp0")   # Max size: 98.397
spice[ 740] = nfet(0.42, "9_I10", "Vgnd", "I10/A", "I10/temp0")


spice[ 794] = nfet(0.65, "0_I11", "Vgnd", "I11/A2", "I11/temp0")       # Max size: 115.436
spice[ 795] = nfet(0.65, "1_I11", "Vgnd", "I11/B1", "I11/Y")           # Max size: 180.253
spice[ 796] = nfet(0.65, "2_I11", "I11/Y", "I11/A1", "I11/temp1")
spice[ 797] = nfet(0.65, "3_I11", "I11/temp1", "I11/A2", "Vgnd")       # Max size: 115.436
spice[ 798] = pfet(1.00, "4_I11", "I11/temp2", "I11/B1", "I11/Y")      # Max size: 180.253
spice[ 799] = pfet(1.00, "5_I11", "I11/temp2", "I11/A1", "Vdd")
spice[ 800] = pfet(1.00, "6_I11", "I11/Y", "I11/B1", "I11/temp2")      # Max size: 180.253
spice[ 801] = pfet(1.00, "7_I11", "Vdd", "I11/A2", "I11/temp2")        # Max size: 115.436
spice[ 802] = pfet(1.00, "8_I11", "I11/temp2", "I11/A2", "Vdd")        # Max size: 115.436
spice[ 803] = pfet(1.00, "9_I11", "Vdd", "I11/A1", "I11/temp2")
spice[ 804] = nfet(0.65, "10_I11", "I11/temp0", "I11/A1", "I11/Y")
spice[ 805] = nfet(0.65, "11_I11", "I11/Y", "I11/B1", "Vgnd")          # Max size: 180.253


spice[ 863] = nfet(0.65, "0_I12", "Vgnd", "I12/A1", "I12/temp3")
spice[ 864] = nfet(0.65, "1_I12", "I12/temp1", "I12/B1", "I12/temp3")  # Max size: 96.296
spice[ 865] = pfet(1.00, "2_I12", "I12/temp2", "I12/C1", "Vdd")        # Max size: 194.476
spice[ 866] = pfet(1.00, "3_I12", "Vdd", "I12/B1", "I12/temp2")        # Max size: 96.296
spice[ 867] = pfet(1.00, "4_I12", "I12/temp2", "I12/A2", "I12/temp0")  # Max size: 256.186
spice[ 868] = pfet(1.00, "5_I12", "I12/temp0", "I12/A1", "Vdd")
spice[ 869] = nfet(0.65, "6_I12", "I12/temp2", "I12/C1", "I12/temp1")  # Max size: 194.476
spice[ 870] = pfet(1.00, "7_I12", "Vdd", "I12/temp2", "I12/X")
spice[ 871] = nfet(0.65, "8_I12", "Vgnd", "I12/temp2", "I12/X")
spice[ 872] = nfet(0.65, "9_I12", "I12/temp3", "I12/A2", "Vgnd")       # Max size: 256.186


spice[ 947] = nfet(0.65, "0_I13", "I13/temp1", "I13/A2", "I13/temp2")  # Max size: 231.566
spice[ 948] = nfet(0.65, "1_I13", "Vgnd", "I13/A4", "I13/temp4")       # Max size: 143.006
spice[ 949] = pfet(1.00, "2_I13", "Vdd", "I13/A3", "I13/temp0")        # Max size: 155.502
spice[ 950] = pfet(1.00, "3_I13", "I13/temp0", "I13/A2", "Vdd")        # Max size: 231.566
spice[ 951] = pfet(1.00, "4_I13", "I13/temp0", "I13/A4", "Vdd")        # Max size: 143.006
spice[ 952] = pfet(1.00, "5_I13", "Vdd", "I13/A1", "I13/temp0")
spice[ 953] = nfet(0.65, "6_I13", "I13/temp2", "I13/A1", "I13/temp3")
spice[ 954] = pfet(1.00, "7_I13", "I13/temp0", "I13/B1", "I13/temp3")  # Max size: 454.441
spice[ 955] = pfet(1.00, "8_I13", "Vdd", "I13/temp3", "I13/X")
spice[ 956] = nfet(0.65, "9_I13", "I13/temp3", "I13/B1", "Vgnd")       # Max size: 454.441
spice[ 957] = nfet(0.65, "10_I13", "Vgnd", "I13/temp3", "I13/X")
spice[ 958] = nfet(0.65, "11_I13", "I13/temp4", "I13/A3", "I13/temp1") # Max size: 155.502


spice[1024] = nfet(0.65, "0_I14", "Vgnd", "I14/A2", "I14/temp0")       # Max size: 166.609
spice[1025] = nfet(0.65, "1_I14", "Vgnd", "I14/B1", "I14/Y")           # Max size: 598.228
spice[1026] = nfet(0.65, "2_I14", "I14/Y", "I14/A1", "I14/temp1")
spice[1027] = nfet(0.65, "3_I14", "I14/temp1", "I14/A2", "Vgnd")       # Max size: 166.609
spice[1028] = pfet(1.00, "4_I14", "I14/temp2", "I14/B1", "I14/Y")      # Max size: 598.228
spice[1029] = pfet(1.00, "5_I14", "I14/temp2", "I14/A1", "Vdd")
spice[1030] = pfet(1.00, "6_I14", "I14/Y", "I14/B1", "I14/temp2")      # Max size: 598.228
spice[1031] = pfet(1.00, "7_I14", "Vdd", "I14/A2", "I14/temp2")        # Max size: 166.609
spice[1032] = pfet(1.00, "8_I14", "I14/temp2", "I14/A2", "Vdd")        # Max size: 166.609
spice[1033] = pfet(1.00, "9_I14", "Vdd", "I14/A1", "I14/temp2")
spice[1034] = nfet(0.65, "10_I14", "I14/temp0", "I14/A1", "I14/Y")
spice[1035] = nfet(0.65, "11_I14", "I14/Y", "I14/B1", "Vgnd")          # Max size: 598.228


spice[1081] = nfet(0.42, "0_I15", "Vgnd", "I15/A_N", "I15/temp1")
spice[1082] = nfet(0.65, "1_I15", "I15/Y", "I15/temp1", "I15/temp0")
spice[1083] = nfet(0.65, "2_I15", "I15/temp0", "I15/B", "Vgnd")        # Max size: 222.145
spice[1084] = pfet(1.00, "3_I15", "Vdd", "I15/temp1", "I15/Y")
spice[1085] = pfet(1.00, "4_I15", "I15/Y", "I15/B", "Vdd")             # Max size: 222.145
spice[1086] = pfet(0.42, "5_I15", "Vdd", "I15/A_N", "I15/temp1")


spice[1123] = pfet(1.00, "0_I16", "Vdd", "I16/A", "I16/temp0")
spice[1124] = nfet(0.65, "1_I16", "Vgnd", "I16/A", "I16/Y")
spice[1125] = pfet(1.00, "2_I16", "I16/temp0", "I16/B", "I16/Y")       # Max size: 286.074
spice[1126] = nfet(0.65, "3_I16", "I16/Y", "I16/B", "Vgnd")            # Max size: 286.074


spice[1176] = nfet(0.65, "0_I17", "I17/temp1", "I17/C1", "Vgnd")       # Max size: 726.551
spice[1177] = nfet(0.65, "1_I17", "I17/temp2", "I17/A3", "Vgnd")       # Max size: 242.971
spice[1178] = nfet(0.65, "2_I17", "I17/temp3", "I17/A2", "I17/temp2")
spice[1179] = nfet(0.65, "3_I17", "Vgnd", "I17/B1", "I17/temp1")       # Max size: 741.092
spice[1180] = nfet(0.65, "4_I17", "I17/temp1", "I17/A1", "I17/temp3")  # Max size: 71.979
spice[1181] = pfet(1.00, "5_I17", "I17/temp1", "I17/C1", "I17/temp0")  # Max size: 726.551
spice[1182] = pfet(1.00, "6_I17", "I17/temp0", "I17/B1", "I17/temp4")  # Max size: 741.092
spice[1183] = pfet(1.00, "7_I17", "Vdd", "I17/temp1", "I17/X")
spice[1184] = pfet(1.00, "8_I17", "I17/temp4", "I17/A3", "Vdd")        # Max size: 242.971
spice[1185] = pfet(1.00, "9_I17", "Vdd", "I17/A2", "I17/temp4")
spice[1186] = pfet(1.00, "10_I17", "I17/temp4", "I17/A1", "Vdd")       # Max size: 71.979
spice[1187] = nfet(0.65, "11_I17", "Vgnd", "I17/temp1", "I17/X")


spice[1258] = nfet(0.65, "0_I18", "I18/temp2", "I18/B1", "Vgnd")       # Max size: 729.552
spice[1259] = pfet(1.00, "1_I18", "I18/temp0", "I18/B1", "I18/temp2")  # Max size: 729.552
spice[1260] = pfet(1.00, "2_I18", "Vdd", "I18/temp2", "I18/X")
spice[1261] = pfet(1.00, "3_I18", "Vdd", "I18/A1", "I18/temp0")
spice[1262] = nfet(0.65, "4_I18", "Vgnd", "I18/temp2", "I18/X")
spice[1263] = nfet(0.65, "5_I18", "Vgnd", "I18/A2", "I18/temp1")       # Max size: 148.907
spice[1264] = pfet(1.00, "6_I18", "I18/temp0", "I18/A2", "Vdd")        # Max size: 148.907
spice[1265] = nfet(0.65, "7_I18", "I18/temp1", "I18/A1", "I18/temp2")


spice[1319] = pfet(1.00, "0_I19", "Vdd", "I19/A1", "I19/temp2")        # Max size: 71.979
spice[1320] = nfet(0.65, "1_I19", "I19/temp0", "I19/B1", "I19/temp1")
spice[1321] = nfet(0.65, "2_I19", "I19/temp0", "I19/A1", "Vgnd")       # Max size: 71.979
spice[1322] = nfet(0.65, "3_I19", "Vgnd", "I19/A2", "I19/temp0")       # Max size: 323.301
spice[1323] = pfet(1.00, "4_I19", "Vdd", "I19/temp1", "I19/X")
spice[1324] = pfet(1.00, "5_I19", "I19/temp1", "I19/B1", "Vdd")
spice[1325] = pfet(1.00, "6_I19", "I19/temp2", "I19/A2", "I19/temp1")  # Max size: 323.301
spice[1326] = nfet(0.65, "7_I19", "Vgnd", "I19/temp1", "I19/X")


spice[1380] = nfet(0.65, "0_I20", "I20/temp0", "I20/A1", "I20/Y")      # Max size: 71.979
spice[1381] = pfet(1.00, "1_I20", "I20/temp1", "I20/A2", "Vdd")        # Max size: 826.949
spice[1382] = nfet(0.65, "2_I20", "I20/Y", "I20/B1", "Vgnd")
spice[1383] = pfet(1.00, "3_I20", "Vdd", "I20/A1", "I20/temp1")        # Max size: 71.979
spice[1384] = pfet(1.00, "4_I20", "I20/temp1", "I20/B1", "I20/Y")
spice[1385] = nfet(0.65, "5_I20", "Vgnd", "I20/A2", "I20/temp0")       # Max size: 826.949


spice[1427] = pfet(1.00, "0_I21", "I21/temp3", "I21/A", "Vdd")
spice[1428] = pfet(1.00, "1_I21", "I21/temp2", "I21/B", "Vdd")         # Max size: 411.859
spice[1429] = nfet(0.65, "2_I21", "I21/temp1", "I21/B", "I21/temp2")   # Max size: 411.859
spice[1430] = nfet(0.65, "3_I21", "I21/temp0", "I21/B", "Vgnd")        # Max size: 411.859
spice[1431] = nfet(0.65, "4_I21", "I21/Y", "I21/temp2", "I21/temp0")
spice[1432] = nfet(0.65, "5_I21", "Vgnd", "I21/A", "I21/temp1")
spice[1433] = pfet(1.00, "6_I21", "Vdd", "I21/A", "I21/temp2")
spice[1434] = pfet(1.00, "7_I21", "Vdd", "I21/temp2", "I21/Y")
spice[1435] = pfet(1.00, "8_I21", "I21/Y", "I21/B", "I21/temp3")       # Max size: 411.859
spice[1436] = nfet(0.65, "9_I21", "I21/temp0", "I21/A", "Vgnd")


spice[1488] = pfet(1.00, "0_I22", "Vdd", "I22/A2", "I22/temp1")        # Max size: 114.13
spice[1489] = nfet(0.65, "1_I22", "I22/temp0", "I22/B1", "I22/temp3")
spice[1490] = nfet(0.65, "2_I22", "Vgnd", "I22/A2", "I22/temp2")       # Max size: 114.13
spice[1491] = pfet(1.00, "3_I22", "I22/X", "I22/temp0", "Vdd")
spice[1492] = pfet(1.00, "4_I22", "I22/temp0", "I22/B1", "I22/temp1")
spice[1493] = pfet(1.00, "5_I22", "I22/temp1", "I22/A1", "Vdd")        # Max size: 71.979
spice[1494] = nfet(0.65, "6_I22", "I22/temp2", "I22/A1", "I22/temp0")  # Max size: 71.979
spice[1495] = nfet(0.65, "7_I22", "I22/X", "I22/temp0", "Vgnd")
spice[1496] = pfet(1.00, "8_I22", "I22/temp1", "I22/B2", "I22/temp0")  # Max size: 382.407
spice[1497] = nfet(0.65, "9_I22", "I22/temp3", "I22/B2", "Vgnd")       # Max size: 382.407


spice[1556] = nfet(0.65, "0_I23", "I23/temp2", "I23/B1", "Vgnd")       # Max size: 868.031
spice[1557] = pfet(1.00, "1_I23", "I23/temp0", "I23/B1", "I23/temp2")  # Max size: 868.031
spice[1558] = pfet(1.00, "2_I23", "Vdd", "I23/temp2", "I23/X")
spice[1559] = pfet(1.00, "3_I23", "Vdd", "I23/A1", "I23/temp0")        # Max size: 71.979
spice[1560] = nfet(0.65, "4_I23", "Vgnd", "I23/temp2", "I23/X")
spice[1561] = nfet(0.65, "5_I23", "Vgnd", "I23/A2", "I23/temp1")
spice[1562] = pfet(1.00, "6_I23", "I23/temp0", "I23/A2", "Vdd")
spice[1563] = nfet(0.65, "7_I23", "I23/temp1", "I23/A1", "I23/temp2")  # Max size: 71.979


spice[1612] = pfet(0.42, "0_I24", "Vdd", "I24/B", "I24/temp1")
spice[1613] = pfet(1.00, "1_I24", "I24/X", "I24/temp1", "Vdd")
spice[1614] = nfet(0.42, "2_I24", "Vgnd", "I24/B", "I24/temp0")
spice[1615] = pfet(0.42, "3_I24", "I24/temp1", "I24/A", "Vdd")         # Max size: 0.0
spice[1616] = nfet(0.65, "4_I24", "I24/X", "I24/temp1", "Vgnd")
spice[1617] = nfet(0.42, "5_I24", "I24/temp0", "I24/A", "I24/temp1")   # Max size: 0.0


spice[1649] = nfet(0.65, "0_I25", "I25/Q", "I25/temp1", "Vgnd")
spice[1650] = nfet(0.36, "1_I25", "I25/temp2", "I25/temp9", "I25/temp8")
spice[1651] = pfet(0.42, "2_I25", "I25/temp4", "I25/temp3", "I25/temp6")
spice[1652] = pfet(0.64, "3_I25", "Vdd", "clk", "I25/temp3")
spice[1653] = pfet(1.00, "4_I25", "I25/Q", "I25/temp1", "Vdd")
spice[1654] = pfet(0.42, "5_I25", "I25/temp10", "I25/D", "Vdd")
spice[1655] = nfet(0.42, "6_I25", "Vgnd", "I25/temp8", "I25/temp7")
spice[1656] = pfet(1.00, "7_I25", "Vdd", "I25/temp2", "I25/temp1")
spice[1657] = pfet(0.42, "8_I25", "I25/temp6", "I25/temp9", "I25/temp10")
spice[1658] = pfet(0.42, "9_I25", "Vdd", "I25/temp8", "I25/temp4")
spice[1659] = nfet(0.64, "10_I25", "I25/temp8", "I25/temp6", "Vgnd")
spice[1660] = pfet(0.75, "11_I25", "I25/temp8", "I25/temp6", "Vdd")
spice[1661] = pfet(0.42, "12_I25", "I25/temp5", "I25/temp9", "I25/temp2")
spice[1662] = nfet(0.42, "13_I25", "Vgnd", "I25/temp1", "I25/temp0")
spice[1663] = nfet(0.42, "14_I25", "I25/temp9", "I25/temp3", "Vgnd")
spice[1664] = pfet(0.42, "15_I25", "I25/temp2", "I25/temp3", "I25/temp8")
spice[1665] = nfet(0.36, "16_I25", "I25/temp7", "I25/temp9", "I25/temp6")
spice[1666] = pfet(0.42, "17_I25", "Vdd", "I25/temp1", "I25/temp5")
spice[1667] = nfet(0.36, "18_I25", "I25/temp0", "I25/temp3", "I25/temp2")
spice[1668] = pfet(0.64, "19_I25", "I25/temp9", "I25/temp3", "Vdd")
spice[1669] = nfet(0.36, "20_I25", "I25/temp6", "I25/temp3", "I25/temp10")
spice[1670] = nfet(0.65, "21_I25", "Vgnd", "I25/temp2", "I25/temp1")
spice[1671] = nfet(0.42, "22_I25", "I25/temp10", "I25/D", "Vgnd")
spice[1672] = nfet(0.42, "23_I25", "Vgnd", "clk", "I25/temp3")



spice = "\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
    