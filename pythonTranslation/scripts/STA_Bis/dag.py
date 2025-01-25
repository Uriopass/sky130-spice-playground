import json
import os.path
import pickle
import time
from collections import defaultdict, deque
import re
import multiprocessing as mp

import numpy as np
import netCDF4 as nc
from tqdm import tqdm

from spice import run_spice_timing

pin_combinations = json.load(open("../../../libjson_parse/cells_transition_combinations.json"))
pin_combinations["sky130_fd_sc_hs__bufbuf_1"] = pin_combinations["sky130_fd_sc_hs__bufbuf_8"]
pin_combinations["sky130_fd_sc_hs__bufinv_1"] = pin_combinations["sky130_fd_sc_hs__bufinv_8"]
pin_combinations["sky130_fd_sc_hs__clkinv_0"] = pin_combinations["sky130_fd_sc_hs__clkinv_1"]

alpha = 50
DEFAULT_CAPA = 2.0

def LSE(l):
    m = np.max(l)
    e = np.exp(alpha * (l - m))
    return m + 1 / alpha * np.log(np.sum(e))


def LSE_with_deriv(l):
    m = np.max(l)
    e = np.exp(alpha * (l - m))
    s = np.sum(e)
    return m + 1 / alpha * np.log(s), e / np.sum(e)


def LSE_deriv(l):
    m = np.max(l)
    e = np.exp(alpha * (l - m))
    return e / np.sum(e)


def parallel_work(l, f, num_workers=1):
    if num_workers == 1:
        return [f(v) for v in l]

    results = [None] * len(l)

    input_queue = mp.Queue(len(l))
    output_queue = mp.Queue(len(l))

    def f_worker(input_queue, output_queue):
        for i, v in iter(input_queue.get, None):
            result = f(v)
            output_queue.put((i, result))


    processes = [mp.Process(target=f_worker, args=(input_queue, output_queue)) for _ in range(num_workers)]
    for p in processes:
        p.start()

    for i, v in enumerate(l):
        input_queue.put((i, v))
    for _ in range(num_workers):
        input_queue.put(None)

    for _ in tqdm(range(len(l))):
        i, result = output_queue.get()
        results[i] = result

    for p in processes:
        p.join()

    return results


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

            subcircuits[current_subckt] = {"name": current_subckt, "input_pins": input_pins, "output_pin": output_pin,
                                           "transistors": []}
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
                    # print("duplicate in", current_subckt)
                    break
                if transistor["source"] == drain and transistor["gate"] == gate and transistor["drain"] == source:
                    # print("duplicate in", current_subckt)
                    break

            if source == circuit["output_pin"] or drain == circuit["output_pin"]:
                circuit["output_transistors"].append(t1)

    for key in list(subcircuits.keys()):
        circuit_name_without_size = "_".join(key.split("_")[:-1])
        smallest_size = smallest_sizes[circuit_name_without_size]
        subcircuits[circuit_name_without_size] = subcircuits[circuit_name_without_size + "_" + str(smallest_size)]

    return subcircuits


def parse_linear_estimators(all_celltypes):
    linear_estimators = {}
    if os.name == 'nt':
        print("CDF files cannot be read on windows for some reason wtf, please run on linux")
        exit(0)
    for celltype in all_celltypes:
        with nc.Dataset(f"../../../slx/models/{celltype}.nc", "r") as f:
            for pin_state, case in f.groups.items():
                linear_estimator = case.variables["linear_estimator"][:, :]
                linear_estimator_capa = case.variables["linear_estimator_capa"][:, :]

                linear_estimators[f"{celltype}@{pin_state}"] = (
                    np.array(linear_estimator, dtype=np.float64), linear_estimator_capa)
    return linear_estimators


circuits = parse_netlist(open("../../../slx/hs_nopex.spice").read())
MINSIZE = 0.36

import mk_vector


