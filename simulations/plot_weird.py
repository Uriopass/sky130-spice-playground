import matplotlib.pyplot as plt
import numpy as np
from spice import parse_voltage, run_spice

def run_sim(delay):
    with open("weird.spice", "r") as f:
        content = f.read()
        content = content.replace("{{{DELAY}}}", str(delay))

    run_spice(content)

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
plt.show()