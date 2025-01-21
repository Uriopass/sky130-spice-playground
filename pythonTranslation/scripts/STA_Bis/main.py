from dag import DAG
import time
import pickle

N = 170
t0 = time.time()

with open('hs_saved_instance_to_cell_type.pkl', 'rb') as f:
    instance_to_cell_type = pickle.load(f)

dag = DAG.load_from_file("dag_hs.json")

path, max_length = dag.longest_path_linear_sta(groundtruth=True)
#path, max_length = dag.longest_path()
t1 = time.time()

for node, time in path:
    print(instance_to_cell_type[node.split("@")[0]], node, time)

print(f"Path length: {max_length}")
print(f"Time taken: {t1-t0} seconds")
