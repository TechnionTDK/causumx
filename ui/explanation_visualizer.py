import os
from graphviz import Digraph

def get_causal_explanation(dag_as_list, green_nodes, red_nodes):
    dot = Digraph(comment='The Research DAG', node_attr={'fontname': 'Helvetica-bold', 'fontsize': '8'})
    # Add nodes and edges to the graph
    for item in dag_as_list:
        item = item.strip()
        if '->' in item:
            start, end = item.split('->')
            start, end = start.strip(), end.strip()

            dot.edge(start, end, arrowsize='0.3')

        else:
            if item in green_nodes and item in red_nodes:
                dot.node(item.strip(), style='filled', fillcolor='yellow')
            elif item in green_nodes:
                dot.node(item.strip(), style='filled', fillcolor='green')
            elif item in red_nodes:
                dot.node(item.strip(), style='filled', fillcolor='red')
            else:
                dot.node(item.strip())


    return dot
