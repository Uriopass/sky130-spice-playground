import time
import os
import subprocess

def parse_measures(stdout):
    """
    Parse the measures from a spice output
    e.g lines that look like t_start = 1.0
    :param stdout: The stdout from the spice simulation
    :return: A dictionary containing the measures
    """
    measures = {}
    for line in stdout.split("\n"):
        vals = line.strip().split()
        if len(vals) != 3:
            continue
        if vals[1] != "=":
            continue
        if not vals[2][0].isdigit():
            continue
        measures[vals[0]] = float(vals[2])
    return measures

def run(filename):
    # Start the subprocess and wait for it to finish
    result = subprocess.run(["python3", filename])
    print(f"python script finished with exit code {result.returncode}")
    out = subprocess.run(["ngspice", "-b", filename_spice_output], capture_output=True)
    print(f"ngspice finished with exit code {out.returncode}")
    if out.returncode != 0:
        print(out.stderr.decode("utf-8"))
        return

    stdout = out.stdout.decode("utf-8")
    measures = parse_measures(stdout)

    print(measures)

    with open(filename, 'r') as f:
        content = f.read()

        lines = content.split("\n")

        for i in range(len(lines)):
            if not lines[i].startswith('# timing for'):
                continue
            lines[i] = lines[i].split(":")[0]
            name = lines[i].split(" ")[-1]
            lines[i] += ':'
            name = name.lower()
            if name in measures:
                value = measures[name]*1e9
                lines[i] += f" {value:.2f}n"

        content = "\n".join(lines)

    with open("timings_"+filename, 'w') as f:
        f.write(content)
def watch_and_run(filename):
    try:
        last_mtime = os.path.getmtime(filename)
    except FileNotFoundError:
        last_mtime = None
        print(f"{filename} not found. Waiting for it to be created...")


    while True:
        try:
            current_mtime = os.path.getmtime(filename)
            if last_mtime is None or current_mtime != last_mtime:
                print(f"{filename} modified. Running script...")
                run(filename)

                last_mtime = os.path.getmtime(filename)
        except FileNotFoundError:
            if last_mtime is not None:
                print(f"{filename} was deleted. Waiting for it to be recreated...")
            last_mtime = None

if __name__ == "__main__":
    filename_to_watch = "python_spice.py"  # Replace with your script's filename
    filename_spice_output = "../../../simulations/generated_out.spice"
    print(f"Watching {filename_to_watch} for changes. Press Ctrl+C to stop.")
    watch_and_run(filename_to_watch)
