from graphviz import Digraph


def get_causal_explanation(color='blue'):
    dag_data = [
        'Gender',
        'Age',
        'Ethnicity',
        'Major',
        'Education',
        'YearsCoding',
        'Role',
        'Salary',
        'Country -> Education',
        'Country -> Salary',
        'Gender -> Education',
        'Gender -> Major',
        'Gender -> YearsCoding',
        'Gender -> Salary',
        'Age -> Major',
        'Age -> Education',
        'Age -> YearsCoding',
        'Age -> Role',
        'Age -> Salary',
        'Ethnicity -> Major',
        'Ethnicity -> Education',
        'Ethnicity -> Salary',
        'Major -> YearsCoding',
        'Major -> Role',
        'Education -> YearsCoding',
        'Education -> Role',

        'Country',

    ]

    edges_in_paths = set()


    dot = Digraph(comment='The Research DAG', node_attr={'fontname': 'Helvetica-bold', 'fontsize': '8'})
    # dot = Digraph(comment='The Research DAG', node_attr={'fontname': 'Helvetica-bold'})
    # Add nodes and edges to the graph
    for item in dag_data:
        if '->' in item:
            start, end = item.split(' -> ')
            start, end = start.strip(), end.strip()
            # if start == 'Student' or start == 'Age' or start == 'FormalEducation':
            #     dot.node(start, color='red')
            if start == start == 'Age' or start == 'Education':
                dot.node(start, color='green')
            if (start, end) in edges_in_paths:
                dot.edge(start, end, color=color, arrowsize='0.3')
            else:
                dot.edge(start, end, arrowsize='0.3')
        else:
            dot.node(item.strip())

    return dot

