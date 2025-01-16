from dag import DAG
import time
import pickle

N = 170
t0 = time.time()

with open('hs_saved_instance_to_cell_type.pkl', 'rb') as f:
    instance_to_cell_type = pickle.load(f)

dag = DAG.load_from_file("dag_hs.json")
dag.init_cell_widths()
print(dag.cell_widths)

path, max_length = dag.longest_path()
t1 = time.time()

for node in path:
    print(instance_to_cell_type[node.split("@")[0]])
    print(node)

print(f"Path length: {max_length}")
print(f"Time taken: {t1-t0} seconds")
