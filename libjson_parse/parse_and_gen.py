import os
import json
import itertools

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

    for cell, lib in cells.items():
        print(cell)
        if type (lib) is not dict:
            continue
        for lib_outpin in lib.values():
            if type(lib_outpin) is not dict:
                continue
            if not "direction" in lib_outpin:
                continue
            if not lib_outpin["direction"] == "output":
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

    with open("cells_transition_combinations.json", "w") as f:
        f.write(json.dumps(cells_transition_combinations, indent=4))