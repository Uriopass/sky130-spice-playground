import json
import re
from collections import defaultdict

pin_combinations = json.load(open("../libjson_parse/cells_transition_combinations.json"))

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

            subcircuits[current_subckt] = {"name": current_subckt, "transistors": []}
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
        subcircuits[key]['smallest_parent'] = key
        smallest_size = smallest_sizes["_".join(name_split[:-1])]
        if size != smallest_size:
            subcircuits[key]['smallest_parent'] = "_".join(name_split[:-1]) + "_" + str(smallest_size)

    return subcircuits


src = parse_netlist(open("sky130_subckt").read())
dst = parse_netlist(open("hd_nopex.spice").read())

transistor_maps = {}

for key in src:
    if key not in dst:
        print(key)
        continue


    dst_smallest = dst[key]['smallest_parent']

    csrc = src[key]
    cdst = dst[dst_smallest]

    transistor_map = {}

    temp_variables_src = set()
    temp_variables_dst = set()

    for tsrc in csrc['transistors']:
        temp_variables_src.add(tsrc['source'])
        temp_variables_src.add(tsrc['gate'])
        temp_variables_src.add(tsrc['drain'])

    for tdst in cdst['transistors']:
        temp_variables_dst.add(tdst['source'])
        temp_variables_dst.add(tdst['gate'])
        temp_variables_dst.add(tdst['drain'])

    temp_variables_src = list(v for v in temp_variables_src if v.startswith("a_") and v.endswith("#"))
    temp_variables_dst = list(v for v in temp_variables_dst if v.startswith("a_") and v.endswith("#"))

    #print(temp_variables_src, temp_variables_dst)

    print(len(temp_variables_dst) ** len(temp_variables_src))

    # map transistors names from src to dst

    for tsrc in csrc['transistors']:
        for tdst in cdst['transistors']:
            if tsrc['source'] == tdst['source'] and tsrc['gate'] == tdst['gate'] and tsrc['drain'] == tdst['drain']:
                transistor_map[tsrc['name']] = tdst['name']
                break
            if tsrc['source'] == tdst['drain'] and tsrc['gate'] == tdst['gate'] and tsrc['drain'] == tdst['source']:
                transistor_map[tsrc['name']] = tdst['name']
                break
    #print(key, transistor_map)
    transistor_maps[key] = transistor_map

with open("sky130_subckt_to_hd_nopex.json", "w") as f:
    json.dump(transistor_maps, f)