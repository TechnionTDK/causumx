import json
import os
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import pycountry
import re
import plotly.express as px


from case_study import so, german, SO_DAG, GERMAN_DAG, ADULT_DAG, adult
from llm_explainer import causumx_output_to_natural_language_explanation
from ui.explanation_visualizer import get_causal_explanation

st.set_page_config(page_title="CauSumX UI", layout="wide")
filename_name = os.path.basename(__file__)
dirname = os.path.dirname(__file__)
PATH = os.path.join(dirname, "data/")
def country_name_to_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_2
    except LookupError:
        print(f"Country not found: {name}")
        if name == 'Turkey':
            return "TR"
        return 'Unknown'


def plot_interactive_bar_chart(data, country_column, value_column, title=None):
    # Convert the data to a DataFrame if it's not already
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    # Ensure the required columns exist
    if country_column not in df.columns or value_column not in df.columns:
        st.error(f"Required columns '{country_column}' or '{value_column}' not found in the data.")
        return

    # Convert value_column to numeric, ignoring errors
    df[value_column] = pd.to_numeric(df[value_column], errors='coerce')

    # Group by country, calculate mean value and count records
    grouped_data = df.groupby(country_column).agg({
        value_column: ['mean', 'count']
    }).reset_index()

    # Flatten the column names
    grouped_data.columns = [country_column, f'Average {value_column}', 'Record Count']

    # Sort and get top 10 countries
    top = grouped_data.sort_values(f'Average {value_column}', ascending=False).head(15)

    # Create the interactive bar chart
    fig = px.bar(
        top,
        x=country_column,
        y=f'Average {value_column}',
        text=f'Average {value_column}',
        hover_data=['Record Count'],
        title=title or f'Top 15 {country_column} by Average {value_column}'
    )

    # Customize the layout
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title=country_column,
        yaxis_title=f'Average {value_column}',
        xaxis_tickangle=-45
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title('✨ CauSumX UI')

    st.markdown("###### A UI for Explaining the Causes of Aggregate SQL Queries Results")

    st.sidebar.subheader('1. Upload Your Data')
    uploaded_dataset = st.sidebar.file_uploader("Upload a dataset CSV file", type=['csv'])
    uploaded_dag = st.sidebar.file_uploader("Upload a DAG (dot file)", type=['dot'])

    st.sidebar.markdown("Or:")
    button_for_dag = st.sidebar.button('Run Causal Discovery Algorithm')

    # actionable_atts input. THis should be (all attributes by default)
    actionable_atts = st.sidebar.text_area("Enter Actionable Attributes (comma-separated). Leave blank for all attributes.")

    st.sidebar.subheader('Or Select a Preloaded Dataset')
    dataset_options_with_explanations = load_dataset_options()

    selected_dataset = st.sidebar.selectbox(
        "Select Dataset",
        options=list(dataset_options_with_explanations.keys()),
        # format_func=lambda x: f"{x} - {dataset_options_with_explanations[x]}"
        format_func=lambda x: f"{x}"
    )

    st.sidebar.subheader('2. Enter Your Query')

    if selected_dataset == CUSTOM_DB_DESCRIPTION:
        st.markdown("custom dataset")
    else:

        sql_query = dataset_options_with_explanations[selected_dataset]["SQL"]
        data_filename = dataset_options_with_explanations[selected_dataset]["data_filename"]

        data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', data_filename), encoding='utf8')

        print(f"Using dataset: {data_filename}")
        print(data.head(100))

        # query_input = st.sidebar.code(causumx_result, language='sql')
        query_input = st.sidebar.text_area("Enter GROUP-BY SQL Query", value=sql_query, height=100)
        size_constraint = st.sidebar.slider("Constraint on Explanation's Size", min_value=1, max_value=10, value=2)
        positive_or_negative = st.sidebar.radio("Causality Direction", ["Both", "Positive", "Negative"], index=1)
        coverage_constraint = st.sidebar.slider("Coverage Constraint", min_value=0.0, max_value=1.0, value=0.20)


        # extract the value insite the AVG (example: SELECT Country, AVG(ConvertedSalary)
        # FROM Stack-Overflow
        # GROUP BY Country -> ConvertedSalary
        # Use regex to support AVG / avg / Avg / aVg / etc. and catch the paranthesis
        pattern = r'AVG\s*\((.*?)\)'

        def extract_avg_value(query):
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
            return None

        target_value = extract_avg_value(query_input)
        if target_value:
            st.markdown(f"Target Value: {target_value}")


        def extract_group_by_value(query):
            pattern = r'GROUP\s+BY\s+(.*?)(?:\s*;|\s*$)'
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            return None


        group_by_value = extract_group_by_value(query_input)
        if group_by_value:
            st.markdown(f"Group By Value: {group_by_value}")

        execute_button = st.sidebar.button('Execute Query')
        if True:
            if not query_input:
                st.error("Please enter a valid SQL GROUP-BY query.")
            else:
                if True:
                    progress_text = f"Running CauSumX with size constraint {size_constraint} and coverage constraint {coverage_constraint}..."
                    my_bar = st.progress(0, text=progress_text)

                    # for percent_complete in range(100):
                    #     time.sleep(0.01)
                    #     my_bar.progress(percent_complete + 1, text=progress_text)

                    dag = dataset_options_with_explanations[selected_dataset]["dag"]
                    # causumx_result = dataset_options_with_explanations[selected_dataset]["function"](k=size_constraint, tau=coverage_constraint)

                    my_bar.empty()

                    # dot_graph = get_causal_explanation()
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 💬 Causal Explanation")

                        # check if causumx_result contains the key "solution_details"
                        # if so, the explanation was generated successfully
                        # otherwise, display an error message

                        script_path = os.path.realpath(__file__)
                        script_directory = os.path.dirname(script_path)
                        filename = "causumx_json_response_example.json"
                        full_path = os.path.join(script_directory, filename)
                        causumx_result = json.load(open(full_path))
                        insights = causumx_output_to_natural_language_explanation(causumx_result)

                        if "solution_details" in causumx_result:
                            insights = causumx_output_to_natural_language_explanation(causumx_result)

                        else:
                            st.error("Failed to generate an explanation. Please check the query and try again.")
                            return

                        for i, insight in enumerate(insights):
                            st.markdown(insight)

                        st.markdown("### Raw JSON")
                        st.json(causumx_result, expanded=False)

                        st.markdown(f"#### 📊 Visualization")
                        plot_interactive_bar_chart(data, group_by_value, target_value)


                    with col2:
                        st.markdown("### 🔷 Graphs")

                        # create tabs based on the number of insights

                        tab_titles = []
                        for i, insight in enumerate(insights):
                            tab_titles.append(f"Insight {i + 1}")

                        # create tabs
                        tabs = st.tabs(tab_titles)

                        for i, tab in enumerate(tabs):
                            # find the
                            red_nodes = list(causumx_result["solution_details"][i]["details"]["t_l"].keys())[0]
                            green_nodes = list(causumx_result["solution_details"][i]["details"]["t_h"].keys())[0]

                            tab.graphviz_chart(get_causal_explanation(dag, green_nodes, red_nodes), use_container_width=True)

                else:
                    st.error("Failed to generate an explanation. Please check the query and try again.")

