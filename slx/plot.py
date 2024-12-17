import json
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from mpl_toolkits.mplot3d import Axes3D

# Original imports and code from your script remain the same:
from spice import parse_measures, run_spice

MINSIZE = 0.36


def area(W):
    return 0.15 * W


def perim(W):
    return 2 * (W + 0.15)


fets = {}

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")


    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[
        name] = f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[
        name] = f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def value_to_voltage(value, transition):
    if value == "0" or value == 0:
        return 0
    if value == "1.8" or value == 1.8:
        return 1.8
    if value == "rise":
        return f"PULSE(0 1.8 0 {transition}n 0.1n 100n 100n)"
    if value == "fall":
        return f"PULSE(1.8 0 0 {transition}n 0.1n 100n 100n)"
    raise ValueError(f"Unknown value for voltage conv {value}")


def get_timing(P):
    pfet(P["w_0"], "0", "Vdd",  "A", "X")
    nfet(P["w_1"], "1", "Vgnd", "A", "X")

    spice = f"""
    .title slx
    .include "./prelude.spice"

    VVDD Vdd 0 1.8
    VVGND Vgnd 0 0

    VA A 0 {value_to_voltage(P["val_a"], P["transition"])}

    CX X 0 {P["capa_out_fF"]}f

    """

    for fet in fets.values():
        spice += fet + "\n"

    spice += f"""
    .tran 0.01n {P["sim_time"]}n

    .control
    run
    plot V(C) V(X)
    meas tran x_cross when V(X) = 0.9
    meas tran x_start WHEN V(X) = {1.8 * 0.8}
    meas tran x_end   WHEN V(X) = {1.8 * 0.2}
    .endc
    """

    output, stderr = run_spice(spice)
    measures = parse_measures(output)

    if "x_cross" not in measures or "x_start" not in measures or "x_end" not in measures:
        return None, None

    transition = abs(measures["x_end"] - measures["x_start"])
    delta_time = measures["x_cross"] - P["transition"] * 0.5e-9

    return delta_time, transition

randfet = lambda: min(100.0, 1.0 / math.sqrt(np.random.uniform(0, 1)) - 1 + 0.36)

if __name__ == "__main__":
    np.random.seed(0)

    w0_values = np.linspace(0.36, 10.0, 8)  # for example
    w1_values = np.linspace(0.36, 10.0, 8)  # for example

    # Keep other widths fixed to some nominal value:
    fixed_width = 0.5

    # 0 is tradeoff, 5 a bit

    # Fixed parameters for simulation:
    value_a = "rise"
    sim_time = 3
    transition_time = 0.01  # for simplicity
    capa_out_fF = 10.0  # for simplicity

    delta_times = np.zeros((len(w0_values), len(w1_values)))

    for i, w0 in enumerate(w0_values):
        for j, w1 in enumerate(w1_values):
            P = {
                "w_0": w0,
                "w_1": w1,

                "val_a": value_a,

                "sim_time": sim_time,
                "transition": transition_time,
                "capa_out_fF": capa_out_fF,
            }

            dt, tr = get_timing(P)
            delta_times[i, j] = dt if dt is not None else np.nan

    W0, W1 = np.meshgrid(w1_values, w0_values)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(W0, W1, delta_times, cmap='viridis')
    ax.set_xlabel(f"W_1")
    ax.set_ylabel(f"W_0")
    ax.set_zlabel("Delta Time")
    ax.set_title("Delta Time as a function of W_0 and W_1")

    plt.ylabel("Delta Time")
    plt.legend()
    plt.show()

"""
if __name__ == "__main__":
    # Define the widths we want to sweep for w_0 and w_1:
    w0_values = np.linspace(0.36, 2.0, 8)  # for example
    w1_values = np.linspace(0.36, 2.0, 8)  # for example

    # Keep other widths fixed to some nominal value:
    fixed_width = 0.5

    # 0 is tradeoff, 5 a bit

    w_idx_0 = 6
    w_idx_1 = 7

    # Fixed parameters for simulation:
    value_a = "1.8"
    value_b = "1.8"
    value_c = "rise"
    sim_time = 3
    transition_time = 0.5  # for simplicity
    capa_out_fF = 10.0  # for simplicity

    # Create a 2D array to store delta_time results
    delta_times = np.zeros((len(w0_values), len(w1_values)))

    # Sweep over w_0 and w_1
    for i, w0 in enumerate(w0_values):
        for j, w1 in enumerate(w1_values):
            # Construct parameters P:
            P = {
                "w_0": fixed_width,
                "w_1": fixed_width,
                "w_2": fixed_width,
                "w_3": fixed_width,
                "w_4": fixed_width,
                "w_5": fixed_width,
                "w_6": fixed_width,
                "w_7": fixed_width,
                "w_8": fixed_width,
                "w_9": fixed_width,
                "w_10": fixed_width,
                "w_11": fixed_width,
                "w_12": fixed_width,
                "w_13": fixed_width,
                "w_14": fixed_width,
                "w_15": fixed_width,
                "w_16": fixed_width,
                "w_17": fixed_width,
                "w_18": fixed_width,
                "w_19": fixed_width,
                "w_20": fixed_width,
                "w_21": fixed_width,

                "val_a": value_a,
                "val_b": value_b,
                "val_c": value_c,

                "sim_time": sim_time,
                "transition": transition_time,
                "capa_out_fF": capa_out_fF,

                f"w_{w_idx_0}": w0,
                f"w_{w_idx_1}": w1,
            }


            dt, tr = get_timing(P)
            delta_times[i, j] = dt if dt is not None else np.nan
    # Now plot the results in 3D
    W0, W1 = np.meshgrid(w1_values, w0_values)
    print(delta_times)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(W0, W1, delta_times, cmap='viridis')
    ax.set_xlabel(f"W_{w_idx_1}")
    ax.set_ylabel(f"W_{w_idx_0}")
    ax.set_zlabel("Delta Time")
    ax.set_title("Delta Time as a function of W_0 and W_1")

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
"""