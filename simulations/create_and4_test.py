import matplotlib.pyplot as plt

from spice import pfet, nfet

and4_counter = 0

def sw_and4_N(A, B, C, D, X, N):
    global and4_counter
    and4_counter += 1
    i = and4_counter

    inverter = []
    for j in range(N):
        inverter.append(pfet(f"A{i}_{j}p", "Vdd", f"o_{i}", X, 1.0))
        inverter.append(nfet(f"A{i}_{j}n", "Vgnd", f"o_{i}", X, 0.65))

    inverter = "\n".join(inverter)

    return f"""
{pfet(f"A{i}_4", f"o_{i}", A, "Vdd", 0.42)}
{pfet(f"A{i}_5", f"o_{i}", B, "Vdd", 0.42)}
{pfet(f"A{i}_6", f"o_{i}", C, "Vdd", 0.42)}
{pfet(f"A{i}_7", f"o_{i}", D, "Vdd", 0.42)}

{nfet(f"A{i}_0", f"i0_{i}", A, "Vgnd", 0.42)}
{nfet(f"A{i}_1", f"i1_{i}", B, f"i0_{i}", 0.42)}
{nfet(f"A{i}_2", f"i2_{i}", C, f"i1_{i}", 0.42)}
{nfet(f"A{i}_3", f"o_{i}", D, f"i2_{i}", 0.42)}

{inverter}

C0_{i} Vdd {B} 0.023081f
C1_{i} o_{i} {D} 0.106582f
C2_{i} Vdd o_{i} 0.082046f
C3_{i} {X} Vdd 0.011072f
C5_{i} o_{i} {C} 0.051593f
C6_{i} Vgnd {B} 0.045272f
C7_{i} {A} o_{i} 0.15343f
C8_{i} Vdd {D} 0.020729f
C10_{i} Vdd {B} 0.064328f
C11_{i} Vdd {C} 0.021032f
C12_{i} {C} {B} 0.160614f
C13_{i} {A} Vdd 0.043995f
C14_{i} Vgnd {D} 0.089796f
C15_{i} {A} {B} 0.083909f
C16_{i} {X} o_{i} 0.075371f
C17_{i} Vgnd {C} 0.040816f
C18_{i} Vgnd {A} 0.015122f
C19_{i} Vdd {D} 0.078225f
C20_{i} o_{i} Vdd 0.326283f
C21_{i} o_{i} {B} 0.129725f
C22_{i} {D} {C} 0.180159f
C23_{i} {X} Vdd 0.094506f
C24_{i} Vdd {C} 0.060876f
C25_{i} {A} Vdd 0.090662f
C26_{i} Vgnd o_{i} 0.13176f
C27_{i} Vgnd {X} 0.09025f
C29_{i} {X} Vgnd 0.093317f
C31_{i} {D} Vgnd 0.130267f
C32_{i} {C} Vgnd 0.109828f
C33_{i} {B} Vgnd 0.112123f
C34_{i} {A} Vgnd 0.220977f
C36_{i} o_{i} Vgnd 0.174893f
"""


