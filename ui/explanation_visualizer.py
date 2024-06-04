import os
from graphviz import Digraph

def get_causal_explanation(dag_path, color='blue'):
    edges_in_paths = set()

    with open(dag_path, 'r') as f:
        dag_data = f.readlines()

    dot = Digraph(comment='The Research DAG', node_attr={'fontname': 'Helvetica-bold', 'fontsize': '8'})
    # Add nodes and edges to the graph
    for item in dag_data:
        item = item.strip()
        if '->' in item:
            start, end = item.split('->')
            start, end = start.strip(), end.strip()
            dot.edge(start, end, arrowsize='0.3')
        else:
            dot.node(item.strip())

    return dot
