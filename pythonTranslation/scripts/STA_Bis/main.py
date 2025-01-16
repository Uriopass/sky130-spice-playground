import argparse
from sdf_parser import SDF, SDFGraphAnalyzed, SDFGraph

# import os
# from functools import cmp_to_key
# from ordered_set import OrderedSet
# from sdfparse import SDF
# from stars.analysis import SDFGraphAnalyzed
# from stars.graph import SDFGraph
# from stars.instance_name import instance_name
# from stars.parasitics import Parasitics
# from stars.spice import extract_spice_for_manual_analysis
# from stars.subckt import SubcktData

def main():
    parser = argparse.ArgumentParser(description="Analyze SDF graph.")
    parser.add_argument("--subckt", help="Path to the subckt file", default="../libs/ngspice/sky130_subckt")
    parser.add_argument("--sdf", help="Path to the SDF file", default="../libs/sdf/hd_picorv32__nom_tt_025C_1v80.sdf")
    parser.add_argument("--spef", help="Path to the SPEF file")
    args = parser.parse_args()

    # Read SDF content
    sdf_data_path = args.sdf
    with open(sdf_data_path, 'r') as f:
        sdf_content = f.read()

    # Parse SDF content into an SDF object
    sdf = SDF.parse_str(sdf_content)

    # Create the SDF graph
    graph = SDFGraph(sdf)

    # Load SUBCKT data if provided
    subckt = None
    if args.subckt:
        with open(args.subckt, 'r') as f:
            subckt = SubcktData(f.read())
    else:
        print("SUBCKT not passed with --subckt {file}, skipping spice extraction")

    # Load SPEF data if provided
    spef = None
    if args.spef:
        spef = Parasitics(args.spef)
    else:
        print("SPEF not passed with --spef {file}, using wire load model (inaccurate!) for parasitics")

    # Analyze the graph
    analysis = SDFGraphAnalyzed.analyze(graph)
    outputs_with_delay = []
    for output in graph.outputs:
        delay = analysis.max_delay.get(output)
        if delay is not None:
            outputs_with_delay.append((output, delay))

    # Sort outputs by delay in descending order
    outputs_with_delay.sort(key=lambda x: -x[1])

    # Iterate through sorted outputs
    for i, (output, delay) in enumerate(outputs_with_delay[44:45], start=1):
        print(f"{i}  -- {output[0]}{output[1]}:\t{delay:.3f}")
        path = analysis.extract_path(graph, output)
        for (pin, transition), delay in path:
            print(f"  {pin} {transition}{delay:.3f}")

        o_instance = instance_name(output[0])
        o_celltype = graph.instance_celltype[o_instance]
        print(f"  {output[0]}{output[1]} {delay:.3f} {o_instance} {o_celltype}")

        extract_html_for_manual_analysis(graph, analysis, output, delay, path)
        if subckt:
            extract_spice_for_manual_analysis(graph, analysis, subckt, spef, output, delay, path)


if __name__ == "__main__":
    main()
