import matplotlib.pyplot as plt

bins_nfet = [
    0.36,
    0.39,
    0.42,
    0.52,
    0.54,
    0.55,
    0.58,
    0.6,
    0.61,
    0.64,
    0.65,
    0.74,
    0.84,
    1.0,
    1.26,
    1.68,
    2.0,
    3.0,
    5.0,
    7.0
]

bins_pfet = [
    0.36,
    0.42,
    0.54,
    0.55,
    0.63,
    0.64,
    0.70,
    0.75,
    0.79,
    0.82,
    0.84,
    0.86,
    0.94,
    1.00,
    1.12,
    1.26,
    1.65,
    1.68,
    2.00,
    3.00,
    5.00,
    7.00
]

and4_counter = 0


def sw_and4_N(A, B, C, D, X, N):
    global and4_counter
    and4_counter += 1
    i = and4_counter

    inverter = []
    for j in range(N):
        inverter.append(f"""
XA{i}_{j}p Vdd  o_{i} {X} Vdd  sky130_fd_pr__pfet_01v8_hvt w=1.0  l=0.15
XA{i}_{j}n Vgnd o_{i} {X} Vgnd sky130_fd_pr__nfet_01v8     w=0.65 l=0.15
""")

    inverter = "\n".join(inverter)

    return f"""
XA{i}_4 o_{i} {A} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_5 o_{i} {B} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_6 o_{i} {C} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_7 o_{i} {D} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15

XA{i}_0 i0_{i} {A} Vgnd   Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_1 i1_{i} {B} i0_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_2 i2_{i} {C} i1_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_3  o_{i} {D} i2_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15

{inverter}
"""


def and4(A, B, C, D, X, config):
    global and4_counter
    and4_counter += 1
    i = and4_counter
    return f"""
XA{i}_7 o_{i} {A} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w={config["W_ABC_pfet"]} l=0.15
XA{i}_6 o_{i} {B} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w={config["W_ABC_pfet"]} l=0.15
XA{i}_5 o_{i} {C} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w={config["W_ABC_pfet"]} l=0.15
XA{i}_4 o_{i} {D} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w={config["W_D_pfet"]}   l=0.15

XA{i}_0 i0_{i} {A}   Vgnd Vgnd sky130_fd_pr__nfet_01v8 w={config["W_ABC_nfet"]} l=0.15
XA{i}_1 i1_{i} {B} i0_{i} Vgnd sky130_fd_pr__nfet_01v8 w={config["W_ABC_nfet"]} l=0.15
XA{i}_2 i2_{i} {C} i1_{i} Vgnd sky130_fd_pr__nfet_01v8 w={config["W_ABC_nfet"]} l=0.15
XA{i}_3  o_{i} {D} i2_{i} Vgnd sky130_fd_pr__nfet_01v8 w={config["W_D_nfet"]} l=0.15

XA{i}_9 Vdd  o_{i} {X} Vdd sky130_fd_pr__pfet_01v8_hvt w={config["W_inv_pfet"]} l=0.15
XA{i}_8 Vgnd o_{i} {X} Vgnd sky130_fd_pr__nfet_01v8 w={config["W_inv_nfet"]} l=0.15
"""


ff_counter = 0


def flipflop(D, Q):
    global ff_counter
    ff_counter += 1
    i = ff_counter
    return f"""
XF{i} clk {D} Vgnd Vgnd Vdd Vdd {Q} sky130_fd_sc_hd__dfxtp_2
"""


def wire(pinout, next_pinin, extra_fanout):
    load_model = [23.2746, 32.1136, 48.4862, 64.0974, 86.2649, 84.2649]

    def load_model_extrapolate(fanout):
        slope = 8.36
        if fanout <= 0:
            return 0
        if fanout <= len(load_model):
            return load_model[fanout - 1]
        else:
            return load_model[-1] + slope * (fanout - len(load_model))

    res_base = 0.0745 * 1000.0  # in ohms
    capa_base = 1.42e-5  # in picofarads

    fanout_res = extra_fanout + 1
    fanout_capa = extra_fanout

    mult_res = load_model_extrapolate(fanout_res)
    mult_capa = load_model_extrapolate(fanout_capa)

    res_wire = res_base * mult_res
    capa_wire = capa_base * mult_capa

    return f"""
Cfanout_{pinout} {pinout} Vgnd {capa_wire}p
Rwire_{pinout} {pinout} {next_pinin} {res_wire}
"""


