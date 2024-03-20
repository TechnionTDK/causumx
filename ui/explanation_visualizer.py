import streamlit as st
from graphviz import Digraph


def get_causal_explanation(query, constraint):
    # Placeholder for the algorithm implementation
    # Returns a tuple of (natural language explanation, dot graph for visualization)
    explanation = "Given the GROUP-BY clause on 'ProductCategory', the significant variation in sales is primarily due to seasonal demand changes and promotional events. For instance, 'Electronics' peak during November due to Black Friday sales."
    from graphviz import Digraph

    # Your DAG representation
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
        'Age -> Dependents',
        'Age -> FormalEducation',
        'Dependents -> ComputerHoursPerDay',
        'ComputerHoursPerDay -> ConvertedSalary'
    ]

    # Initialize a Digraph object
    dot = Digraph(comment='The Research DAG')

    # Add nodes and edges to the graph
    for item in dag:
        if '->' in item:
            start, end = item.split(' -> ')
            dot.edge(start, end)
        else:
            dot.node(item)

    # TODO: students vertex to salary - this route should be marked red (like with a marker)
    return explanation, dot

# def visualize_explanation_with_dag():
#     st.subheader("Causal Explanation Visualization")
#
#     # Define the DAG using Graphviz's Dot language as a string
#     dag_dot = """
#         digraph {
#             "A" [label="Education"]
#             "B" [label="Workclass"]
#             "C" [label="Occupation"]
#             "D" [label="Hours-per-week"]
#             "E" [label="Income"]
#
#             A -> C
#             B -> C
#             C -> D
#             D -> E
#         }
#     """
#
#     # Use Streamlit's built-in function to display the graph
#     st.graphviz_chart(dag_dot, use_container_width=True)


if __name__ == '__main__':
    st.title('Causal Explanation Visualization Demo')
    visualize_explanation_with_dag()
