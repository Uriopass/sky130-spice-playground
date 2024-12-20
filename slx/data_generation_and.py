import json
import math
import time
import multiprocessing as mp

from spice import parse_measures, run_spice, run_spice_plot
import numpy as np

MINSIZE = 0.36

def area(W):
    return 0.15 * W

def perim(W):
    return 2 * (W + 0.15)

fets = {}

def pfet(W, name, D, G, S):

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def nfet(W, name, D, G, S):

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    fets[name] = f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"

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
    pfet(P["w_0"], "0", "Vdd", "A", "temp_inv")
    pfet(P["w_1"], "1", "Vdd", "B", "temp_inv")
    pfet(P["w_2"], "2", "Vdd", "C", "temp_inv")
    nfet(P["w_3"], "3",  "Vgnd", "A", "temp0")
    nfet(P["w_4"], "4", "temp0", "B", "temp1")
    nfet(P["w_5"], "5", "temp1", "C", "temp_inv")
    nfet(P["w_6"], "6", "Vgnd", "temp_inv", "X")
    pfet(P["w_7"], "7", "Vdd", "temp_inv", "X")


    spice = f"""
    .title slx
    .include "./prelude.spice"
    
    VVDD Vdd 0 1.8
    VVGND Vgnd 0 0
    
    VA A 0 {value_to_voltage(P["val_a"], P["transition"])}
    VB B 0 {value_to_voltage(P["val_b"], P["transition"])}
    VC C 0 {value_to_voltage(P["val_c"], P["transition"])}
    
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


randfet = lambda: min(100.0, 1.0 / np.sqrt(np.random.uniform(0, 1)) - 1 + 0.36)

sim_time = 3

def simulate(i):
    critical_which = 2

    value_a = np.random.randint(0, 2)
    value_b = np.random.randint(0, 2)
    value_c = 0

    def mk_val(value, critical, index):
        if index == critical:
            if value == 1:
                return "rise"
            return "fall"
        return "1.8"

    P = {
        "w_0": randfet(),
        "w_1": randfet(),
        "w_2": randfet(),
        "w_3": randfet(),
        "w_4": randfet(),
        "w_5": randfet(),
        "w_6": randfet(),
        "w_7": randfet(),

        "val_a": mk_val(value_a, critical_which, 0),
        "val_b": mk_val(value_b, critical_which, 1),
        "val_c": mk_val(value_c, critical_which, 2),

        "sim_time": sim_time,

        "transition": np.random.random() + 0.01,

        "capa_out_fF": 10 ** (3 * np.random.random()),
    }

    delta_time, transition = get_timing(P)



    if delta_time is None:
        return None

    P["out_delta_time"] = delta_time
    P["out_transition"] = transition

    p_json = json.dumps(P)
    return p_json


def worker(input_queue, output_queue):
    while True:
        i = input_queue.get()
        if i is None:
            break
        result = simulate(i)
        if result is None:
            continue
        output_queue.put(result)

if __name__ == "__main__":
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    num_workers = 15

    processes = [mp.Process(target=worker, args=(input_queue, output_queue)) for _ in range(num_workers)]
    for p in processes:
        p.start()


    def write_results(output_queue):
        with open("out_and3_test.njson", "a") as f:
            f.write("\n")
            t = time.time()
            i = 0
            while True:
                i += 1
                if i % 100 == 0:
                    print(i, time.time() - t)
                    t = time.time()
                result = output_queue.get()
                if result is None:
                    break
                f.write(result + "\n")

    write_process = mp.Process(target=write_results, args=(output_queue,))
    write_process.start()

    for i in range(100000):
        input_queue.put(i)

    for _ in range(num_workers):
        input_queue.put(None)


    for p in processes:
        p.join()
    write_process.join()