import json
import os
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pycountry

from case_study import so, german, SO_DAG, GERMAN_DAG
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

def plot_bar_chart(countries, values):
    # Generate a color for each country
    colors = plt.cm.viridis(np.linspace(0, 1, len(countries)))

    fig, ax = plt.subplots()
    # Create bars with different colors
    ax.bar(countries, values, color=colors)

    # Add some labels and title
    ax.set_ylabel('Values')
    ax.set_title('Values by Country')
    ax.set_xticks(range(len(countries)), countries)

    return fig

def main():
    st.title('✨ CauSumX UI')

    st.markdown("###### A UI for Explaining the Causes of Aggregate SQL Queries Results")

    # get the path of the data file by using the current working directory

    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'so_countries_col_new_full.csv'))

    st.sidebar.subheader('1. Upload Your Data')
    uploaded_dataset = st.sidebar.file_uploader("Upload a dataset CSV file", type=['csv'])
    uploaded_dag = st.sidebar.text_input("Upload a DAG (python list)", value=str(SO_DAG))
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
        # query_input = st.sidebar.code(causumx_result, language='sql')
        query_input = st.sidebar.text_area("Enter GROUP-BY SQL Query", value=sql_query, height=100)
        size_constraint = st.sidebar.slider("Constraint on Explanation's Size", min_value=1, max_value=10, value=3)
        positive_or_negative = st.sidebar.radio("Causality Direction", ["Both", "Positive", "Negative"], index=1)
        coverage_constraint = st.sidebar.slider("Coverage Constraint", min_value=0.0, max_value=1.0, value=0.75)

        execute_button = st.sidebar.button('Execute Query')
        if True:
            if not query_input:
                st.error("Please enter a valid SQL GROUP-BY query.")
            else:
                if True:
                    # progress_text = "Running CauSumX... 🏃‍"
                    # my_bar = st.progress(0, text=progress_text)
                    #
                    # for percent_complete in range(100):
                    #     time.sleep(0.01)
                    #     my_bar.progress(percent_complete + 1, text=progress_text)
                    # my_bar.empty()

                    # TODO: what is this??
                    tau = 0.75
                    # causumx_result = dataset_options_with_explanations[selected_dataset]["function"](k=coverage_constraint, tau=tau)

                    # my_bar.empty()

                    # dot_graph = get_causal_explanation()
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 💬 Causal Explanation")

                        script_path = os.path.realpath(__file__)
                        script_directory = os.path.dirname(script_path)
                        filename = "causumx_json_response_example.json"
                        full_path = os.path.join(script_directory, filename)
                        causumx_result = json.load(open(full_path))

                        insights = causumx_output_to_natural_language_explanation(causumx_result)

                        for i, insight in enumerate(insights):
                            st.markdown(insight)

                        st.markdown("### Raw JSON")
                        st.json(causumx_result, expanded=False)
                        def result_visualization(data):
                            # Count records where the 'Continent' column == 'EU'
                            records_from_europe_countries = data[data['Continent'] == 'EU'].shape[0]

                            # Count records where the 'GDP' column == 'High'
                            records_from_high_GDP_countries = data[data['GDP'] == 'High'].shape[0]

                            # Count records where the 'Gini' column == 'High'
                            records_from_high_Gini_countries = data[data['GINI'] == 'High'].shape[0]

                            europe_tooltip = f"""<span class="tooltip">Europe<span class="tooltiptext">{records_from_europe_countries} records</span></span>"""

                            tooltip_html = """
                            <style>
                            .tooltip {
                              position: relative;
                              display: inline; /* Ensure it's an inline element */
                              background-color: red; /* Background color for the highlighted text */
                              color: white; /* Text color */
                              padding: 0 4px; /* Some padding around the text */
                              border-radius: 4px; /* Optional: adds rounded corners */
                              cursor: pointer; /* Changes the cursor to indicate it's interactive */
                            }
        
                            .tooltip .tooltiptext {
                              visibility: hidden;
                              width: 120px;
                              background-color: black;
                              color: #fff;
                              text-align: center;
                              border-radius: 6px;
                              padding: 5px 0;
        
                              /* Position the tooltip text */
                              position: absolute;
                              z-index: 1;
                              bottom: 100%;
                              margin-left: -60px;
                              left: 50%;
                            }
        
                            .tooltip:hover .tooltiptext {
                              visibility: visible;
                            }
                            </style>
                            """

                            # tooltip_html += f"""<p>1️⃣ For countries in {europe_tooltip}, the most substantial effect on high salaries (effect size of 36K, 𝑝 < 1e-3) is observed for individuals under 35 with a Master’s degree.
                            # Conversely, being a student has the greatest adverse impact on annual income (effect size: -39K, 𝑝 < 1e-3).</p>"""

                            tooltip_html += f"""<p>1️⃣ For countries in {europe_tooltip}, the most substantial effect on high salaries (effect size of 36K) is observed for individuals under 35 with a Master’s degree.</p>"""

                            high_GDP_level_tooltip = f"""<span class="tooltip" style="background-color: blue;">high GDP level<span class="tooltiptext">{records_from_high_GDP_countries} records</span></span>"""

                            # tooltip_html += f"""<p>2️⃣ For countries with a {high_GDP_level_tooltip}, the most substantial effect on high salaries (effect size of 41K, 𝑝 < 1e-3 ) is observed for C-level executives.
                            # Conversely, being over 55 with a bachelor’s degree has the greatest adverse impact on annual income (effect size: -35K,𝑝 < 1e-4).</p>"""

                            tooltip_html += f"""<p>2️⃣ For countries with a {high_GDP_level_tooltip}, the most substantial effect on high salaries (effect size of 41K) is observed for C-level executives.</p>"""

                            high_Gini_coefficient_tooltip = f"""<span class="tooltip" style="background-color: purple;">high Gini coefficient<span class="tooltiptext">{records_from_high_Gini_countries} records</span></span>"""

                            tooltip_html += f"""<p>3️⃣ For countries with a {high_Gini_coefficient_tooltip}, the most substantial effect on high salaries (effect size of 29K) is observed for white individuals under 45.</p>"""

                            # st.markdown(tooltip_html, unsafe_allow_html=True)

                            st.markdown("### 📊 Result Visualization")

                            # Plotting
                            # fig = plot_bar_chart(countries, values)

                            # st.markdown('Top 15 Countries by Average Salary')

                            eu_data = data[data['Continent'] == 'EU']
                            eu_countries = eu_data['Country'].unique().tolist()

                            high_gdp_data = data[data['GDP'] == 'High']
                            high_gdp_countries = high_gdp_data['Country'].unique().tolist()

                            high_gini_data = data[data['GINI'] == 'High']
                            high_gini_countries = high_gini_data['Country'].unique().tolist()

                            average_salary_per_country = data.groupby('Country')['ConvertedSalary'].mean()

                            data = average_salary_per_country.reset_index()

                            def income_category(country):
                                if country in high_gdp_countries:
                                    return 'High GDP'
                                elif country in eu_countries:
                                    return 'EU'
                                elif country in high_gini_countries:
                                    return 'High GINI'
                                else:
                                    return 'Uncovered'

                            data['Category'] = data['Country'].apply(income_category)

                            income_color_scale = alt.Scale(domain=['High GDP', 'EU', 'High GINI', 'Uncovered'],
                                                           range=['blue', 'red', 'purple', 'gray'])

                            # change the names of the countries. For example: change United States to US, United Kingdom to UK, etc. Use an external module for that.

                            data['Country'] = data['Country'].apply(country_name_to_code)

                            chart = alt.Chart(data).mark_bar().encode(
                                x=alt.X('Country:N', sort=alt.SortField('ConvertedSalary', order='descending'),
                                        axis=alt.Axis(labelFontWeight='bold', labelFontSize=15, labelColor='black')),
                                y='ConvertedSalary:Q',
                                color=alt.Color('Category:N', scale=income_color_scale,
                                                legend=alt.Legend(title="Income Level")),
                            )

                            # st.altair_chart(chart, use_container_width=True)

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

                            tab.graphviz_chart(get_causal_explanation(SO_DAG, green_nodes, red_nodes), use_container_width=True)

                else:
                    st.error("Failed to generate an explanation. Please check the query and try again.")

CUSTOM_DB_DESCRIPTION = "Custom Dataset"

def load_dataset_options():
    datasets_with_explanations = {
        CUSTOM_DB_DESCRIPTION: "Upload a dataset CSV file and enter a DAG to get started.",
        "Stack Overflow":
            {
            "description": "Derived from Stack Overflow, this dataset includes data on posts, comments, votes, and more, ideal for analyzing software development trends.",
            "SQL": "SELECT Country, AVG(ConvertedSalary)\nFROM Stack-Overflow\nGROUP BY Country",
                "function": so
        },
        "German":
            {

                "description": "The German Credit Data classifies individuals as good or bad credit risks based on several attributes, used commonly in credit scoring models.",
                "SQL": "SELECT purpose, AVG(credit_risk)\nFROM German\nGROUP BY purpose",
                "function": german
            },
        "Accidents": "The Accidents dataset contains information about road accidents, including the severity of the accident and contributing factors.",
        "Adults": "The Adult dataset contains demographic information about adults, including age, education, and income.",
    }
    return datasets_with_explanations

if __name__ == "__main__":
    main()
