import requests
import os

cells = ["sky130_fd_sc_hd__or4_1",
"sky130_fd_sc_hd__xnor2_1",
"sky130_fd_sc_hd__mux2_2",
"sky130_fd_sc_hd__a211o_1",
"sky130_fd_sc_hd__mux2_1",
"sky130_fd_sc_hd__a221oi_2",
"sky130_fd_sc_hd__nor2_1",
"sky130_fd_sc_hd__a21oi_2",
"sky130_fd_sc_hd__a311o_2",
"sky130_fd_sc_hd__o211a_1",
"sky130_fd_sc_hd__xor2_1",
"sky130_fd_sc_hd__a21oi_1",
"sky130_fd_sc_hd__a22o_1",
"sky130_fd_sc_hd__a311o_1",
"sky130_fd_sc_hd__clkbuf_4",
"sky130_fd_sc_hd__buf_4",
"sky130_fd_sc_hd__a21o_1",
"sky130_fd_sc_hd__o21a_1",
"sky130_fd_sc_hd__nand2b_1",
"sky130_fd_sc_hd__and2_1",
"sky130_fd_sc_hd__a41o_1"]

def gen_url(cell_name):
    cell_name_short = cell_name.split("__")[1].split("_")[0]
    return f"https://raw.githubusercontent.com/google/skywater-pdk-libs-sky130_fd_sc_hd/refs/heads/main/cells/{cell_name_short}/{cell_name}__tt_025C_1v80.lib.json"

def fetch_json(cell_name):
    url = gen_url(cell_name)
    response = requests.get(url)
    with open(f"libjson/{cell_name}.json", "w") as f:
        f.write(response.text)


os.makedirs("libjson", exist_ok=True)

if __name__ == "__main__":
    for cell in cells:
        fetch_json(cell)