CUSTOM_DB_DESCRIPTION = "Custom Dataset"

def load_dataset_options():
    datasets_with_explanations = {
        "Stack Overflow":
            {
                "description": "Derived from Stack Overflow, this dataset includes data on posts, comments, votes, and more, ideal for analyzing software development trends.",
                "SQL": "SELECT Country, AVG(ConvertedSalary)\nFROM Stack-Overflow\nGROUP BY Country",
                "function": so,
                "dag": SO_DAG,
                "data_filename": "so_countries_col_new.csv"
            },
        "Adults": {
            "description": "The Adult dataset contains demographic information about adults, including age, education, and income.",
            "SQL": "SELECT occupation, AVG(income)\nFROM Adults\nGROUP BY occupation",
            "function": adult,
            "dag": ADULT_DAG,
            "data_filename": "adult_new.csv",
        },
        "German":
            {

                "description": "The German Credit Data classifies individuals as good or bad credit risks based on several attributes, used commonly in credit scoring models.",
                "SQL": "SELECT purpose, AVG(credit_risk)\nFROM German\nGROUP BY purpose",
                "function": german,
                "dag": GERMAN_DAG,
                "data_filename": "german_credit_data_new.csv"
            },
        CUSTOM_DB_DESCRIPTION: "Upload a dataset CSV file and enter a DAG to get started.",

    }
    return datasets_with_explanations

if __name__ == "__main__":
    main()
