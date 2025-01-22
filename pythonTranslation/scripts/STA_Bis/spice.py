import subprocess
import tempfile


MINSIZE = 0.36
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
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={1} l=0.15"


def nfet(W, name, D, G, S):
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


def get_timing(P, subckt):
    fets = []

    for transistor in subckt["transistors"]:
        fetfun = pfet if transistor["type"] == "pfet" else nfet
        fets.append(fetfun(P["w_" + transistor["name"]], transistor["name"], transistor["source"], transistor["gate"],
                           transistor["drain"]))

    fets = "\n".join(fets)

    pin_values = []


    for p in P:
        if p.startswith("val_"):
            pin = p[4:]
            pin_values.append(f"V{pin} {pin} 0 {value_to_voltage(P[p], P['slew'])}")

    pin_values = "\n".join(pin_values)

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

.tran 5p {P["sim_time"]}n

.options AUTOSTOP

.meas tran x_cross when V({subckt["output_pin"]}) = 0.9
.meas tran x_start WHEN V({subckt["output_pin"]}) = {1.8 * 0.8}
.meas tran x_end   WHEN V({subckt["output_pin"]}) = {1.8 * 0.2}

.control
run


*plot V({subckt["output_pin"]}) V(S)
.endc
    """

    output, stderr = run_spice(spice)
    measures = parse_measures(output)

    if "x_cross" not in measures or "x_start" not in measures or "x_end" not in measures:
        print(P, output, stderr)
        exit(0)
        return None, None, None

    slew = abs(measures["x_end"] - measures["x_start"])
    delta_time = measures["x_cross"] - P["slew"] * 0.5e-9

    pin_capacitance = None
    if "tot_charge" in measures:
        pin_capacitance = abs(measures["tot_charge"] / 1.8)
    return delta_time * 1e9, slew * 1e9, pin_capacitance


def run_spice_timing(subckt, pin_state, w, capa, slew):

    P = {
        "i": 0,
        "sim_time": 1000,
        "slew": slew,
        "capa_out_fF": capa,
    }

    for pin,value in map(lambda x: x.split(":"), pin_state.split(",")):
        P[f"val_{pin}"] = value

    for i in range(len(w)):
        P[f"w_{i}"] = w[i]


    delta_time, slew, _ = get_timing(P, subckt)
    if delta_time is None:
        print("Failed to get timing")
        return None, None

    return delta_time, slew


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
