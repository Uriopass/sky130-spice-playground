import json
import pickle
from collections import defaultdict, deque

def dict_to_string(d):
    s = ""
    for k, v in d.items():
        s += f"{k}={v},"
    return s[:-1]

# Step 1: Represent the DAG with node weights
class DAG:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list: node -> list of (neighbor, edge_weight)
        self.node_weights = {}          # Node weights: node -> weight

    def add_node(self, node, weight=0.):
        """Add a node with its weight."""
        self.node_weights[node] = weight

    def add_edge(self, u, v, weight=0.):
        """Add an edge with its weight."""
        self.graph[u].append((v, weight))

    def get_end_nodes(self):
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [node for node in self.node_weights if not self.graph.get(node)]
        return end_nodes

    def topological_sort(self):
        """Perform topological sorting of the DAG."""
        in_degree = defaultdict(int)
        for u in self.graph:
            for v, _ in self.graph[u]:
                in_degree[v] += 1

        queue = deque([node for node in self.node_weights if in_degree[node] == 0])
        top_order = []

        while queue:
            u = queue.popleft()
            top_order.append(u)
            for v, _ in self.graph.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return top_order

    def get_start_nodes(self):
        """Return a list of nodes with no incoming edges."""
        in_degree = defaultdict(int)
        for u in self.graph:
            for v, _ in self.graph[u]:
                in_degree[v] += 1
        start_nodes = [node for node in self.node_weights if in_degree[node] == 0]
        return start_nodes

    def get_end_nodes(self):
        """Return a list of nodes with no outgoing edges."""
        end_nodes = [node for node in self.node_weights if not self.graph.get(node)]
        return end_nodes

    def top_n_longest_paths(self, N):
        """Compute the top N longest paths in the DAG, including accumulated times."""
        top_order = self.topological_sort()
        paths = {node: [] for node in self.node_weights}

        start_nodes = self.get_start_nodes()

        # Initialize paths for start nodes
        for node in start_nodes:
            # For start nodes, the accumulated time is just their node weight
            paths[node].append((self.node_weights[node], [node], [self.node_weights[node]]))

        for node in top_order:
            for neighbor, edge_weight in self.graph.get(node, []):
                new_paths = []
                for weight_u, path_u, times_u in paths[node]:
                    # Calculate new total weight
                    new_total_weight = weight_u + edge_weight + self.node_weights[neighbor]
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

    def save_to_file(self, file_path):
        """Serialize the DAG to a JSON file."""
        # Convert defaultdict to a regular dict for JSON serialization
        graph_dict = {node: neighbors for node, neighbors in self.graph.items()}
        data = {
            'graph': graph_dict,
            'node_weights': self.node_weights
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load_from_file(cls, file_path):
        """Deserialize the DAG from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        dag = cls()
        dag.node_weights = data['node_weights']
        dag.graph = defaultdict(list, {
            node: [(neighbor, weight) for neighbor, weight in neighbors]
            for node, neighbors in data['graph'].items()
        })
        return dag

def map_instance_to_cell_type():
    # opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    instance_to_cell = {}
    for i in range(len(sdf_content)):
        line = sdf_content[i]
        if "CELLTYPE" in line and line != '  (CELLTYPE "picorv32")' and line != '  (CELLTYPE "spm")':
            cell_short = "_".join(line.split("__")[1].split("_")[0:-1])
            instance_to_cell[sdf_content[i+1][12:-1]] = cell_short

    return instance_to_cell

def temp():
    instance_to_cell_type = map_instance_to_cell_type()
    # opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    with open('saved_nods.pkl', 'rb') as f:
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
                if instance_1 not in instance_to_cell_type.keys() or instance_2 not in instance_to_cell_type.keys() or "dfxtp" in instance_to_cell_type[instance_1] or "dfxtp" in instance_to_cell_type[instance_2] or "dfrtp" in instance_to_cell_type[instance_1] or "dfrtp" in instance_to_cell_type[instance_2]:
                    j += 1
                    continue


                pin_1 = words[5].split(".")[1]
                pin_2 = words[6].split(".")[1]


                if instance_1 in nod_names and instance_2 in nod_names:
                    for s2 in nods[instance_2]:
                        for s1 in nods[instance_1]:
                            if s2[0][pin_2] == "falling" and s1[1][0] == 0:
                                dag.add_node(instance_1 + "_" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "_" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "_" + dict_to_string(s1[0]), instance_2 + "_" + dict_to_string(s2[0]), float(words[8].split(":")[0]))
                            elif s2[0][pin_2] == "rising" and s1[1][0] == 1:
                                dag.add_node(instance_1 + "_" + dict_to_string(s1[0]), float(s1[1][1]))
                                dag.add_node(instance_2 + "_" + dict_to_string(s2[0]), float(s2[1][1]))
                                dag.add_edge(instance_1 + "_" + dict_to_string(s1[0]), instance_2 + "_" + dict_to_string(s2[0]), float(words[7].split(":")[0]))

                j += 1

    dag.save_to_file("dag.json")

if __name__ == "__main__":
    temp()