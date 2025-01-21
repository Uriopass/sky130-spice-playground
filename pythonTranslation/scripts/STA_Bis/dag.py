import json
import os.path
import pickle
import subprocess
import tempfile
from collections import defaultdict, deque
import re
import multiprocessing as mp

import numpy as np
import netCDF4 as nc
from tqdm import tqdm

pin_combinations = json.load(open("../../../libjson_parse/cells_transition_combinations.json"))
pin_combinations["sky130_fd_sc_hs__bufbuf_1"] = pin_combinations["sky130_fd_sc_hs__bufbuf_8"]
pin_combinations["sky130_fd_sc_hs__bufinv_1"] = pin_combinations["sky130_fd_sc_hs__bufinv_8"]
pin_combinations["sky130_fd_sc_hs__clkinv_0"] = pin_combinations["sky130_fd_sc_hs__clkinv_1"]


def parallel_work(l, arg, f):
    num_workers = 24
    input_queue = mp.Queue(len(l))
    output_queue = mp.Queue(num_workers * 3)

    results = [None] * len(l)

    def f_worker(arg, input_queue, output_queue):
        for i, v in iter(input_queue.get, None):
            result = f(v, arg)
            output_queue.put((i, result))

    processes = [mp.Process(target=f_worker, args=(arg, input_queue, output_queue)) for _ in range(num_workers)]
    for p in processes:
        p.start()

    for i,v in enumerate(l):
        input_queue.put((i, v))

    for _ in range(num_workers):
        input_queue.put(None)

    for _ in tqdm(range(len(l))):
        i, result = output_queue.get()
        results[i] = result

    for p in processes:
        p.join()


    return results

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
def dict_to_string(d):
    return ",".join(f"{k}:{d[k]}" for k in sorted(d.keys()))

