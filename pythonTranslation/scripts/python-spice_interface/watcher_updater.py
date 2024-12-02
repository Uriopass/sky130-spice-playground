import os
import subprocess
from gen_svg import generate_svg

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

    timing_diffs = []

    with open(filename, 'r') as f:
        content = f.read()

        lines = content.split("\n")

        for i in range(len(lines)):
            if lines[i].startswith("# ==="):
                timing_diffs.append(("skip_line", None, None))

            if not lines[i].startswith('# timing'):
                continue

            with_img = lines[i].startswith('# timing with img')

            timing_name, previous_times_str = lines[i].split(":")
            lines[i] = timing_name + ":"
            name = timing_name.split(" ")[-1]
            name = name.lower()

            previous_times_str = previous_times_str.strip()

            previous_times = previous_times_str.split("|")[0].split()


            for v in previous_times:
                lines[i] += " " + v
            if len(previous_times) > 0:
                lines[i] += " |"

            if 'rise_'+name in measures:
                value = measures['rise_'+name]*1e9
                lines[i] += f" {value:.3f}"

            if 'fall_'+name in measures:
                value = measures['fall_'+name]*1e9
                lines[i] += f" {value:.3f}"

            if len(previous_times_str) == 0:
                lines[i] += " |"

            drise = None
            if 'rise_'+name in measures and len(previous_times) > 0:
                value_rise = measures['rise_'+name]*1e9
                previous_rise = float(previous_times[0])
                drise = value_rise-previous_rise

            dfall = None
            if 'fall_'+name in measures and len(previous_times) > 1:
                value = measures['fall_'+name]*1e9
                previous_fall = float(previous_times[1])
                dfall = value-previous_fall

            if (drise is not None and abs(drise) >= 0.001) or (dfall is not None and abs(dfall) >= 0.001):
                if drise is not None:
                    lines[i] += f" {drise:+.3f}"
                else:
                    lines[i] += " ??????"

                if dfall is not None:
                    lines[i] += f" {dfall:+.3f}"
                else:
                    lines[i] += " ??????"

            timing_diffs.append((name, drise, dfall))

        content = "\n".join(lines)

    with open(filename, 'w') as f:
        f.write(content)
        f.flush()

    content = generate_svg(timing_diffs)
    with open('timings.svg', 'w') as f:
        f.write(content)

    print("Updated the script with the new timing values")
def watch_and_run(filename):
    last_mtime = None


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
    filename_to_watch = "python_spice_real.py"  # Replace with your script's filename
    filename_spice_output = "../../../simulations/generated_out.spice"
    print(f"Watching {filename_to_watch} for changes. Press Ctrl+C to stop.")
    watch_and_run(filename_to_watch)
