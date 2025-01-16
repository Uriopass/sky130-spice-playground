from dag import DAG
import time
import pickle

N = 170
t0 = time.time()

with open('hs_saved_instance_to_cell_type.pkl', 'rb') as f:
    instance_to_cell_type = pickle.load(f)

N_paths = DAG.load_from_file("dag.json").top_n_longest_paths(N)
t1 = time.time()

path, times = N_paths[N-1][1], N_paths[N-1][2]
max_length = times[-1]
for i in range(len(path)):
    node = path[i]
    if node[0] == "_":
        print(instance_to_cell_type[node.split("__")[0] + "_"])
    else:
        print(instance_to_cell_type[node.split("_")[0]])
    print(node)

    print(times[i], "\n")


print(f"Path length: {max_length}")
print(f"Time taken: {t1-t0} seconds")
print(N_paths[0][2])