def and4(A, B, C, D, X, config):
    global and4_counter
    and4_counter += 1
    i = and4_counter
    return f"""
{pfet(f"A{i}_7", f"o_{i}", A, "Vdd", config["W_ABC_pfet"])}
{pfet(f"A{i}_6", f"o_{i}", B, "Vdd", config["W_ABC_pfet"])}
{pfet(f"A{i}_5", f"o_{i}", C, "Vdd", config["W_ABC_pfet"])}

{nfet(f"A{i}_0", f"i0_{i}", A, "Vgnd", config["W_ABC_nfet"])}
{nfet(f"A{i}_1", f"i1_{i}", B, f"i0_{i}", config["W_ABC_nfet"])}
{nfet(f"A{i}_2", f"i2_{i}", C, f"i1_{i}", config["W_ABC_nfet"])}

{pfet(f"A{i}_4", f"o_{i}", D, "Vdd", config["W_D_pfet"])}
{nfet(f"A{i}_3", f"o_{i}", D, f"i2_{i}", config["W_D_nfet"])}

{pfet(f"A{i}_9", "Vdd", f"o_{i}", X, config["W_inv_pfet"])}
{nfet(f"A{i}_8", "Vgnd", f"o_{i}", X, config["W_inv_nfet"])}

* C0_{i} Vdd {B} 0.023081f
* C1_{i} o_{i} {D} 0.106582f
* C2_{i} Vdd o_{i} 0.082046f
* C3_{i} {X} Vdd 0.011072f
* C5_{i} o_{i} {C} 0.051593f
* C6_{i} Vgnd {B} 0.045272f
* C7_{i} {A} o_{i} 0.15343f
* C8_{i} Vdd {D} 0.020729f
* C10_{i} Vdd {B} 0.064328f
* C11_{i} Vdd {C} 0.021032f
* C12_{i} {C} {B} 0.160614f
* C13_{i} {A} Vdd 0.043995f
* C14_{i} Vgnd {D} 0.089796f
* C15_{i} {A} {B} 0.083909f
* C16_{i} {X} o_{i} 0.075371f
* C17_{i} Vgnd {C} 0.040816f
* C18_{i} Vgnd {A} 0.015122f
* C19_{i} Vdd {D} 0.078225f
* C20_{i} o_{i} Vdd 0.326283f
* C21_{i} o_{i} {B} 0.129725f
* C22_{i} {D} {C} 0.180159f
* C23_{i} {X} Vdd 0.094506f
* C24_{i} Vdd {C} 0.060876f
* C25_{i} {A} Vdd 0.090662f
* C26_{i} Vgnd o_{i} 0.13176f
* C27_{i} Vgnd {X} 0.09025f
* C29_{i} {X} Vgnd 0.093317f
* C31_{i} {D} Vgnd 0.130267f
* C32_{i} {C} Vgnd 0.109828f
* C33_{i} {B} Vgnd 0.112123f
* C34_{i} {A} Vgnd 0.220977f
* C36_{i} o_{i} Vgnd 0.174893f
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

    slope = 8.36
    if extra_fanout <= 0:
        mult = 0
    elif extra_fanout <= len(load_model):
        mult = load_model[extra_fanout - 1]
    else:
        mult = load_model[-1] + slope * (extra_fanout - len(load_model))

    res_base = 0.0 * 0.0745 * 1000.0  # in ohms
    capa_base = 0.0142  # in femtofarads

    res_wire = res_base * mult
    capa_wire = capa_base * mult

    return f"""
Cfanout_{pinout} {pinout} Vgnd {capa_wire}f
Rwire_{pinout} {pinout} {next_pinin} {res_wire}
"""


def in_one(pin):
    return f"""
V{pin} {pin} Vgnd 1.8
"""

def in_zero(pin):
    return f"""
