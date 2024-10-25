import os
import json
import itertools
from collections import defaultdict


def calc_transition(function_str, pins, pin_in, comb_other_pins):
    pin_before = False
    pin_after = True

    evalbefore = ""
    evalafter = ""
    i = 0
    for pin in pins:
        if pin == pin_in:
            evalbefore += f"{pin} = {pin_before}\n"
            evalafter += f"{pin} = {pin_after}\n"
        else:
            evalbefore += f"{pin} = {comb_other_pins[i]}\n"
            evalafter += f"{pin} = {comb_other_pins[i]}\n"
            i += 1

    exec(evalbefore)

    function_str = function_str.replace("!", "~")

    value_before = eval(function_str)%2

    exec(evalafter)
    value_after = eval(function_str)%2

    return value_before, value_after

if __name__ == "__main__":
    cells = {}

    for file in os.listdir("libjson"):
        with open(f"libjson/{file}") as f:
            cell_name = file.split(".json")[0]
            cells[cell_name] = json.loads(f.read())

    cells_transition_combinations = {}
    unateness = defaultdict(dict)

    for cell, lib in cells.items():
        if type (lib) is not dict:
            continue
        for lib_outpin in lib.values():
            if type(lib_outpin) is not dict:
                continue
            if not "direction" in lib_outpin:
                continue
            if not lib_outpin["direction"] == "output":
                continue
            if not "timing" in lib_outpin:
                continue

            timings = lib_outpin["timing"]
            if type(timings) == dict:
                timings = [timings]

            pins = set()
            for timing in timings:
                pins.add(timing["related_pin"])

            pins = list(pins)

            out_cell = {}
            for pin_in in pins:
                if "function" not in lib_outpin or lib_outpin["function"] == "IQ" or lib_outpin["function"] == "IQ_N":
                    out_cell[pin_in] = [
                        {
                            "pins": {},
                            "unate": "positive"
                        }
                    ]
                    continue
                if len(pins) == 1:
                    before, after = calc_transition(lib_outpin["function"], pins, pin_in, [])
                    if before != after:
                        out_cell[pin_in] = [
                            {
                                "pins": {},
                                "unate": "positive" if before == 0 else "negative"
                            }
                        ]
                        continue
                    else:
                        print(f"weird, {cell} {pin_in} has no transition")
                        continue

                combs = []
                for combinations in itertools.product([True, False], repeat=len(pins)-1):
                    before, after = calc_transition(lib_outpin["function"], pins, pin_in, combinations)
                    if before != after:
                        pins_without_in = list(pin for pin in pins if pin != pin_in)
                        pins_values = dict(zip(pins_without_in, combinations))

                        combs.append({
                            "pins": pins_values,
                            "unate": "positive" if before == 0 else "negative"
                        })
                out_cell[pin_in] = combs
            cells_transition_combinations[cell] = out_cell

    for cell, pin_combs in cells_transition_combinations.items():
        shortcell = "_".join(cell.split("__")[1].split("_")[0:-1])
        for pin, combs in pin_combs.items():
            positive_unate = False
            negative_unate = False

            for comb in combs:
                if comb["unate"] == "positive":
                    positive_unate = True
                if comb["unate"] == "negative":
                    negative_unate = True

            if positive_unate and negative_unate:
                unateness[shortcell][pin] = "non_unate"
            elif positive_unate:
                unateness[shortcell][pin] = "positive_unate"
            elif negative_unate:
                unateness[shortcell][pin] = "negative_unate"
            else:
                print(f"weird, {shortcell} {pin} has no unate")

    with open('unateness.json', 'w') as f:
        f.write(json.dumps(unateness, indent=4))

    with open("cells_transition_combinations.json", "w") as f:
        f.write(json.dumps(cells_transition_combinations, indent=4))