def parse_spice(spice_path):
    with open(spice_path, 'r') as f:
        spice_content = f.read()
    spice_content = spice_content.split("\n")

    for i in range(len(spice_content)):
        spice_content[i] = spice_content[i].strip()

    cells = []
    pin_p_max_sizes = {}
    pin_n_max_sizes = {}
    plotline = None

    i = 0
    celltype = ""
    while i < len(spice_content):
        line = spice_content[i]

        if line.startswith("plot "):
            plotline = i
            i += 1
            continue

        if line == "* pins":
            pin_p_max_sizes = {}
            pin_n_max_sizes = {}

            i += 1
            line = spice_content[i]
            while len(line) != 0:
                if line[0] == "*":
                    pin_parameters = line.split(" ")
                    if pin_parameters[1] == "maxw_p":
                        pin_p_max_sizes[pin_parameters[2]] = float(pin_parameters[3])
                    else:
                        pin_n_max_sizes[pin_parameters[2]] = float(pin_parameters[3])
                i += 1
                line = spice_content[i]
            else:
                i += 1
        elif line.startswith("* celltype"):
            celltype = line.split(" ")[-1]
            i += 1
        elif line == "* cell":

            i += 1
            line = spice_content[i]

            transistors = []

            while len(line) != 0 and line[0] == "X":
                transistor_parameters = line.split(" ")
                if len(line.split(" ")) != 12:
                    i += 1
                    line = spice_content[i]
                    continue

                transistor = {
                    "line": i,
                    "name": transistor_parameters[0][1:],
                    "drain": transistor_parameters[1],
                    "gate": transistor_parameters[2],
                    "source": transistor_parameters[3],
                    "bulk": transistor_parameters[4],
                    "instance": transistor_parameters[5],
                    "ad": transistor_parameters[6],
                    "pd": transistor_parameters[7],
                    "as": transistor_parameters[8],
                    "ps": transistor_parameters[9],
                    "w": float(transistor_parameters[10].split("=")[1]),
                    "l": float(transistor_parameters[11].split("=")[1])
                }
                if transistor["gate"] in pin_p_max_sizes.keys():
                    transistor["max_size"] = pin_p_max_sizes[transistor["gate"]]
                elif transistor["gate"] in pin_n_max_sizes.keys():
                    transistor["max_size"] = pin_n_max_sizes[transistor["gate"]]

                transistors.append(transistor)
                i += 1
                line = spice_content[i]
            cells.append({
                "celltype": celltype,
                "transistors": transistors
            })
            celltype = ""
        else:
            i += 1
    return cells, plotline


def spice_to_python(cells, plotline):
    python_code = """import bisect

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

MINSIZE = 0.36

timings_to_track = set()

def area(W):
    return 0.15 * W

def perim(W):
    return 2*(W + 0.15)

def pfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: pfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    closest_bin = bins_pfet[min(bisect.bisect_left(bins_pfet, W), len(bins_pfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vdd sky130_fd_pr__pfet_01v8_hvt ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

def nfet(W, name, D, G, S):
    if W < MINSIZE:
        print(f"Warning: nfet {name} has width {W} which is less than the minimum size of {MINSIZE}")

    timings_to_track.add(D)
    timings_to_track.add(G)
    timings_to_track.add(S)

    closest_bin = bins_nfet[min(bisect.bisect_left(bins_nfet, W), len(bins_nfet) - 1)]
    mult = W / closest_bin
    ar = area(W) / mult
    pe = perim(W) / mult
    return f"X{name} {D} {G} {S} Vgnd sky130_fd_pr__nfet_01v8 ad={ar} as={ar} pd={pe} ps={pe} m={mult} w={closest_bin} l=0.15"

with open("../../libs/ngspice/out.spice", 'r') as f:
    spice = f.read()

spice = spice.split('\\n')
"""

    for cell in cells:
        all_pins = set()
        celltype = cell["celltype"]
        python_code += f"# === {celltype} ===\n"
        for transistor in cell["transistors"]:
            all_pins.add(transistor["drain"])
            all_pins.add(transistor["gate"])
            all_pins.add(transistor["source"])
            function_name = "pfet" if "pfet" in transistor["instance"] else "nfet"

            line = f'spice[{transistor["line"]:>4}] = {function_name}({transistor["w"]:.2f}, "{transistor["name"]}", "{transistor["drain"]}", "{transistor["gate"]}", "{transistor["source"]}")'
            if "max_size" in transistor.keys():
                nb_spaces = 71 - len(line)

                python_code += line + nb_spaces * " " + f'# Max size: {transistor["max_size"]}\n'
            else:
                python_code += line + '\n'

        for pin in all_pins:
            if pin == "Vdd" or pin == "Vgnd":
                continue
            python_code += f"# timing for {pin:>10}:\n"

        python_code += "\n\n"
    python_code += f"""

spice[{plotline}] = ""
for name in timings_to_track:
    spice.insert({plotline}, f"meas tran {{name}} when V({{name}}) = 0.9")

spice = "\\n".join(spice)
file_name = "../../../simulations/generated_out.spice"
with open(file_name, "w") as file:
    file.write(spice)
    """

    file_name = "python_spice.py"
    # Write the string to the .py file
    with open(file_name, "w") as file:
        file.write(python_code)


def main():
    spice_path = "../../libs/ngspice/out.spice"
    cells, plotline = parse_spice(spice_path)

    spice_to_python(cells, plotline)


if __name__ == "__main__":
    main()
