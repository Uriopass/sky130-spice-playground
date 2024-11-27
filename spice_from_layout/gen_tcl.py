import os
import subprocess
import shutil

def extract_cellnames(gds) -> list[str]:
    import re
    cellnames = []
    with open(gds, "rb") as f:
        bytes = f.read()
        matches = re.findall(b"sky130_fd_sc_[a-z][a-z]__[_a-z\-0-9]+", bytes)
        for match in matches:
            cellname = match.decode("utf-8")
            cellnames.append(cellname)
    return cellnames

for prefix in ["sky130_fd_sc_hd", "sky130_fd_sc_hs"]:
    print(*extract_cellnames(f"{prefix}.gds"), sep="\n")

exit(0)

for prefix in ["sky130_fd_sc_hd", "sky130_fd_sc_hs"]:
    cellnames = extract_cellnames(f"{prefix}.gds")

    cellnames.remove(f"{prefix}__inv_1")
    cellnames.remove(f"{prefix}__inv_2")
    cellnames.remove(f"{prefix}__inv_4")
    cellnames.remove(f"{prefix}__inv_8")
    cellnames.remove(f"{prefix}__inv_16")

    cellnames.insert(0, f"{prefix}__inv_1")
    cellnames.insert(1, f"{prefix}__inv_2")
    cellnames.insert(2, f"{prefix}__inv_4")
    cellnames.insert(3, f"{prefix}__inv_8")
    cellnames.insert(4, f"{prefix}__inv_16")

    ext2spice = []

    for cellname in cellnames:
        ext2spice.append(f"""
    load {cellname}
    select top cell
    extract do resistance
    extract all
    ext2sim labels on;
    ext2sim -p ext
    extresist all  
    port makeall
    ext2spice -p ext -o spice/{cellname}.spice
    """)

    ext2spice = "\n".join(ext2spice)

    tcl = f"""
    # read design
    gds read {prefix}.gds
    
    extract path ext
    
    ext2spice lvs
    ext2spice cthresh 0
    ext2spice rthresh 0
    ext2spice extresist on
    ext2spice subcircuit on
    ext2spice ngspice
    
    {ext2spice}
    
    # quit
    quit
    """

    with open("pex.tcl", "w") as f:
        f.write(tcl)

    os.makedirs("spice", exist_ok=True)
    os.makedirs("ext", exist_ok=True)
    os.makedirs("sim", exist_ok=True)

    s = subprocess.run(
        ["magic", "-dnull", "-noconsole", "-rcfile", "~/.volare/sky130A/libs.tech/magic/sky130A.magicrc", "pex.tcl"])

    for file in os.listdir("ext"):
        filename = file.split(".")[0]
        try:
            os.remove(f"{filename}.nodes")
            os.remove(f"{filename}.sim")
        except Exception as e:
            pass

    if s.returncode != 0:
        print("Failed to run magic")
        exit(1)

    # consolidate all spice/ files into a single file

    with open(f"{prefix}.spice", "w") as f2:
        for cell in cellnames:
            try:
                with open(f"spice/{cell}.spice", "r") as f:
                    content = f.read()

                    if cell.startswith(f"{prefix}__inv_"):
                        newcontent = ""
                        for line in content.split("\n"):
                            if line.startswith(".subckt"):
                                newcontent += f".subckt {cell} A VGND VNB VPB VPWR Y\n"
                                continue
                            newcontent += line + "\n"
                        content = newcontent
                    f2.write(content)
            except FileNotFoundError:
                print(f"Failed to find spice file for {cell}")
                pass

    shutil.rmtree("spice")
    shutil.rmtree("ext")
    shutil.rmtree("sim")