def in_one(pin):
    return f"""
V{pin} {pin} Vgnd 1.8
"""


def genspice(config):
    cells = []
    addsp = lambda C: cells.append(C)

    N = 10
    to_plot = []

    addsp(f".ic V(DstartQ)=0")
    addsp(in_one(f"DstartD"))

    addsp(flipflop(f"DstartD", f"DstartQ"))
    addsp(flipflop(f"DendD", f"DendQ"))

    last_out = f"DstartQ"

    for i in range(N):
        addsp(in_one(f"A{i}"))
        addsp(in_one(f"B{i}"))
        addsp(in_one(f"C{i}"))

        if "sw_and4_N" in config:
            addsp(sw_and4_N(f"A{i}", f"B{i}", f"C{i}", f"D{i}", f"X{i}", config["sw_and4_N"]))
        else:
            addsp(and4(f"A{i}", f"B{i}", f"C{i}", f"D{i}", f"X{i}", config))

        addsp(wire(last_out, f"D{i}", config["fanout"]))

        to_plot.append(f"V(X{i})")

        last_out = f"X{i}"

    addsp(wire(last_out, f"DendD", config["fanout"]))

    cells_spice = "\n".join(cells)
    return cells_spice


def run_sim(config):
    cells_spice = genspice(config)

    measures = [f".measure tran tstart when V(DstartQ) = 0.9",
                f".measure tran tend   when V(DendD) = 0.9"]

    measures_spice = "\n".join(measures)

    spice = f"""
    .include "./lib/prelude.spice"
    
    Vgnd Vgnd 0 0
    Vdd Vdd Vgnd 1.8
    Vclk clk Vgnd PULSE(0 1.8 0n 0.2n 0.2n 4.6n 10.0n)
    
    .include ./sky130_fd_sc_hd/cells/dfxtp/sky130_fd_sc_hd__dfxtp_2.spice
    
    {cells_spice}
    
    .tran 0.01n 5n

    {measures_spice}
    
    .control
    run
    .endc
    .end
    """

    with open("simulations/and4_test.spice", "w") as f:
        f.write(spice)

    # run spice

    import subprocess

    s = subprocess.run(["ngspice", "-b", "simulations/and4_test.spice"], capture_output=True, text=True)
    output = s.stdout
    output_err = s.stderr

    tend = None
    tstart = None

    for line in output.split("\n"):
        if line.startswith("tend"):
            tend = float(line.split()[2]) * 1e9
        if line.startswith("tstart"):
            tstart = float(line.split()[2]) * 1e9

    config_str = " ".join([f"{k}={v:.2f}" for k, v in config.items()])

    if tend is None or tstart is None:
        print(f"{config_str} failed")
        print(output_err)
        return -1.0

    print(f"{config_str} delay = {tend - tstart:.4} ns")
    return tend - tstart


xs = []
ys = []
ys2 = []

horiz_bars = [
    run_sim({
        "sw_and4_N": 1,
        "fanout": 4,
    }),
    run_sim({
        "sw_and4_N": 2,
        "fanout": 4,
    }),
    run_sim({
        "sw_and4_N": 4,
        "fanout": 4,
    }),
    run_sim({
        "sw_and4_N": 8,
        "fanout": 4,
    })
]

for W in bins_nfet:
    config = {
        "W_D_pfet": 0.42,
        "W_D_nfet": 0.42,

        "W_ABC_pfet": 0.42,
        "W_ABC_nfet": W,

        "W_inv_pfet": 1.0,
        "W_inv_nfet": 0.65,

        "fanout": 4,
    }

    xs.append(W)
    ys.append(run_sim(config))

f, ax = plt.subplots()
ax.plot(xs, ys)
if len(ys2) > 0:
    ax.plot(xs, ys2)
ax.legend()

for bar in horiz_bars:
    ax.axhline(y=bar, color='r', linestyle='--')

print(ys)

ax.set_ylim(bottom=0)
ax.set_xlabel("W")
ax.set_ylabel("Delay (ns)")
f.savefig("simulations/and4_test.png")

"""
# config optimale:
    config = {
    "W_D_nfet": 0.58,
    "W_D_pfet": 0.36,

    "W_ABC_nfet": W,
    "W_ABC_pfet": 0.36,

    "W_inv_nfet": 0.36,
    "W_inv_pfet": 2.0,

    "fanout": 4,
}"""