def parse_netlist(netlist):
    subckt_pattern = re.compile(r"^\.subckt (\S+)(.*?)$")
    ends_pattern = re.compile(r"^\.ends$")
    transistor_pattern = re.compile(
        r"^X(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+sky130_fd_pr__(nfet|pfet)_\S+\s+w=(\S+)"
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
                name, source, gate, drain, bulk, type_, w = transistor_match.groups()

                subcircuits[current_subckt]["transistors"].append(
                    {
                        "type": type_,
                        "name": name,
                        "source": source,
                        "gate": gate,
                        "drain": drain,
                        "bulk": bulk,
                        "w": float(w)
                    }
                )

    smallest_sizes = {}
    for subckt, sizes in subckt_sizes.items():
        smallest_sizes[subckt] = min(sizes)

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
                    #print("duplicate in", current_subckt)
                    break
                if transistor["source"] == drain and transistor["gate"] == gate and transistor["drain"] == source:
                    #print("duplicate in", current_subckt)
                    break

            if source == circuit["output_pin"] or drain == circuit["output_pin"]:
                circuit["output_transistors"].append(t1)


    for key in list(subcircuits.keys()):
        circuit_name_without_size = "_".join(key.split("_")[:-1])
        smallest_size = smallest_sizes[circuit_name_without_size]
        subcircuits[circuit_name_without_size] = subcircuits[circuit_name_without_size+"_"+str(smallest_size)]

    return subcircuits

circuits = parse_netlist(open("../../../slx/hs_nopex.spice").read())
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

def run_spice_timing(celltype, pin_state, w, capa, slew):
    subckt = circuits[celltype]

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

def mk_vector(w, capa, slew):
    numb_fets = len(w)
    input_tensor = np.zeros(3 + numb_fets * 5 + numb_fets * (numb_fets - 1) * 2)

    #todo!!: this will change when new models are added
    slew = slew * slew_to_pulse_arc

    input_tensor[0] = 1.0
    input_tensor[1] = slew
    input_tensor[2] = capa

    for j in range(numb_fets):
        w_j = w[j]
        input_tensor[3 + j * 5    ] = 1.0 / w_j
        input_tensor[3 + j * 5 + 1] = capa / w_j
        input_tensor[3 + j * 5 + 2] = np.cbrt(capa / w_j)
        input_tensor[3 + j * 5 + 3] = np.sqrt(slew / w_j)
        input_tensor[3 + j * 5 + 4] = np.cbrt(slew * capa / w_j)

    for j in range(numb_fets):
        w_j = w[j]
        off = 3 + numb_fets * 5 + j * (numb_fets - 1) * 2
        for k in range(numb_fets):
            if j == k:
                continue
            w_k = w[k]
            input_tensor[off + (k - (1 if k > j else 0)) * 2    ] = w_j / w_k
            input_tensor[off + (k - (1 if k > j else 0)) * 2 + 1] = capa / (w_j + w_k)
    return input_tensor

class DAG:
    def __init__(self):
        self.rev_graph = defaultdict(list)  # Adjacency list: node -> list of (neighbor, edge_weight)
        self.graph = defaultdict(list)      # Adjacency list: node -> list of (neighbor, edge_weight)
        self.sdf_node_time = {}         # Node weights: node -> time
        self.instance_to_cell_type = {} # Instance to cell type mapping
        self.instance_to_cell_type_full = {} # Instance to full cell type mapping

    def add_node(self, node, weight=0.):
        """Add a node with its weight."""
        self.sdf_node_time[node] = weight
        if node not in self.rev_graph:
            self.rev_graph[node] = []

    def add_edge(self, u, v, weight=0.):
        """Add an edge with its weight."""
        self.rev_graph[v].append((u, weight))

    def topological_sort(self):
        """Perform topological sorting of the DAG."""
        in_degree = defaultdict(int)
        for u in self.rev_graph:
            for v, _ in self.rev_graph[u]:
                in_degree[v] += 1

        queue = deque([node for node in self.sdf_node_time if in_degree[node] == 0])
        top_order = []

        while queue:
            u = queue.popleft()
            top_order.append(u)
            for v, _ in self.rev_graph.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        top_order.reverse()
        return top_order

    def get_end_nodes(self):
        """Return a list of nodes with no incoming edges."""
        in_degree = defaultdict(int)
        for u in self.rev_graph:
            for v, _ in self.rev_graph[u]:
                in_degree[v] += 1
        start_nodes = [node for node in self.sdf_node_time if in_degree[node] == 0]
        return start_nodes

    def get_start_nodes(self):
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [child for child, parents in self.rev_graph.items() if len(parents) == 0]
        return end_nodes

    def longest_path_linear_sta(self, groundtruth=False):
        print("starting linear STA")
        cell_widths = {}
        all_celltypes = set()
        for instance, celltype in self.instance_to_cell_type.items():
            if celltype not in circuits:
                print("Circuit not found for", celltype)
                continue
            circuit = circuits[celltype]

            w = [0]*len(circuit["transistors"])
            for transistor in circuit["transistors"]:
                w[int(transistor["name"])] = transistor["w"]


            size = min(4, max(1, int(self.instance_to_cell_type_full[instance].split("_")[-1])))
            for transistor in circuit["output_transistors"]:
                w[int(transistor["name"])] *= size

            cell_widths[instance] = w
            all_celltypes.add(celltype)
        print("created cell widths")

        linear_estimators = {}

        if os.name == 'nt':
            print("CDF files cannot be read on windows for some reason wtf, please run on linux")
            exit(0)

        for celltype in all_celltypes:
            with nc.Dataset(f"../../../slx/models/{celltype}.nc", "r") as f:
                for group, case in f.groups.items():
                    linear_estimator = case.variables["linear_estimator"][:,:]
                    linear_estimator_capa = case.variables["linear_estimator_capa"][:,:]

                    linear_estimators[f"{celltype}@{group}"] = (linear_estimator, linear_estimator_capa)
        print("parsed needed linear estimators")

        node_out_capa = defaultdict(float)
        node_seen_instance = defaultdict(list)

        for child in self.rev_graph:
            instance, pin_state = child.split("@")
            celltype = self.instance_to_cell_type[instance]

            _, capa_estimator = linear_estimators[f"{celltype}@{pin_state}"]

            capa = (np.array(cell_widths[instance]) @ capa_estimator)[0]
            for parent, _ in self.rev_graph[child]:
                if instance not in node_seen_instance[parent]:
                    node_seen_instance[parent].append(instance)
                    node_out_capa[parent] += capa

        for node in self.rev_graph:
            if node not in node_out_capa:
                node_out_capa[node] = 2.0
        print("computed node capas")

        node_depth = defaultdict(int)

        cur_nodes = list(self.get_start_nodes())
        next_nodes = set()
        maxdepth = 0

        for node in cur_nodes:
            node_depth[node] = 0

        while True:
            for node in cur_nodes:
                for child, _ in self.graph.get(node, []):
                    node_depth[child] = max(node_depth[child], node_depth[node] + 1)
                    next_nodes.add(child)
            if len(next_nodes) == 0:
                break
            cur_nodes = list(next_nodes)
            next_nodes = set()
            maxdepth += 1

        nodes_by_depths = [[] for _ in range(maxdepth + 1)]
        for node, depth in node_depth.items():
            nodes_by_depths[depth].append(node)

        print(*(len(nodes) for nodes in nodes_by_depths))

        time_slew = {node: (0.0, 0.0) for node in self.sdf_node_time}

        path_parent = {node: None for node in self.sdf_node_time}

        start_nodes = self.get_start_nodes()
        print(f"got {len(start_nodes)} start nodes")




        def process_node(child, time_slew):
            instance, pin_state = child.split("@")
            celltype = self.instance_to_cell_type[instance]
            linear_estimator, _ = linear_estimators[f"{celltype}@{pin_state}"]

            time_slews_parent = []
            for parent, edge_weight in self.rev_graph.get(child, []):
                t_parent, slew = time_slew[parent]
                time_slews_parent.append((t_parent + edge_weight, slew, parent))

            if len(time_slews_parent) == 0:
                is_falling = False
                for pin in pin_state.split(","):
                    if pin.endswith("fall"):
                        is_falling = True
                        break

                slew = 0.1
                if is_falling:
                    slew = 0.06

                if groundtruth:
                    dt, slew = run_spice_timing(celltype, pin_state, cell_widths[instance], node_out_capa[child], slew)
                else:
                    v = mk_vector(cell_widths[instance], node_out_capa[child], slew)

                    dtslew = np.dot(v, linear_estimator)
                    dt, slew = dtslew[0], dtslew[1]
                return dt, slew, None

            t_parent, slew_parent, parent = max(time_slews_parent)

            if groundtruth:
                dt, slew = run_spice_timing(celltype, pin_state, cell_widths[instance], node_out_capa[child], slew_parent)
            else:
                linear_estimator, _ = linear_estimators[f"{celltype}@{pin_state}"]
                v = mk_vector(cell_widths[instance], node_out_capa[child], slew_parent)
                dtslew = np.dot(v, linear_estimator)
                dt, slew = dtslew[0], dtslew[1]

            return t_parent + dt, slew, parent

        for depth, nodes in enumerate(nodes_by_depths):
            results = parallel_work(nodes, time_slew, process_node)
            for node, result in zip(nodes, results):
                time_slew[node] = (result[0], result[1])
                path_parent[node] = result[2]

        argmax_time = max(time_slew.keys(), key=time_slew.get)

        path = []
        node = argmax_time
        while node is not None:
            path.append((node, time_slew[node][0]))
            node = path_parent[node]

        path.reverse()
        return path, time_slew[argmax_time][0]

    def longest_path(self):
        """Compute the top N longest paths in the DAG, including accumulated times."""
        top_order = self.topological_sort()
        time = {node: 0 for node in self.sdf_node_time}
        parent_p = {node: None for node in self.sdf_node_time}

        for node in top_order:
            maxt = None
            node_time = self.sdf_node_time[node]
            for parent, edge_weight in self.rev_graph.get(node, []):
                newt = time[parent] + edge_weight + node_time
                if maxt is None or newt > maxt:
                    maxt = newt
                    parent_p[node] = parent
            if maxt is None:
                maxt = node_time
            time[node] = maxt

        argmax_time = max(time.keys(), key=time.get)

        path = []
        node = argmax_time
        while node is not None:
            path.append((node, time[node]))
            node = parent_p[node]

        path.reverse()
        return path, time[argmax_time]

    def set_instance_to_cell_type(self, instance_to_cell_type):
        self.instance_to_cell_type = instance_to_cell_type

    def set_instance_to_cell_type_full(self, instance_to_cell_type_full):
        self.instance_to_cell_type_full = instance_to_cell_type_full

    def remove_delay_gates(self):
        affected_nodes = []
        node_parents = defaultdict(list)

        for node in self.rev_graph:
            instance, _ = node.split("@")
            celltype = self.instance_to_cell_type[instance]
            if "dly" in celltype:
                affected_nodes.append(node)
            for neighbor, _ in self.rev_graph.get(node, []):
                instance, _ = neighbor.split("@")
                celltype = self.instance_to_cell_type[instance]
                if "dly" in celltype:
                    node_parents[neighbor].append(node)

        # connect all inputs to all outputs
        for node in affected_nodes:
            for input_node in node_parents[node]:
                for neighbor in self.rev_graph[node]:
                    self.rev_graph[input_node].append((neighbor[0], neighbor[1]))
                    node_parents[neighbor[0]].append(input_node)
                for i in range(len(self.rev_graph[input_node])):
                    if self.rev_graph[input_node][i][0] == node:
                        del self.rev_graph[input_node][i]
                        break
            del self.rev_graph[node]
            del self.sdf_node_time[node]

            instance = node.split("@")[0]
            if instance in self.instance_to_cell_type:
                del self.instance_to_cell_type[instance]

        for node in affected_nodes:
            if node in self.rev_graph:
                del self.rev_graph[node]

    def save_to_file(self, file_path):
        """Serialize the DAG to a JSON file."""
        # Convert defaultdict to a regular dict for JSON serialization
        rev_graph_dict = {node: neighbors for node, neighbors in self.rev_graph.items()}
        graph_dict = {}

        for node, neighbors in self.rev_graph.items():
            for neighbor, weight in neighbors:
                if neighbor not in graph_dict:
                    graph_dict[neighbor] = []
                graph_dict[neighbor].append((node, weight))

        data = {
            'graph': graph_dict,
            'rev_graph': rev_graph_dict,
            'node_weights': self.sdf_node_time,
            'instance_to_cell_type': self.instance_to_cell_type,
            'instance_to_cell_type_full': self.instance_to_cell_type_full
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load_from_file(cls, file_path):
        """Deserialize the DAG from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        dag = cls()
        dag.sdf_node_time = data['node_weights']
        dag.rev_graph = defaultdict(list, {
            node: [(neighbor, weight) for neighbor, weight in neighbors]
            for node, neighbors in data['rev_graph'].items()
        })
        dag.graph = defaultdict(list, {
            node: [(neighbor, weight) for neighbor, weight in neighbors]
            for node, neighbors in data['graph'].items()
        })
        dag.instance_to_cell_type = data['instance_to_cell_type']
        dag.instance_to_cell_type_full = data['instance_to_cell_type_full']
        return dag


def temp():
    with open('hs_saved_instance_to_cell_type.pkl', 'rb') as f:
        instance_to_cell_type = pickle.load(f)

    with open('hs_saved_instance_to_cell_type_full.pkl', 'rb') as f:
        instance_to_cell_type_full = pickle.load(f)

    # opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/hs_picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    with open('hs_saved_nods.pkl', 'rb') as f:
        nods = pickle.load(f)

    print("read sdf and nods")

    nod_names = list(nods.keys())

    dag = DAG()

    for i in range(len(sdf_content)):
        line = sdf_content[i]
        if line == '  (CELLTYPE "picorv32")' or line == '  (CELLTYPE "spm")':
            j = i+4
            while "INTERCONNECT" in sdf_content[j]:
                words = sdf_content[j].replace("(", "").replace(")", "").split(" ")

                if len(words[5].split(".")) == 1:
                    j += 1
                    if words[5] in instance_to_cell_type.keys():
                        print(words[5])
                        print(nods[words[5]])
                    continue

                instance_1 = words[5].split(".")[0]
                instance_2 = words[6].split(".")[0]
                if instance_1 not in instance_to_cell_type.keys() or instance_2 not in instance_to_cell_type.keys():
                    j += 1
                    continue

                if "dfxtp" in instance_to_cell_type[instance_1] or "dfxtp" in instance_to_cell_type[instance_2] or "dfrtp" in instance_to_cell_type[instance_1] or "dfrtp" in instance_to_cell_type[instance_2]:
                    j += 1
                    continue

                if "_07331_" in instance_1 or "_07331_" in instance_2:
                    j += 1
                    continue

                pin_1 = words[5].split(".")[1]
                pin_2 = words[6].split(".")[1]

                if instance_1 in nod_names and instance_2 in nod_names:
                    for s2 in nods[instance_2]:
                        for s1 in nods[instance_1]:
                            if len(words) == 8:
                                words.append(words[7])
                            if s2[0][pin_2] == "fall" and s1[1][0] == 0:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]), instance_2 + "@" + dict_to_string(s2[0]), float(words[8].split(":")[0]))
                            elif s2[0][pin_2] == "rise" and s1[1][0] == 1:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]), instance_2 + "@" + dict_to_string(s2[0]), float(words[7].split(":")[0]))

                j += 1
    print("prepared the dag")
    dag.set_instance_to_cell_type(instance_to_cell_type)
    dag.set_instance_to_cell_type_full(instance_to_cell_type_full)
    dag.remove_delay_gates()
    dag.save_to_file("dag_hs.json")

if __name__ == "__main__":
    temp()
