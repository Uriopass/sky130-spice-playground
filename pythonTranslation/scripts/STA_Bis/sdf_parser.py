import time
from itertools import product
from generate_gate_function import generate_gate_function
from functools import partial
import re
import pickle
from collections import defaultdict

def sdf_parser():
    #opens the sdf file and reads the content
    sdf_data_path = "../../libs/sdf/picorv32__nom_tt_025C_1v80.sdf"
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    sdf_content = sdf_content.split("\n")

    functions = generate_gate_function("../../../libjson_parse/libjson")

    nods  = defaultdict(list)
    for i in range(len(sdf_content)):
        line = sdf_content[i]
        if "CELLTYPE" in line and line != '  (CELLTYPE "picorv32")' and line != '  (CELLTYPE "spm")':
            cell_short = "_".join(line.split("__")[1].split("_")[0:-1])
            pins, function, function_str = functions[cell_short]

            for j in range(len(pins)):
                current_pin = pins[j]
                other_pins = [pin for pin in pins if pin != current_pin]
                combinations = list(product([0, 1], repeat=len(other_pins)))
                for comb in combinations:
                    gate_val_falling = 0
                    gate_state_falling = ""

                    gate_val_rising = 0
                    gate_state_rising = ""

                    if len(other_pins) == 0:
                        gate_val_falling = function(**{current_pin: 0})
                        gate_state_falling = {current_pin:"falling"}

                        gate_val_rising = function(**{current_pin: 1})
                        gate_state_rising = {current_pin:"rising"}
                    else:
                        pin_val = 0
                        new_func = partial(function, **{current_pin: pin_val})
                        gate_val_falling = new_func(*comb)
                        #gate_state_falling = ",".join([pins[k] + "=" + str(comb[k]) if k<j else pins[k] + "=" + "falling" if k == j else pins[k] + "=" + str(comb[k-1]) for k in range(len(pins))])
                        gate_state_falling = {pins[k]: comb[k] if k<j else "falling" if k==j else comb[k-1] for k in range(len(pins))}

                        pin_val = 1
                        new_func = partial(function, **{current_pin: pin_val})
                        gate_val_rising = new_func(*comb)
                        #gate_state_rising = ",".join([pins[k] + "=" + str(comb[k]) if k<j else pins[k] + "=" + "rising" if k == j else pins[k] + "=" + str(comb[k-1]) for k in range(len(pins))])
                        gate_state_rising = {pins[k]: comb[k] if k < j else "rising" if k == j else comb[k - 1] for k in range(len(pins))}

                    if gate_val_falling != gate_val_rising:
                        line_index = 0
                        while "IOPATH" in sdf_content[i+4+line_index]:
                            line_index += 1

                        falling_output_max_t = 0
                        rising_output_max_t = 0


                        for k in range(line_index):
                            if sdf_content[i+4+k].split(" ")[5] == current_pin:
                                s = sdf_content[i+4+k]

                                triplet_pattern = r'\(\s*([\d.]+):[\d.]+:[\d.]+\s*\)'
                                triplet_match = re.search(triplet_pattern, s)

                                pos_after_triplet = triplet_match.end()
                                number_pattern = r'[\d.]+'
                                number_match = re.search(number_pattern, s[pos_after_triplet:])

                                rising_output_max_t = max(rising_output_max_t, float(triplet_match.group(1)))
                                falling_output_max_t = max(falling_output_max_t, float(number_match.group(0)))

                        if gate_val_falling:
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_falling, [1, rising_output_max_t]])
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_rising, [0, falling_output_max_t]])
                        else:
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_rising, [1, rising_output_max_t]])
                            nods[sdf_content[i + 1][12:-1]].append(
                                [gate_state_falling, [0, falling_output_max_t]])
                    # else:
                    #     nods[sdf_content[i + 1][12:-1]].append([gate_state_falling, [gate_val_falling, 0]])
                    #     nods[sdf_content[i + 1][12:-1]].append([gate_state_rising, [gate_val_rising, 0]])





    with open('saved_nods.pkl', 'wb') as f:
        pickle.dump(nods, f)


sdf_parser()