from dag import DAG

dag = DAG.load_from_file("dag_hs.json")

dag.analyze_cell_widths()