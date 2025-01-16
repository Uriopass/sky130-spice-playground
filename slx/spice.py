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

def run_spice_plot(content):
    """
    Run a spice simulation with the spice content
    :param content: Spice language content
    :return: (stdout, stderr)
    """
    temp_file = tempfile.mktemp()
    with open(temp_file, "w") as f:
        f.write(content)
    s = subprocess.run(["ngspice", temp_file], capture_output=True, text=True)
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
        if len(vals) < 3:
            continue
        if vals[1] != "=":
            continue
        if not vals[2][0].isdigit() and not vals[2][0] == "-":
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