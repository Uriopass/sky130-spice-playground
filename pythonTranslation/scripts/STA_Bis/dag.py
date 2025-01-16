import json
import pickle
from collections import defaultdict, deque
import re

pin_combinations = json.load(open("../../../libjson_parse/cells_transition_combinations.json"))
pin_combinations["sky130_fd_sc_hs__bufbuf_1"] = pin_combinations["sky130_fd_sc_hs__bufbuf_8"]
pin_combinations["sky130_fd_sc_hs__bufinv_1"] = pin_combinations["sky130_fd_sc_hs__bufinv_8"]
pin_combinations["sky130_fd_sc_hs__clkinv_0"] = pin_combinations["sky130_fd_sc_hs__clkinv_1"]

def dict_to_string(d):
    s = ""
    for k, v in d.items():
        s += f"{k}:{v},"
    return s[:-1]

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

circuits = parse_netlist(open("../../../slx/hs_nopex.spice").read())

class DAG:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list: node -> list of (neighbor, edge_weight)
        self.sdf_node_time = {}         # Node weights: node -> time
        self.cell_widths = {}           # Cell widths: cell -> widths
        self.instance_to_cell_type = {} # Instance to cell type mapping

    def add_node(self, node, weight=0.):
        """Add a node with its weight."""
        self.sdf_node_time[node] = weight

    def add_edge(self, u, v, weight=0.):
        """Add an edge with its weight."""
        self.graph[u].append((v, weight))

    def get_end_nodes(self):
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [node for node in self.sdf_node_time if not self.graph.get(node)]
        return end_nodes

    def topological_sort(self):
        """Perform topological sorting of the DAG."""
        in_degree = defaultdict(int)
        for u in self.graph:
            for v, _ in self.graph[u]:
                in_degree[v] += 1

        queue = deque([node for node in self.sdf_node_time if in_degree[node] == 0])
        top_order = []

        while queue:
            u = queue.popleft()
            top_order.append(u)
            for v, _ in self.graph.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return top_order

    def init_cell_widths(self):
        for instance, celltype in self.instance_to_cell_type.items():
            if celltype not in circuits:
                print("Circuit not found for", celltype)
                continue
            circuit = circuits[celltype]

            cell_widths = [0]*len(circuit["transistors"])
            for transistor in circuit["transistors"]:
                cell_widths[int(transistor["name"])] = transistor["w"]
            self.cell_widths[instance] = cell_widths

    def get_start_nodes(self):
        """Return a list of nodes with no incoming edges."""
        in_degree = defaultdict(int)
        for u in self.graph:
            for v, _ in self.graph[u]:
                in_degree[v] += 1
        start_nodes = [node for node in self.sdf_node_time if in_degree[node] == 0]
        return start_nodes

    def get_end_nodes(self):
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [node for node in self.sdf_node_time if not self.graph.get(node)]
        return end_nodes

    def longest_path(self):
        """Compute the top N longest paths in the DAG, including accumulated times."""
        top_order = self.topological_sort()
        time = {node: 0 for node in self.sdf_node_time}
        parent = {node: None for node in self.sdf_node_time}

        start_nodes = self.get_start_nodes()

        for node in start_nodes:
            time[node] = self.sdf_node_time[node]

        for node in top_order:
            for neighbor, edge_weight in self.graph.get(node, []):
                t = time[neighbor]
                newt = time[node] + edge_weight + self.sdf_node_time[neighbor]
                if newt > t:
                    time[neighbor] = newt
                    parent[neighbor] = node

        argmax_time = max(time.keys(), key=time.get)

        path = []
        node = argmax_time
        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path, time[argmax_time]

    def top_n_longest_paths(self, N):
        """Compute the top N longest paths in the DAG, including accumulated times."""
        top_order = self.topological_sort()
        paths = {node: [] for node in self.sdf_node_time}

        start_nodes = self.get_start_nodes()

        # Initialize paths for start nodes
        for node in start_nodes:
            # For start nodes, the accumulated time is just their node weight
            paths[node].append((self.sdf_node_time[node], [node], [self.sdf_node_time[node]]))

        for node in top_order:
            for neighbor, edge_weight in self.graph.get(node, []):
                new_paths = []
                for weight_u, path_u, times_u in paths[node]:
                    # Calculate new total weight
                    new_total_weight = weight_u + edge_weight + self.sdf_node_time[neighbor]
                    # Create new path and times list
                    new_path = path_u + [neighbor]
                    new_time = times_u + [new_total_weight]
                    new_paths.append((new_total_weight, new_path, new_time))
                # Merge new_paths with existing paths[neighbor] and keep top N
                combined_paths = paths[neighbor] + new_paths
                # Keep top N paths by total_weight
                combined_paths.sort(reverse=True, key=lambda x: x[0])
                paths[neighbor] = combined_paths[:N]

        # Collect paths from end nodes
        end_nodes = self.get_end_nodes()
        all_paths = []
        for node in end_nodes:
            all_paths.extend(paths[node])
        # Keep top N paths overall
        all_paths.sort(reverse=True, key=lambda x: x[0])
        top_N_paths = all_paths[:N]
        return top_N_paths

    def set_instance_to_cell_type(self, instance_to_cell_type):
        self.instance_to_cell_type = instance_to_cell_type

    def save_to_file(self, file_path):
        """Serialize the DAG to a JSON file."""
        # Convert defaultdict to a regular dict for JSON serialization
        graph_dict = {node: neighbors for node, neighbors in self.graph.items()}
        data = {
            'graph': graph_dict,
            'node_weights': self.sdf_node_time,
            'instance_to_cell_type': self.instance_to_cell_type
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
        dag.graph = defaultdict(list, {
            node: [(neighbor, weight) for neighbor, weight in neighbors]
            for node, neighbors in data['graph'].items()
        })
        dag.instance_to_cell_type = data['instance_to_cell_type']
        return dag


def temp():
    with open('hs_saved_instance_to_cell_type.pkl', 'rb') as f:
        instance_to_cell_type = pickle.load(f)

    # opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/hs_picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    with open('hs_saved_nods.pkl', 'rb') as f:
        nods = pickle.load(f)

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


                pin_1 = words[5].split(".")[1]
                pin_2 = words[6].split(".")[1]

                if instance_1 in nod_names and instance_2 in nod_names:
                    for s2 in nods[instance_2]:
                        for s1 in nods[instance_1]:
                            if len(words) == 8:
                                words.append(words[7])
                            if s2[0][pin_2] == "falling" and s1[1][0] == 0:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]), instance_2 + "@" + dict_to_string(s2[0]), float(words[8].split(":")[0]))
                            elif s2[0][pin_2] == "rising" and s1[1][0] == 1:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]), instance_2 + "@" + dict_to_string(s2[0]), float(words[7].split(":")[0]))

                j += 1

    dag.set_instance_to_cell_type(instance_to_cell_type)
    dag.save_to_file("dag_hs.json")

if __name__ == "__main__":
    temp()