class DAG:
    def __init__(self):
        self.rev_graph = defaultdict(list)  # Adjacency list: node -> list of (neighbor, edge_weight)
        self.graph = defaultdict(list)  # Adjacency list: node -> list of (neighbor, edge_weight)
        self.sdf_node_time = {}  # Node weights: node -> time
        self.instance_to_cell_type = {}  # Instance to cell type mapping
        self.instance_to_cell_type_full = {}  # Instance to full cell type mapping

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
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [parent for parent, childs in self.graph.items() if len(childs) == 0]
        return end_nodes

    def get_start_nodes(self):
        """Return a list of nodes with no incoming edges."""
        start_nodes = [child for child, parents in self.rev_graph.items() if len(parents) == 0]
        return start_nodes

    def longest_path_linear_sta(self, groundtruth=False):
        print(len(self.graph), len(self.rev_graph))
        node_idx = {node: i for i, node in enumerate(self.rev_graph)}
        instance_idx = {instance: i for i, instance in enumerate(self.instance_to_cell_type)}
        node_idx_to_node = {i: node for i, node in enumerate(self.rev_graph)}

        # region cell widths
        cell_widths = [None] * len(self.instance_to_cell_type)
        all_celltypes = set()

        instance_to_celltype_idx = [""] * len(self.instance_to_cell_type)
        node_to_pin_state_idx = [""] * len(self.graph)

        for instance, celltype in self.instance_to_cell_type.items():
            if celltype not in circuits:
                print("Circuit not found for", celltype)
                continue
            circuit = circuits[celltype]

            w = np.zeros(len(circuit["transistors"]), dtype=np.float64)
            for transistor in circuit["transistors"]:
                w[int(transistor["name"])] = transistor["w"]

            size = min(4, max(1, int(self.instance_to_cell_type_full[instance].split("_")[-1])))
            for transistor in circuit["output_transistors"]:
                w[int(transistor["name"])] *= size

            cell_widths[instance_idx[instance]] = w
            instance_to_celltype_idx[instance_idx[instance]] = celltype
            all_celltypes.add(celltype)
        # endregion
        print("sum cell widths", sum(np.sum(v) for v in cell_widths))

        cell_widths = pickle.load(open('hs_saved_cell_widths.pkl', 'rb'))

        print("created cell widths")

        # region linear_estimator
        linear_estimators = parse_linear_estimators(all_celltypes)

        linear_estimator_node = [None] * len(self.graph)
        capa_estimator_node = [None] * len(self.graph)

        for node in self.graph:
            instance, pin_state = node.split("@")
            celltype = self.instance_to_cell_type[instance]
            node_to_pin_state_idx[node_idx[node]] = pin_state
            linear_estimator_node[node_idx[node]] = linear_estimators[f"{celltype}@{pin_state}"][0]
            capa_estimator_node[node_idx[node]] = linear_estimators[f"{celltype}@{pin_state}"][1]
        print("parsed needed linear estimators")
        # endregion

        rev_graph_idx = [[]] * len(self.graph)
        for node, neighbors in self.rev_graph.items():
            rev_graph_idx[node_idx[node]] = [(node_idx[neighbor], weight) for neighbor, weight in neighbors]

        graph_idx = [[]] * len(self.graph)
        for node, neighbors in self.graph.items():
            graph_idx[node_idx[node]] = [(node_idx[neighbor], weight) for neighbor, weight in neighbors]

        node_to_instance = np.zeros(len(self.graph), dtype=np.uint32)
        for node in self.graph:
            instance, _ = node.split("@")
            node_to_instance[node_idx[node]] = instance_idx[instance]

        maxdepth, nodes_by_depths = self.depth_chunks(node_idx)

        is_falling_node = [False] * len(self.graph)
        for node in self.graph:
            instance, pin_state = node.split("@")
            if "fall" in pin_state:
                is_falling_node[node_idx[node]] = True

        end_nodes = np.array(list(node_idx[node] for node in self.get_end_nodes()), dtype=np.uint32)
        start_nodes = np.array(list(node_idx[node] for node in self.get_start_nodes()), dtype=np.uint32)
        print(f"got {len(start_nodes)} start nodes")

        def process_node(child):
            instance = node_to_instance[child]
            linear_estimator = linear_estimator_node[child]

            parents = [v[0] for v in rev_graph_idx[child]]

            parent = None
            t_parent = 0
            if len(parents) == 0:
                is_falling = is_falling_node[child]

                slew_in = 0.1
                if is_falling:
                    slew_in = 0.06
            else:
                time_parents = time_slew[parents, 0]

                t_parent, deriv = LSE_with_deriv(time_parents)
                slew_in = np.dot(deriv, time_slew[parents, 1])
                parent = parents[np.argmax(time_parents)]

            if groundtruth:
                celltype = instance_to_celltype_idx[instance]
                subckt = circuits[celltype]
                pin_state = node_to_pin_state_idx[child]
                dt, slew = run_spice_timing(subckt, pin_state, cell_widths[instance], node_out_capa[child], slew_in)
            else:
                v = mk_vector.mk_vector(cell_widths[instance], node_out_capa[child], slew_in)
                dtslew = np.dot(v, linear_estimator)
                dt, slew = dtslew[0], dtslew[1]

            return t_parent + dt, slew, slew_in, parent

        first_time = 0

        node_filter = np.ones(len(self.graph), dtype=np.bool_)

        for iter in range(1000000):
            node_out_capa = self.node_capa(capa_estimator_node, cell_widths, node_to_instance, rev_graph_idx, graph_idx, node_filter)

            time_slew = np.zeros((len(self.graph), 3), dtype=np.float64)

            for depth, nodes in enumerate(nodes_by_depths):
                nodes = np.array(nodes, dtype=np.uint32)
                nodes = nodes[node_filter[nodes]]

                results = parallel_work(nodes, process_node)
                for node, result in zip(nodes, results):
                    time_slew[node, 0] = result[0]
                    time_slew[node, 1] = result[1]
                    time_slew[node, 2] = result[2]

            node_gradient = np.zeros(len(self.graph))

            end_w = LSE_deriv(time_slew[end_nodes, 0])
            node_gradient[end_nodes] = end_w

            for depth in range(maxdepth - 1, -1, -1):
                nodes = nodes_by_depths[depth]
                for child in nodes:
                    if not node_filter[child]:
                        continue
                    t_parents = []
                    parent_idx = []
                    for parent, edge_weight in rev_graph_idx[child]:
                        parent_idx.append(parent)
                        t_parent = time_slew[parent, 0]
                        t_parents.append(t_parent + edge_weight)
                    if len(t_parents) == 0:
                        continue
                    weights = LSE_deriv(np.array(t_parents))
                    node_gradient[np.array(parent_idx, dtype=np.uint32)] += node_gradient[child] * weights

            if iter % 20 == 0:
                # pickle the cell widths
                with open('hs_saved_cell_widths.pkl', 'wb') as f:
                    pickle.dump(cell_widths, f)

                node_out_capa = self.node_capa(capa_estimator_node, cell_widths, node_to_instance, rev_graph_idx, graph_idx, None)

                time_slew = np.zeros((len(self.graph), 3), dtype=np.float64)

                for depth, nodes in enumerate(nodes_by_depths):
                    results = parallel_work(nodes, process_node)
                    for node, result in zip(nodes, results):
                        time_slew[node, 0] = result[0]
                        time_slew[node, 1] = result[1]
                        time_slew[node, 2] = result[2]

                node_gradient = np.zeros(len(self.graph))

                end_w = LSE_deriv(time_slew[end_nodes, 0])
                node_gradient[end_nodes] = end_w

                for depth in range(maxdepth - 1, -1, -1):
                    nodes = nodes_by_depths[depth]
                    for child in nodes:
                        t_parents = []
                        parent_idx = []
                        for parent, edge_weight in rev_graph_idx[child]:
                            parent_idx.append(parent)
                            t_parent = time_slew[parent, 0]
                            t_parents.append(t_parent + edge_weight)
                        if len(t_parents) == 0:
                            continue
                        weights = LSE_deriv(np.array(t_parents))
                        node_gradient[np.array(parent_idx, dtype=np.uint32)] += node_gradient[child] * weights

                node_filter = node_gradient > 1e-5

            dws = [[]] * len(rev_graph_idx)
            dcapas = [0.0] * len(rev_graph_idx)

            for node in range(len(rev_graph_idx)):
                if not node_filter[node]:
                    continue
                w = cell_widths[node_to_instance[node]]
                capa = node_out_capa[node]
                slew_in = time_slew[node, 2]
                linear_estimator = linear_estimator_node[node]

                dt_grad = node_gradient[node]
                dv = linear_estimator[:, 0] * dt_grad

                dw, dcapa = mk_vector.vector_grad(w, capa, slew_in, dv)

                dws[node] = dw
                dcapas[node] = dcapa


            for node in start_nodes:
                if not node_filter[node]:
                    continue
                dws[node] += 0.01 * capa_estimator_node[node].flatten()

            dws_instance = [np.zeros(0)] * len(self.instance_to_cell_type)

            node_seen_instance = defaultdict(set)

            for node in range(len(rev_graph_idx)):
                dcapa = dcapas[node]

                for child, _ in graph_idx[node]:
                    if not node_filter[child]:
                        continue
                    instance = node_to_instance[child]

                    if instance not in node_seen_instance[node]:
                        node_seen_instance[node].add(instance)
                    else:
                        continue
                    capa_estimator = capa_estimator_node[child]

                    dw_capa = dcapa * capa_estimator
                    dws[child] += dw_capa.flatten()

                if not node_filter[node]:
                    continue
                instance = node_to_instance[node]
                if dws_instance[instance].size == 0:
                    dws_instance[instance] = dws[node]
                else:
                    dws_instance[instance] += dws[node]


            #print("dws_instance", *dws_instance)

            if iter % 20 == 0:
                predicted_time = time_slew[end_nodes, 0]
                maxtime = np.round(np.max(predicted_time), 5)
                if first_time == 0:
                    first_time = maxtime
                print(iter, first_time, maxtime, first_time / maxtime)

            if False and iter % 1 == 0:
                #predicted_all = time_slew[:, 0]
                groundtruth = True
                time_slew = np.zeros((len(self.graph), 3), dtype=np.float64)
                path_parent = [None] * len(self.graph)
                for depth, nodes in enumerate(nodes_by_depths):
                    results = parallel_work(nodes, process_node, 20)
                    for node, result in zip(nodes, results):
                        time_slew[node, 0] = result[0]
                        time_slew[node, 1] = result[1]
                        time_slew[node, 2] = result[2]
                        path_parent[node] = result[3]
                groundtruth = False
                print("GT", np.max(time_slew[:, 0]))


            for instance, dw in enumerate(dws_instance):
                if len(dw) == 0:
                    continue
                cell_widths[instance] = np.clip(cell_widths[instance] - dw , 0.36, 30.0)
                # print(cell_widths[instance], dw)
            # argmax_time = max(end_nodes, key=lambda x: time_slew[x][0])
            # print(time_slew[argmax_time][0])

        time_slew = np.zeros((len(self.graph), 3), dtype=np.float64)
        path_parent = [None] * len(self.graph)

        for depth, nodes in enumerate(nodes_by_depths):
            results = parallel_work(nodes, process_node)
            for node, result in zip(nodes, results):
                time_slew[node][0] = result[0]
                time_slew[node][1] = result[1]
                time_slew[node][2] = result[2]
                path_parent[node] = result[3]

        argmax_time = max(end_nodes, key=lambda x: time_slew[x][0])

        path = []
        node = argmax_time
        critical_grad = []
        while node is not None:
            critical_grad.append(node_gradient[node])
            path.append((node_idx_to_node[node], time_slew[node][0]))
            node = path_parent[node]
        path.reverse()

        return path, time_slew[argmax_time][0]

    def node_capa(self, capa_estimator_node, cell_widths, node_to_instance, rev_graph_idx, graph_idx, node_filter):
        node_out_capa = np.zeros(len(rev_graph_idx))

        if node_filter is None:
            node_seen_instance = defaultdict(set)
            for child in range(len(rev_graph_idx)):
                instance = node_to_instance[child]

                capa_estimator = capa_estimator_node[child]

                capa = (np.array(cell_widths[instance]) @ capa_estimator)[0]
                for parent, _ in rev_graph_idx[child]:
                    if instance not in node_seen_instance[parent]:
                        node_seen_instance[parent].add(instance)
                        node_out_capa[parent] += capa
        else:
            node_seen_instance = set()
            for parent in range(len(graph_idx)):
                if not node_filter[parent]:
                    continue

                node_seen_instance.clear()
                tot_capa = 0.0
                for child, _ in graph_idx[parent]:
                    instance = node_to_instance[child]

                    if instance not in node_seen_instance:
                        node_seen_instance.add(instance)

                        capa_estimator = capa_estimator_node[child]
                        capa = (np.array(cell_widths[instance]) @ capa_estimator)[0]

                        tot_capa += capa
                node_out_capa[parent] = tot_capa

        node_out_capa = np.where(node_out_capa == 0, DEFAULT_CAPA, node_out_capa)
        return node_out_capa

    def depth_chunks(self, node_idx):
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
            maxdepth += 1
            if len(next_nodes) == 0:
                break
            cur_nodes = list(next_nodes)
            next_nodes = set()
        nodes_by_depths = [[] for _ in range(maxdepth)]
        for node, depth in node_depth.items():
            nodes_by_depths[depth].append(node_idx[node])
        return maxdepth, nodes_by_depths

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
            if node not in graph_dict:
                graph_dict[node] = []
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


