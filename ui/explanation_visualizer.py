import streamlit as st
from graphviz import Digraph
import networkx as nx


def find_all_paths(graph_data, start, end):
    """
    Finds all paths from start node to end node.

    :param graph_data: List of tuples or a list of strings with '->' indicating edges.
    :param start: Start node.
    :param end: End node.
    :return: A list of paths, where each path is a list of nodes.
    """
    G = nx.DiGraph()

    # Add edges to the graph
    for item in graph_data:
        if '->' in item:
            source, target = item.split(' -> ')
            G.add_edge(source.strip(), target.strip())

    # Find all simple paths
    paths = list(nx.all_simple_paths(G, source=start, target=end))

    return paths

def get_causal_explanation(query, constraint, start='Continent', end='ConvertedSalary', color='blue'):
    dag = [
        'Continent',
        'ComputerHoursPerDay',
        'UndergradMajor',
        'FormalEducation',
        'Age',
        'Gender',
        'Dependents',
        'Country',
        'DevType',
        'RaceEthnicity',
        'ConvertedSalary',
        'HDI',
        'GINI',
        'GDP',
        'HDI -> GINI',
        'GINI -> ConvertedSalary',
        'GINI -> GDP',
        'GDP -> ConvertedSalary',
        'Gender -> FormalEducation',
        'Gender -> UndergradMajor',
        'Gender -> DevType',
        'Gender -> ConvertedSalary',
        'Country -> ConvertedSalary',
        'Country -> FormalEducation',
        'Country -> RaceEthnicity',
        'Continent -> Country',
        'Country -> GINI',
        'Country -> GDP',
        'Country -> HDI',
        'FormalEducation -> DevType',
        'FormalEducation -> UndergradMajor',
        'Continent -> UndergradMajor',
        'Continent -> FormalEducation',
        'Continent -> RaceEthnicity',
        'Continent -> ConvertedSalary',
        'RaceEthnicity -> ConvertedSalary',
        'UndergradMajor -> DevType',
        'DevType -> ConvertedSalary',
        'DevType -> ComputerHoursPerDay',
        'Age -> ConvertedSalary',
        'Age -> DevType',
        'Age -> Student',
        'Student -> DevType',
        'Student -> ConvertedSalary',
        'Age -> Dependents',
        'Age -> FormalEducation',
        'Dependents -> ComputerHoursPerDay',
        'ComputerHoursPerDay -> ConvertedSalary'
    ]

    # paths = find_all_paths(dag, start, end)
    #
    # # Create a set of all edges that are part of any path from 'Continent' to 'ConvertedSalary'
    edges_in_paths = set()
    # for path in paths:
    #     edges_in_paths.update(zip(path, path[1:]))
    #
    # # Initialize a Digraph object
    # dot = Digraph(comment='The Research DAG')
    #
    # # Add nodes and edges to the graph
    # for item in dag:
    #     if '->' in item:
    #         start, end = item.split(' -> ')
    #         start, end = start.strip(), end.strip()
    #         if (start, end) in edges_in_paths:
    #             dot.edge(start, end, color=color)  # Color the path from 'Continent' to 'ConvertedSalary'
    #         else:
    #             dot.edge(start, end)
    #     else:
    #         dot.node(item.strip())

    dot = Digraph(comment='The Research DAG', node_attr={'fontname': 'Helvetica-bold', 'fontsize': '9'})
    # Add nodes and edges to the graph
    for item in dag:
        if '->' in item:
            start, end = item.split(' -> ')
            start, end = start.strip(), end.strip()
            if start == 'Student' or start == 'Age' or start == 'FormalEducation':
                dot.node(start, color='red')
            if start == start == 'Age' or start == 'FormalEducation':
                dot.node(start, color='green')
            if (start, end) in edges_in_paths:
                dot.edge(start, end, color=color)  # Color the path from 'Continent' to 'ConvertedSalary'
            else:
                dot.edge(start, end)
        else:
            dot.node(item.strip())

    return dot

