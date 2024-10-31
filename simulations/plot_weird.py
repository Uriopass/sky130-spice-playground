import matplotlib.pyplot as plt
import subprocess
import numpy as np

def parse_voltage(file_path):
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
            if len(vals) == 2:
                time_data.append(float(vals[1]))
            else:
                voltage_data.append(float(vals[0]))


    return time_data, voltage_data

def run_sim(delay):
    with open("simulations/weird.spice", "r") as f:
        content = f.read()
        content = content.replace("{{{DELAY}}}", str(delay))
        with open("simulations/weird_to_run.spice", "w") as f2:
            f2.write(content)
    s = subprocess.run(["ngspice", "-b", "simulations/weird_to_run.spice"], capture_output=True, text=True)
    output = s.stdout
    output_err = s.stderr

    time_data, voltage_data = parse_voltage("output.txt")

    last_crossing = None
    for ((t1, v1), (t2, v2)) in zip(zip(time_data, voltage_data), zip(time_data[1:], voltage_data[1:])):
        if v1 < 0.9 < v2:
            coeff = (0.9 - v1) / (v2 - v1)
            last_crossing = t1 + coeff * (t2 - t1)
        if v1 > 0.9 > v2:
            coeff = (0.9 - v2) / (v1 - v2)
            last_crossing = t2 + coeff * (t1 - t2)

    print(f"Delay: {delay}, Last crossing: {last_crossing}")

    return last_crossing

xs = np.linspace(1.2, 2.0, 70)
ys = [run_sim(x) for x in xs]

plt.plot(xs, ys)
plt.savefig("simulations/weird.png")