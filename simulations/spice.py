import numpy as np
import bisect
import tempfile
import subprocess
import os

def run_spice(content):
    """
    Run a spice simulation with the spice content
    :param content: Spice language content
    :return: (stdout, stderr)
    """
    temp_file = tempfile.mktemp()
    with open(temp_file, "w") as f:
        f.write(content)
    s = subprocess.run(["ngspice", "-b", temp_file], capture_output=True, text=True)
    output = s.stdout
    output_err = s.stderr

    os.remove(temp_file)
    return output, output_err

def parse_measures(stdout):
    """
    Parse the measures from a spice output
    e.g lines that look like t_start = 1.0
    :param stdout: The stdout from the spice simulation
    :return: A dictionary containing the measures
    """
    measures = {}
    for line in stdout.split("\n"):
        vals = line.strip().split()
        if len(vals) != 3:
            continue
        if vals[1] != "=":
            continue
        if not vals[2][0].isdigit():
            continue
        measures[vals[0]] = float(vals[2])
    return measures

def parse_voltage(file_path):
    """
    Parse the voltage data from a spice output file

    :param file_path: The path to the file
    :return: A tuple containing the time data and the voltage data as numpy arrays
    """
    time_data = []
    voltage_data = []

    # Open and read the file line by line
    with open(file_path, 'r') as file:
        content = file.read()
        for line in content.splitlines():
            line = line.strip()

            if len(line) == 0:
                continue

            if not line[0].isdigit():
                continue

            vals = line.split()

            alldigits = True
            for val in vals:
                if not val[0].isdigit():
                    alldigits = False

            if not alldigits:
                continue

            if len(vals) == 2:
                time_data.append(float(vals[1]))
            else:
                voltage_data.append(float(vals[0]))


    return np.array(time_data), np.array(voltage_data)



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

and4_counter = 0


def area(W):
    return 0.15 * W


def perim(W):
    return W + 2*0.15


def pfet(name, D, G, S, W):
    closest_bin = bins_pfet[min(bisect.bisect_left(bins_pfet, W), len(bins_pfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"""
X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt w={closest_bin} l=0.15 ad={ar} as={ar} pd={pe} ps={pe} m={mult}
"""


def nfet(name, D, G, S, W):
    closest_bin = bins_nfet[min(bisect.bisect_left(bins_nfet, W), len(bins_nfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"""
X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 w={closest_bin} l=0.15 ad={ar} as={ar} pd={pe} ps={pe} m={mult}
"""
