import json
import math
import time
import multiprocessing as mp
import re
from collections import defaultdict

from spice import parse_measures, run_spice
import numpy as np

MINSIZE = 0.36

pin_combinations = json.load(open("../libjson_parse/cells_transition_combinations.json"))

def area(W):
    return 0.15 * W

def perim(W):
    return 2 * (W + 0.15)

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"

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

def parse_netlist(netlist):
    subckt_pattern = re.compile(r"^\.subckt (\S+)(.*?)$")
    ends_pattern = re.compile(r"^\.ends$")
    transistor_pattern = re.compile(
        r"^X\d+ (\S+) (\S+) (\S+) (\S+) sky130_fd_pr__(nfet|pfet)_\S+"
    )

    subcircuits = {}
    subckt_sizes = defaultdict(list)
    current_subckt = None

    for line in netlist.splitlines():
        line = line.strip()
        if not line or line.startswith("*"):
            continue

        subckt_match = subckt_pattern.match(line)
        if subckt_match:
            current_subckt = subckt_match.group(1)
            current_pins = subckt_match.group(2).split()

            output_pin = current_pins[-1]
            input_pins = current_pins[:-5]

            power_pins = current_pins[-5:-1]
            if " ".join(power_pins) != "VGND VNB VPB VPWR":
                current_subckt = None
                continue

            if len(input_pins) == 0:
                current_subckt = None
                continue

            if output_pin == "Q" and "D" in input_pins:
                current_subckt = None
                continue

            if "lpflow" in current_subckt or "probe" in current_subckt or output_pin == "GCLK" or output_pin == "CLK":
                current_subckt = None
                continue

            if "dly" in current_subckt:
                current_subckt = None
                continue

            if current_subckt not in pin_combinations:
                current_subckt = None
                continue

            combination = pin_combinations[current_subckt]
            for pin in combination:
                if len(combination[pin]) == 0:
                    current_subckt = None
                    break

            if current_subckt is None:
                continue

            name_split = current_subckt.split("_")
            subckt_sizes["_".join(name_split[:-1])].append(int(name_split[-1]))

            subcircuits[current_subckt] = {"input_pins": input_pins, "output_pin": output_pin, "transistors": []}
            continue

        if ends_pattern.match(line):
            current_subckt = None
            continue

        if current_subckt:
            transistor_match = transistor_pattern.match(line)
            if transistor_match:
                source, gate, drain, bulk, type_ = transistor_match.groups()
                subcircuits[current_subckt]["transistors"].append(
                    {
                        "type": type_,
                        "source": source,
                        "gate": gate,
                        "drain": drain,
                        "bulk": bulk,
                    }
                )

    smallest_sizes = {}
    for subckt, sizes in subckt_sizes.items():
        smallest_sizes[subckt] = min(sizes)

    keys = list(subcircuits.keys())

    for key in keys:
        name_split = key.split("_")
        size = int(name_split[-1])
        if size != smallest_sizes["_".join(name_split[:-1])]:
            del subcircuits[key]

    print(*subcircuits.keys(), sep='\n')

    return subcircuits

def get_timing(P, subckt, pin_values):
    fets = []

    for transistor in subckt:
        fetfun = pfet if transistor["type"] == "pfet" else nfet
        fets.append(fetfun(P["w_" + transistor["name"]], transistor["name"], pin_values[transistor["source"]], pin_values[transistor["gate"]], pin_values[transistor["drain"]]))

    fets = "\n".join(fets)

    spice = f"""
    .title slx
    .include "./prelude.spice"
    
    VVDD Vdd 0 1.8
    VVGND Vgnd 0 0
    
    VA A 0 {value_to_voltage(P["val_a"], P["transition"])}
    VB B 0 {value_to_voltage(P["val_b"], P["transition"])}
    VC C 0 {value_to_voltage(P["val_c"], P["transition"])}
    
    CX X 0 {P["capa_out_fF"]}f
    
    {fets}
    
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

sim_time = 10

def simulate(subckt):
    combination_by_pin = pin_combinations[subckt]

    critical_which = np.random.randint(0, 3)

    value_a = np.random.randint(0, 2)
    value_b = np.random.randint(0, 2)
    value_c = np.random.randint(0, 2)

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
    circuits = parse_netlist(open("hd_nopex.spice").read())
    print(len(circuits))

    print(sum(sum(len(combination) for combination in pin_combinations[subckt].values()) for subckt in circuits))

    exit(0)

    input_queue = mp.Queue()
    output_queue = mp.Queue()
    num_workers = 15

    processes = [mp.Process(target=worker, args=(input_queue, output_queue)) for _ in range(num_workers)]
    for p in processes:
        p.start()


    def write_results(output_queue):
        with open("out_and3.njson", "a") as f:
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