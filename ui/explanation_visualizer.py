import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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

def get_causal_explanation(query, constraint, start='Continent', end='ConvertedSalary', color='black'):
    dag_data = [
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
        # 'Continent -> Country',
        'Country -> GINI',
        'Country -> GDP',
        'Country -> HDI',
        'FormalEducation -> DevType',
        'FormalEducation -> UndergradMajor',
        # 'Continent -> UndergradMajor',
        # 'Continent -> FormalEducation',
        # 'Continent -> RaceEthnicity',
        # 'Continent -> ConvertedSalary',
        'RaceEthnicity -> ConvertedSalary',
        'RaceEthnicity -> ConvertedSalary',
        'UndergradMajor -> DevType',
        'DevType -> ConvertedSalary',
        'DevType -> ComputerHoursPerDay',
        'Age -> ConvertedSalary',
        'Age -> DevType',
        'Age -> Role',
        'Age -> Student',
        'Student -> DevType',
        'Student -> ConvertedSalary',
        'Role -> ConvertedSalary',
        'Age -> Dependents',
        'Age -> FormalEducation',
        'FormalEducation -> Role',
        'Dependents -> ComputerHoursPerDay',
        'ComputerHoursPerDay -> ConvertedSalary'
    ]

    G = nx.DiGraph()
    for item in dag_data:
        if '->' in item:
            source, target = item.split(' -> ')
            G.add_edge(source.strip(), target.strip())
        else:
            G.add_node(item.strip())

    # Create figure for matplotlib
    fig, ax = plt.subplots(figsize=(12, 10))


    # Specify colors for specific nodes
    node_colors = ["green" if node in ['Role', 'Age', 'FormalEducation'] else "gray" for node in G]

    # Drawing the graph
    # pos = nx.spring_layout(G)  # positions for all nodes
    pos = nx.spring_layout(G, k=4)
    # pos = nx.kamada_kawai_layout(G)

    nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors, edge_color=color, node_size=4000, font_size=15, font_family='sans-serif')

    # No plt.show() here, we're returning the figure object
    return fig