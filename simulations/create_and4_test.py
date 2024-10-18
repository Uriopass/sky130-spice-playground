and4_counter = 0
capacitance_fet =

def and4(A, B, C, D, X):
    global and4_counter
    and4_counter += 1
    i = and4_counter
    return f"""
XA{i}_0 i0_{i} {D}   Vgnd Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_1 i1_{i} {C} i0_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_2 i2_{i} {B} i1_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15
XA{i}_3  o_{i} {A} i2_{i} Vgnd sky130_fd_pr__nfet_01v8 w=0.42 l=0.15

XA{i}_4 o_{i} {D} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_5 o_{i} {C} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_6 o_{i} {B} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15
XA{i}_7 o_{i} {A} Vdd Vdd sky130_fd_pr__pfet_01v8_hvt w=0.42 l=0.15

XA{i}_8 Vgnd o_{i} {X} Vgnd sky130_fd_pr__nfet_01v8 w=0.65 l=0.15
XA{i}_9 Vdd  o_{i} {X} Vdd sky130_fd_pr__pfet_01v8_hvt w=1.0 l=0.15

CA{i} {X} Vgnd 1f
"""

ff_counter = 0

def flipflop(D, Q):
    global ff_counter
    ff_counter += 1
    i = ff_counter
    return f"""
XF{i} clk {D} Vgnd Vgnd Vdd Vdd {Q} sky130_fd_sc_hd__dfxtp_2
"""

cells = []

cell = lambda C: cells.append(C)

# lets generate a list of ands chained together serially, with 3 inputs tied to 3 flip flops, the output goes directly to another flipflop
# the fourth input is tied to the previous "AND4" gate. For the first and4, we simply use Vdd as the "chained" input

N = 10
last_out = "Vdd"
for i in range(N):
    cell(flipflop(f"D{i}_0", f"Q{i}_0"))
    cell(flipflop(f"D{i}_1", f"Q{i}_1"))
    cell(flipflop(f"D{i}_2", f"Q{i}_2"))
    cell(flipflop(f"D{i}_3", f"Q{i}_3"))
    cell(and4(f"A{i}", f"B{i}", f"C{i}", f"D{i}", f"X{i}"))

    last_out = f"D{i}_3"


spice = f"""
.include "./lib/prelude.spice"

Vgnd Vgnd 0 0
Vdd Vdd Vgnd 1.8
Vclk clk Vgnd PULSE(0 1.8 0n 0.2n 0.2n 4.6n 10.0n)

.include ./sky130_fd_sc_hd/cells/dfxtp/sky130_fd_sc_hd__dfxtp_2.spice

{"\n".join(ands)}

.tran 0.01n 10n
.control
run
plot V(clk)
.endc
.end
"""


print(spice)