def gen_dag():
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

    for instance in nods:
        for s in nods[instance]:
            dag.add_node(instance + "@" + dict_to_string(s[0]), float(s[1][1]))

    for i in range(len(sdf_content)):
        line = sdf_content[i]
        if line == '  (CELLTYPE "picorv32")' or line == '  (CELLTYPE "spm")' or line == '  (CELLTYPE "test")':
            j = i + 4
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

                if "dfxtp" in instance_to_cell_type[instance_1] or "dfxtp" in instance_to_cell_type[
                    instance_2] or "dfrtp" in instance_to_cell_type[instance_1] or "dfrtp" in instance_to_cell_type[
                    instance_2]:
                    j += 1
                    continue

                # if "_07331_" in instance_1 or "_07331_" in instance_2 or "_07892_" in instance_1 or "_07892_" in instance_2:
                #    j += 1
                #    continue

                # pin_1 = words[5].split(".")[1]
                pin_2 = words[6].split(".")[1]

                if instance_1 in nod_names and instance_2 in nod_names:
                    for s2 in nods[instance_2]:
                        for s1 in nods[instance_1]:
                            if len(words) == 8:
                                words.append(words[7])
                            if s2[0][pin_2] == "fall" and s1[1][0] == 0:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]),
                                             instance_2 + "@" + dict_to_string(s2[0]), float(words[8].split(":")[0]))
                            elif s2[0][pin_2] == "rise" and s1[1][0] == 1:
                                dag.add_node(instance_1 + "@" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "@" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "@" + dict_to_string(s1[0]),
                                             instance_2 + "@" + dict_to_string(s2[0]), float(words[7].split(":")[0]))

                j += 1
    print("prepared the dag")
    dag.set_instance_to_cell_type(instance_to_cell_type)
    dag.set_instance_to_cell_type_full(instance_to_cell_type_full)
    dag.remove_delay_gates()
    dag.save_to_file("dag_hs.json")


if __name__ == "__main__":
    gen_dag()
