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
    nfet(P["w_0"], "0", "t1", "C", "t0")
    nfet(P["w_1"], "1", "t2", "t5", "Vgnd")
    nfet(P["w_2"], "2", "t3", "B", "t2")
    pfet(P["w_3"], "3", "t1", "t4", "t0")
    pfet(P["w_4"], "4", "t5", "t6", "t1")
    pfet(P["w_5"], "5", "X", "t0", "Vdd")
    nfet(P["w_6"], "6", "t6", "B", "Vgnd")
    nfet(P["w_7"], "7", "t2", "t6", "t1")
    nfet(P["w_8"], "8", "t5", "A", "Vgnd")
    pfet(P["w_9"], "9", "t3", "C", "t0")
    pfet(P["w_10"], "10", "t3", "t6", "t2")
    pfet(P["w_11"], "11", "t4", "C", "Vdd")
    pfet(P["w_12"], "12", "t2", "t5", "Vdd")
    nfet(P["w_13"], "13", "t5", "t6", "t3")
    pfet(P["w_14"], "14", "t5", "A", "Vdd")
    pfet(P["w_15"], "15", "t6", "B", "Vdd")
    nfet(P["w_16"], "16", "X", "t0", "Vgnd")
    pfet(P["w_17"], "17", "t5", "B", "t3")
    nfet(P["w_18"], "18", "t4", "C", "Vgnd")
    nfet(P["w_19"], "19", "t5", "B", "t1")
    nfet(P["w_20"], "20", "t3", "t4", "t0")
    pfet(P["w_21"], "21", "t2", "B", "t1")

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


randfet = lambda: min(100.0, 1.0 / math.sqrt(np.random.uniform(0, 1)) - 1 + 0.36)

sim_time = 30


def gen_test_set():
    with open("out_xor3_test.njson", "w") as f:
        for _ in range(300):
            P = {
                "w_0": 0.64,
                "w_1": 0.64,
                "w_2": 0.64,
                "w_3": 0.84,
                "w_4": 0.84,
                "w_5": 1.00,
                "w_6": 0.65,
                "w_7": 0.42,
                "w_8": 0.64,
                "w_9": 0.84,
                "w_10": 0.64,
                "w_11": 0.64,
                "w_12": 1.00,
                "w_13": 0.60,
                "w_14": 1.00,
                "w_15": 1.00,
                "w_16": 0.65,
                "w_17": 0.84,
                "w_18": 0.42,
                "w_19": 0.64,
                "w_20": 0.64,
                "w_21": 0.64,

                "val_a": "fall",
                "val_b": "0",
                "val_c": "1.8",

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
            f.write(p_json + "\n")


def simulate(i):
    # critical_which = np.random.randint(0, 3)
    #
    # value_a = np.random.randint(0, 2)
    # value_b = np.random.randint(0, 2)
    # value_c = np.random.randint(0, 2)

    critical_which = 0
    value_a = 0
    value_b = 0
    value_c = 1

    def mk_val(value, critical, index):
        if index == critical:
            if value == 1:
                return "rise"
            return "fall"

        if value == 1:
            return "1.8"
        return "0"

    P = {
        "w_0": randfet(),
        "w_1": randfet(),
        "w_2": randfet(),
        "w_3": randfet(),
        "w_4": randfet(),
        "w_5": randfet(),
        "w_6": randfet(),
        "w_7": randfet(),
        "w_8": randfet(),
        "w_9": randfet(),
        "w_10": randfet(),
        "w_11": randfet(),
        "w_12": randfet(),
        "w_13": randfet(),
        "w_14": randfet(),
        "w_15": randfet(),
        "w_16": randfet(),
        "w_17": randfet(),
        "w_18": randfet(),
        "w_19": randfet(),
        "w_20": randfet(),
        "w_21": randfet(),

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
    gen_test_set()
    exit(0)

    input_queue = mp.Queue()
    output_queue = mp.Queue()
    num_workers = 12

    processes = [mp.Process(target=worker, args=(input_queue, output_queue)) for _ in range(num_workers)]
    for p in processes:
        p.start()


    def write_results(output_queue):
        with open("out_xor3.njson", "a") as f:
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

    for i in range(1000000):
        input_queue.put(i)

    for _ in range(num_workers):
        input_queue.put(None)

    for p in processes:
        p.join()
    write_process.join()
