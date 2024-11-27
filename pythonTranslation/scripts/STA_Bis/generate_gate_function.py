import json
import os

def generate_gate_function(libjson_path):
    cells = {}
    for file in os.listdir(libjson_path):
        with open(f"{libjson_path}/{file}") as f:
            cell_name = file.split(".json")[0]
            cells[cell_name] = json.loads(f.read())

    functions = {}
    for cell, lib in cells.items():
        cell_short = "_".join(cell.split("__")[1].split("_")[0:-1])
        for lib_outpin in lib.values():
            if type(lib_outpin) is not dict or "function" not in lib_outpin or lib_outpin["function"] == "IQ_N" or "timing" not in lib_outpin:
                continue
            else:
                function_str = lib_outpin["function"]
                function_str = function_str.replace("!", "~")


                timings = lib_outpin["timing"]
                if type(timings) == dict:
                    timings = [timings]

                pins = set()
                for timing in timings:
                    pins.add(timing["related_pin"])

                pins = list(pins)

                if lib_outpin["function"] == "IQ":
                    function_str = f"{pins[0]}"

                def f(logic_str, arg_names):
                    def func(*args, **kwargs):
                        variables = kwargs.copy()
                        arg_iter = iter(args)
                        for name in arg_names:
                            if name not in variables:
                                    variables[name] = next(arg_iter)
                        return eval(logic_str, {}, variables) % 2
                    return func

                functions[cell_short] = (pins, f(function_str, pins), function_str)

    return functions


f = lambda pins, function: eval(function)
