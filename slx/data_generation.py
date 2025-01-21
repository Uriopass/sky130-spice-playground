import json
import math
import time
import multiprocessing as mp
import re
from collections import defaultdict

from spice import parse_measures, run_spice, run_spice_plot
import numpy as np

MINSIZE = 0.36

pin_combinations = json.load(open("../libjson_parse/cells_transition_combinations.json"))

pin_combinations["sky130_fd_sc_hs__bufbuf_1"] = pin_combinations["sky130_fd_sc_hs__bufbuf_8"]
pin_combinations["sky130_fd_sc_hs__bufinv_1"] = pin_combinations["sky130_fd_sc_hs__bufinv_8"]
pin_combinations["sky130_fd_sc_hs__clkinv_0"] = pin_combinations["sky130_fd_sc_hs__clkinv_1"]


def area(W):
    return 0.15 * W

def perim(W):
    return 2 * (W + 0.15)

def pfet_hs(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def nfet_hs(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    mult = W
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8_lvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"

slew_to_pulse_arc = 1.0 / (0.8 - 0.2)

def value_to_voltage(value, slew):
    if value == "0" or value == 0:
        return 0
    if value == "1" or value == 1:
        return 1.8
    if value == "rise":
        return f"PULSE(0 1.8 0 {slew * slew_to_pulse_arc}n 0.1n 100n 100n)"
    if value == "fall":
        return f"PULSE(1.8 0 0 {slew * slew_to_pulse_arc}n 0.1n 100n 100n)"
    raise ValueError(f"Unknown value for voltage conv {value}")

def parse_netlist(netlist):
    subckt_pattern = re.compile(r"^\.subckt (\S+)(.*?)$")
    ends_pattern = re.compile(r"^\.ends$")
    transistor_pattern = re.compile(
        r"^X(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+sky130_fd_pr__(nfet|pfet)_\S+"
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

            subcircuits[current_subckt] = {"name": current_subckt, "input_pins": input_pins, "output_pin": output_pin, "transistors": []}
            continue

        if ends_pattern.match(line):
            current_subckt = None
            continue

        if current_subckt:
            transistor_match = transistor_pattern.match(line)
            if transistor_match:
                name, source, gate, drain, bulk, type_ = transistor_match.groups()

                subcircuits[current_subckt]["transistors"].append(
                    {
                        "type": type_,
                        "name": name,
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

    for key in list(subcircuits.keys()):
        circuit_name_without_size = "_".join(key.split("_")[:-1])
        subcircuits[circuit_name_without_size] = subcircuits.pop(key)

    for current_subckt, circuit in subcircuits.items():
        circuit["output_transistors"] = []
        for t1 in circuit["transistors"]:
            source = t1["source"]
            gate = t1["gate"]
            drain = t1["drain"]

            for transistor in circuit["transistors"]:
                if t1["name"] == transistor["name"]:
                    continue
                if transistor["source"] == source and transistor["gate"] == gate and transistor["drain"] == drain:
                    print("duplicate in", current_subckt)
                    break
                if transistor["source"] == drain and transistor["gate"] == gate and transistor["drain"] == source:
                    print("duplicate in", current_subckt)
                    break

            if source == circuit["output_pin"] or drain == circuit["output_pin"]:
                circuit["output_transistors"].append(t1)
    return subcircuits

def get_timing(P, subckt):
    fets = []

    for transistor in subckt["transistors"]:
        fetfun = pfet_hs if transistor["type"] == "pfet" else nfet_hs
        fets.append(fetfun(P["w_" + transistor["name"]], transistor["name"], transistor["source"], transistor["gate"], transistor["drain"]))

    fets = "\n".join(fets)

    pin_values = []

    commuting_pin = None

    for p in P:
        if p.startswith("val_"):
            pin = p[4:]
            if P[p] == "rise" or P[p] == "fall":
                commuting_pin = pin
            pin_values.append(f"V{pin} {pin} 0 {value_to_voltage(P[p], P['slew'])}")

    pin_values = "\n".join(pin_values)

    measure_integral = ""

    if P["i"] % 5 == 0:
        measure_integral = f".meas tran tot_charge INTEG V{commuting_pin}#branch from=0 to={P['sim_time']}n"

    spice = f"""
.title slx
.include "./prelude.spice"

VVdd Vdd 0 1.8

VVPWR VPWR 0 1.8
VVPB VPB 0 1.8
VVNB VNB 0 0
VVGND VGND 0 0

{pin_values}

Cout {subckt["output_pin"]} 0 {P["capa_out_fF"]}f

{fets}

.tran 0.005n {P["sim_time"]}n

.options AUTOSTOP

.meas tran x_cross when V({subckt["output_pin"]}) = 0.9
.meas tran x_start WHEN V({subckt["output_pin"]}) = {1.8 * 0.8}
.meas tran x_end   WHEN V({subckt["output_pin"]}) = {1.8 * 0.2}
{measure_integral}

.control
run


*plot V({subckt["output_pin"]}) V(S)
.endc
    """

    output, stderr = run_spice(spice)
    measures = parse_measures(output)

    if "x_cross" not in measures or "x_start" not in measures or "x_end" not in measures:
        #print(output, stderr)
        return None, None, None

    slew = abs(measures["x_end"] - measures["x_start"])
    delta_time = measures["x_cross"] - P["slew"] * 0.5e-9

    pin_capacitance = None
    if "tot_charge" in measures:
        pin_capacitance = abs(measures["tot_charge"] / 1.8)
    return delta_time, slew, pin_capacitance

randnfet = lambda: min(100.0, 0.8 * (1.0 / math.sqrt(np.random.uniform(0, 1)) - 1) + 0.36)
randpfet = lambda: min(100.0, 1.0 / math.sqrt(np.random.uniform(0, 1)) - 1 + 0.36)

sim_time = 4

def simulate(subckt, i):
    combination_by_pin = pin_combinations[subckt["name"]]


    for pin, pin_combs in combination_by_pin.items():
        for risefall in range(2):
            for pin_comb in pin_combs:
                while True:
                    P = {
                        "i": i,
                        "sim_time": sim_time,

                        "slew": np.random.random() * (0.35 - 0.04) + 0.04,

                        "capa_out_fF": 10 ** (2.7 * np.random.random()),

                        f"val_{pin}": "rise" if risefall == 0 else "fall"
                    }

                    for other_pin, value in pin_comb["pins"].items():
                        P["val_" + other_pin] = "1" if value else "0"

                    for transistor in subckt["transistors"]:
                        fet_size = randpfet() if transistor["type"] == "pfet" else randnfet()
                        P["w_" + transistor["name"]] = fet_size

                    for transistor in subckt["output_transistors"]:
                        capa = P["capa_out_fF"]
                        P["w_" + transistor["name"]] += np.random.uniform(0, 1) * capa * 0.01

                    delta_time, slew, pin_capacitance = get_timing(P, subckt)

                    if delta_time is None:
                        continue

                    P["out_delta_time"] = delta_time * 1e9
                    P["out_slew"] = slew * 1e9

                    if pin_capacitance is not None:
                        P["commuting_pin_capacitance"] = pin_capacitance * 1e15

                    p_json = json.dumps(P)
                    yield p_json
                    break

def worker(subckt, input_queue, output_queue):
    while True:
        i = input_queue.get()
        if i is None:
            break
        for result in simulate(subckt, i):
            if result is None:
                continue
            output_queue.put(result)

if __name__ == "__main__":
    circuits = parse_netlist(open("hs_nopex.spice").read())

    """
    P = {
        "sim_time": sim_time,

        "slew": 0.06116666,

        "capa_out_fF": 43.725986,

        "val_A0": "fall",
        "val_S": "0",
        "val_A1": "1",

        "w_0": 10 * 0.64,
        "w_1": 8 * 0.42,
        "w_2": 0.36,
        "w_3": 0.64,
        "w_4": 0.36,
        "w_5": 0.36,
        "w_6": 6 * 0.64,
        "w_7": 2.0 * 1.30,
        "w_8": 4.0 * 2.00,
        "w_9": 0.36,
        "w_10": 0.42,
        "w_11": 10 * 0.42,
    }

    real_dt, real_trans = get_timing(P, circuits["sky130_fd_sc_hd__mux2_1"])
    print(f"{real_dt * 1e9}n {real_trans * 1e9}n")
    exit(0)
    """

    for circuit_name, circuit in sorted(circuits.items()):
        print("gonna do", circuit_name)
        t_start = time.time()
        input_queue = mp.Queue()
        output_queue = mp.Queue()
        num_workers = 20

        processes = [mp.Process(target=worker, args=(circuit, input_queue, output_queue)) for _ in range(num_workers)]
        for p in processes:
            p.start()

        def write_results(out_name, output_queue):
            with open(out_name, "a") as f:
                f.write("\n")
                t = time.time()
                i = 0
                while True:
                    i += 1
                    if i % 1000 == 0:
                        print(i, time.time() - t)
                        t = time.time()
                    result = output_queue.get()
                    if result is None:
                        print(i, time.time() - t, "done")
                        break
                    f.write(result + "\n")

        write_process = mp.Process(target=write_results, args=(f"data/{circuit_name}.njson", output_queue))
        write_process.start()

        for i in range(2000):
            input_queue.put(i)

        for _ in range(num_workers):
            input_queue.put(None)

        for p in processes:
            p.join()

        output_queue.put(None)
        write_process.join()

        print(circuit_name, "in", time.time() - t_start)