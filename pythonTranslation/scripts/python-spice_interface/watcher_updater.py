import time
import os
import subprocess

def watch_and_run(filename):
    try:
        last_mtime = os.path.getmtime(filename)
    except FileNotFoundError:
        last_mtime = None
        print(f"{filename} not found. Waiting for it to be created...")

    process_running = False

    while True:
        try:
            current_mtime = os.path.getmtime(filename)
            if last_mtime is None or current_mtime != last_mtime:
                last_mtime = current_mtime
                if process_running:
                    print("Previous process is still running. Waiting for it to finish before starting a new one.")
                    continue
                print(f"{filename} modified. Running script...")
                process_running = True
                # Start the subprocess and wait for it to finish
                result = subprocess.run(["python3", filename])
                run_spice = subprocess.run(["ngspice", "-b", filename_spice_output])
                print(run_spice)
                process_running = False
                print(f"Script finished with exit code {result.returncode}")
        except FileNotFoundError:
            if last_mtime is not None:
                print(f"{filename} was deleted. Waiting for it to be recreated...")
            last_mtime = None

if __name__ == "__main__":
    filename_to_watch = "python_spice.py"  # Replace with your script's filename
    filename_spice_output = "../../../simulations/generated_out.spice"
    print(f"Watching {filename_to_watch} for changes. Press Ctrl+C to stop.")
    watch_and_run(filename_to_watch)
