import time
from itertools import product
from generate_gate_function import generate_gate_function
from functools import partial
import re
import pickle
from collections import defaultdict

def sdf_parser():
    #opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/hs_picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    functions = generate_gate_function("../../../libjson_parse/libjson")
    print("generated gate functions")

    nods  = defaultdict(list)

    instance_to_cell_type = {}
    instance_to_cell_type_full = {}

    for i in range(len(sdf_content)):
        line = sdf_content[i]
        if "CELLTYPE" in line and line != '  (CELLTYPE "picorv32")' and line != '  (CELLTYPE "spm")' and line != '  (CELLTYPE "test")':
            cell_short = "_".join(line.split("__")[1].split("_")[0:-1])
            cell_long = "_".join(line.split('"')[1].split("_")[:-1])
            cell_full = line.split('"')[1]
            pins, function, function_str = functions[cell_short]

            if "dfxtp" in cell_short or "dfrtp" in cell_short:
                continue
            instance_to_cell_type[sdf_content[i+1][12:-1]] = cell_long
            instance_to_cell_type_full[sdf_content[i+1][12:-1]] = cell_full

            for j in range(len(pins)):
                current_pin = pins[j]
                other_pins = [pin for pin in pins if pin != current_pin]
                combinations = list(product([0, 1], repeat=len(other_pins)))
                for comb in combinations:
                    gate_val_fall = 0
                    gate_state_fall = ""

                    gate_val_rise = 0
                    gate_state_rise = ""

                    if len(other_pins) == 0:
                        gate_val_fall = function(**{current_pin: 0})
                        gate_state_fall = {current_pin:"fall"}

                        gate_val_rise = function(**{current_pin: 1})
                        gate_state_rise = {current_pin:"rise"}
                    else:
                        pin_val = 0
                        new_func = partial(function, **{current_pin: pin_val})
                        gate_val_fall = new_func(*comb)
                        #gate_state_fall = ",".join([pins[k] + "=" + str(comb[k]) if k<j else pins[k] + "=" + "fall" if k == j else pins[k] + "=" + str(comb[k-1]) for k in range(len(pins))])
                        gate_state_fall = {pins[k]: comb[k] if k<j else "fall" if k==j else comb[k-1] for k in range(len(pins))}

                        pin_val = 1
                        new_func = partial(function, **{current_pin: pin_val})
                        gate_val_rise = new_func(*comb)
                        #gate_state_rise = ",".join([pins[k] + "=" + str(comb[k]) if k<j else pins[k] + "=" + "rise" if k == j else pins[k] + "=" + str(comb[k-1]) for k in range(len(pins))])
                        gate_state_rise = {pins[k]: comb[k] if k < j else "rise" if k == j else comb[k - 1] for k in range(len(pins))}

                    if gate_val_fall != gate_val_rise:
                        line_index = 0
                        while "IOPATH" in sdf_content[i+4+line_index] or "COND" in sdf_content[i+4+line_index]:
                            line_index += 1

                        fall_output_max_t = 0
                        rise_output_max_t = 0


                        for k in range(line_index):
                            if "COND" in sdf_content[i+4+k]:
                                continue
                            if sdf_content[i+4+k].strip().split(" ")[1] == current_pin:
                                s = sdf_content[i+4+k]

                                triplet_pattern = r'\(\s*([\d.]+):[\d.]+:[\d.]+\s*\)'
                                triplet_match = re.search(triplet_pattern, s)

                                pos_after_triplet = triplet_match.end()
                                number_pattern = r'[\d.]+'
                                number_match = re.search(number_pattern, s[pos_after_triplet:])

                                rise_output_max_t = max(rise_output_max_t, float(triplet_match.group(1)))
                                fall_output_max_t = max(fall_output_max_t, float(number_match.group(0)))

                        if gate_val_fall:
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_fall, [1, rise_output_max_t]])
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_rise, [0, fall_output_max_t]])
                        else:
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_rise, [1, rise_output_max_t]])
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_fall, [0, fall_output_max_t]])
                    # else:
                    #     nods[sdf_content[i + 1][12:-1]].append([gate_state_fall, [gate_val_fall, 0]])
                    #     nods[sdf_content[i + 1][12:-1]].append([gate_state_rise, [gate_val_rise, 0]])




    print(len(nods))

    with open('hs_saved_nods.pkl', 'wb') as f:
        pickle.dump(nods, f)

    with open('hs_saved_instance_to_cell_type.pkl', 'wb') as f:
        pickle.dump(instance_to_cell_type, f)

    with open('hs_saved_instance_to_cell_type_full.pkl', 'wb') as f:
        pickle.dump(instance_to_cell_type_full, f)

sdf_parser()