V{pin} {pin} Vgnd 0
"""

def genspice(config):
    cells = []
    addsp = lambda C: cells.append(C)

    N = 10
    to_plot = []

    transition = config.get("transition", "rise")

    if transition == "rise":
        addsp(f".ic V(DstartQ)=0")
        addsp(in_one(f"DstartD"))
    elif transition == "fall":
        addsp(f".ic V(DstartQ)=1.8")
        addsp(in_zero(f"DstartD"))
    else:
        raise ValueError(f"Unknown transition {transition}")

    addsp(flipflop(f"DstartD", f"DstartQ"))
    addsp(flipflop(f"DendD", f"DendQ"))

    last_out = f"clk"

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
    .include "prelude.spice"
    
    Vgnd Vgnd 0 0
    Vdd Vdd Vgnd 1.8
    Vclk clk Vgnd PULSE(0 1.8 0n 0.2n 0.2n 4.6n 10.0n)
    
    .include ../sky130_fd_sc_hd/cells/dfxtp/sky130_fd_sc_hd__dfxtp_2.spice
    
    {cells_spice}
    
    .tran 0.02n 8n

    {measures_spice}
    
    .control
    run
    .endc
    .end
    """

    with open("and4_test.spice", "w") as f:
        f.write(spice)

    # run spice

    import subprocess

    s = subprocess.run(["ngspice", "-b", "and4_test.spice"], capture_output=True, text=True)
    output = s.stdout
    output_err = s.stderr

    tend = None
    tstart = None

    for line in output.split("\n"):
        if line.startswith("tend"):
            tend = float(line.split()[2]) * 1e9
        if line.startswith("tstart"):
            tstart = float(line.split()[2]) * 1e9

    config_str = ""
    for k, v in config.items():
        if k == "transition":
            config_str += f"{k}={v} "
            continue
        config_str += f"{k}={v:.2f} "

    config_str = config_str.strip()

    if tend is None or tstart is None:
        print(f"{config_str} failed")
        print(output_err)
        return None

    print(f"delay = {tend - tstart:.4f} ns  conf:{config_str}")
    return tend - tstart


def cost_fun(D_pfet, D_nfet, inv_pfet, inv_nfet):
    config = {
        "W_D_pfet": D_pfet,
        "W_D_nfet": D_nfet,

        "W_ABC_pfet": 0.36,#ABC_pfet,
        "W_ABC_nfet": 20.0,#ABC_nfet,

        "W_inv_pfet": inv_pfet,
        "W_inv_nfet": inv_nfet,

        "fanout": 4,
    }

    delay_rise = run_sim(config)
    delay_fall = run_sim({**config, "transition": "fall"})

    return -max(delay_rise, delay_fall)

def bayesian_opt():
    from bayes_opt import BayesianOptimization

    base_rise = run_sim({
        "sw_and4_N": 1,
        "fanout": 4,
    }),
    base_fall = run_sim({
        "sw_and4_N": 1,
        "fanout": 4,
        "transition": "fall",
    }),

    print(f"Base rise: {base_rise} fall: {base_fall}")

    fet_bounds = (0.36, 4.0)

    # Bounded region of parameter space
    pbounds = {"D_pfet": fet_bounds,
               "D_nfet": fet_bounds,

                #"ABC_pfet": fet_bounds,
                #"ABC_nfet": (1.0, 20.0),

                "inv_pfet": fet_bounds,
                "inv_nfet": fet_bounds,
               }

    optimizer = BayesianOptimization(
        f=cost_fun,
        pbounds=pbounds,
        random_state=2,
    )

    optimizer.maximize(
        init_points=10,
        n_iter=1000,
    )

# bayesian_opt()
# exit(0)

xs = []
ys = []
ys2 = []

horiz_bars = [
    run_sim({
        "sw_and4_N": 1,
        "fanout": 4,
    }),
    run_sim({
        "sw_and4_N": 1,
        "fanout": 4,
        "transition": "fall",
    }),
]

for i in range(20):
    W = 0.5 + i / 20
    v = 1.0
    config = {
        "W_D_pfet":  1.7 * v,
        "W_D_nfet":  0.8 * v,

        "W_ABC_pfet": 0.36,
        "W_ABC_nfet": 200.0,

        "W_inv_pfet":  1.7 * v,
        "W_inv_nfet":  0.8 * v,

        "fanout": 4,
    }

    xs.append(W)
    ys.append(run_sim(config))

    config["transition"] = "fall"
    ys2.append(run_sim(config))

f, ax = plt.subplots()
ax.plot(xs, ys)
if len(ys2) > 0:
    ax.plot(xs, ys2)
ax.legend()

for bar in horiz_bars:
    ax.axhline(y=bar, color='r', linestyle='--')

ax.set_ylim(bottom=0)
ax.set_xlabel("W")
ax.set_ylabel("Delay (ns)")
f.savefig("and4_test.png")