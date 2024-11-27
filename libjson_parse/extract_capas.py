import os
import json

if __name__ == "__main__":
    cells = {}

    for file in os.listdir("libjson"):
        with open(f"libjson/{file}") as f:
            cell_name = file.split(".json")[0]
            cells[cell_name] = json.loads(f.read())

    pin_capas = {}

    for cell, lib in cells.items():
        if type (lib) is not dict:
            continue
        for pin_name, lib_outpin in lib.items():
            if type(lib_outpin) is not dict:
                continue
            if not "capacitance" in lib_outpin:
                continue
            pin_name = pin_name.split(",")[-1]

            pin_capas[f"{cell}/{pin_name}"] = lib_outpin["capacitance"]

    with open('pin_capa.json', 'w') as f:
        f.write(json.dumps(pin_capas, indent=4))