import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from explanation_visualizer import get_causal_explanation

st.set_page_config(page_title="CauSumX UI", layout="wide")


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
    st.markdown("#### A UI for Explaining the Causes of Aggregate SQL Queries Results")

    data = pd.read_csv('data/so_countries_col_new.csv')

    st.sidebar.header('1. Upload Your Data')
    uploaded_dataset = st.sidebar.file_uploader("Upload a dataset CSV file", type=['csv'])
    uploaded_dag = st.sidebar.file_uploader("Upload a DAG DOT file", type=['dot'])

    if uploaded_dataset is not None and uploaded_dag is not None:
        # Display the name of the uploaded files (optional)
        st.write("Uploaded dataset:", uploaded_dataset.name)
        st.write("Uploaded DAG:", uploaded_dag.name)

    st.sidebar.header('Or Select a Preloaded Dataset')
    dataset_options_with_explanations = load_dataset_options()
    selected_dataset = st.sidebar.selectbox(
        "Select Dataset",
        options=list(dataset_options_with_explanations.keys()),
        # format_func=lambda x: f"{x} - {dataset_options_with_explanations[x]}"
        format_func=lambda x: f"{x}"
    )

    # Default GROUP-BY SQL query for demo
    st.sidebar.header('2. Enter Your Query')
    default_query = ("SELECT Country, AVG(Salary)\nFROM Stack-Overflow\nGROUP BY Country")
    query_input = st.sidebar.code(default_query, language='sql')
    # query_input = st.sidebar.text_area("Enter GROUP-BY SQL Query", value=default_query, height=150)
    size_constraint = st.sidebar.slider("Constraint on Explanation's Size", min_value=1, max_value=10, value=3)
    positive_or_negative = st.sidebar.radio("Causality Direction", ["Both", "Positive", "Negative"])

    execute_button = st.sidebar.button('Execute Query')

    if True:

        # progress_text = "Running CauSumX... 🏃‍"
        # my_bar = st.progress(0, text=progress_text)
        #
        # for percent_complete in range(100):
        #     time.sleep(0.01)
        #     my_bar.progress(percent_complete + 1, text=progress_text)
        # time.sleep(1)
        # my_bar.empty()
        if not query_input:
            st.error("Please enter a valid SQL GROUP-BY query.")
        else:
            if True:
                dot_graph = get_causal_explanation(query_input, size_constraint)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 💬 Causal Explanation")

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

                    tooltip_html += f"""<p>1️⃣ For countries in {europe_tooltip}, the most substantial effect on high salaries (effect size of 36K, 𝑝 < 1e-3) is observed for individuals under 35 with a Master’s degree. 
                    Conversely, being a student has the greatest adverse impact on annual income (effect size: -39K, 𝑝 < 1e-3).</p>"""

                    high_GDP_level_tooltip = f"""<span class="tooltip" style="background-color: blue;">high GDP level<span class="tooltiptext">{records_from_high_GDP_countries} records</span></span>"""

                    tooltip_html += f"""<p>2️⃣ For countries with a {high_GDP_level_tooltip}, the most substantial effect on high salaries (effect size of 41K, 𝑝 < 1e-3 ) is observed for C-level executives. 
                    Conversely, being over 55 with a bachelor’s degree has the greatest adverse impact on annual income (effect size: -35K,𝑝 < 1e-4).</p>"""

                    high_Gini_coefficient_tooltip = f"""<span class="tooltip" style="background-color: purple;">high Gini coefficient<span class="tooltiptext">{records_from_high_Gini_countries} records</span></span>"""

                    tooltip_html += f"""<p>3️⃣ For countries with a {high_Gini_coefficient_tooltip}, the most substantial effect on high salaries (effect size of 29K, 𝑝 < 1e-4) is observed for white individuals under 45. 
                    Conversely, being having no formal degree has the greatest adverse impact on annual income (effect size: -28K, 𝑝 < 1e-3).</p>"""

                    st.markdown(tooltip_html, unsafe_allow_html=True)

                    st.markdown("### 📊 Result Visualization")

                    # Plotting
                    # fig = plot_bar_chart(countries, values)

                    st.markdown('Top 15 Countries by Average Salary')

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
                            return 'Other'

                    data['Category'] = data['Country'].apply(income_category)

                    income_color_scale = alt.Scale(domain=['High GDP', 'EU', 'High GINI', 'Other'],
                                                   range=['blue', 'red', 'purple', 'gray'])

                    chart = alt.Chart(data).mark_bar().encode(
                        x=alt.X('Country:N', sort=alt.SortField('ConvertedSalary', order='descending')),
                        y='ConvertedSalary:Q',
                        color=alt.Color('Category:N', scale=income_color_scale,
                                        legend=alt.Legend(title="Income Level")),
                    )

                    st.altair_chart(chart, use_container_width=True)

                with col2:
                    st.markdown("### 🔷 Graphs")
                    tab1, tab2, tab3 = st.tabs(["Insight 1", "Insight 2", "Insight 3"])
                    with tab1:
                        st.graphviz_chart(dot_graph, use_container_width=True)

                    # Display Graph 2 in Tab 2
                    with tab2:
                        st.graphviz_chart(get_causal_explanation(None, None, start="FormalEducation", end="ConvertedSalary", color='red'), use_container_width=True)

                    # Display Graph 3 in Tab 3
                    with tab3:
                        st.graphviz_chart(get_causal_explanation(None, None, start="Age", end="ConvertedSalary", color='purple'), use_container_width=True)


            else:
                st.error("Failed to generate an explanation. Please check the query and try again.")


def load_dataset_options():
    datasets_with_explanations = {
        "Stack-Overflow": "Derived from Stack Overflow, this dataset includes data on posts, comments, votes, and more, ideal for analyzing software development trends.",
        "Adults": "The Adult Income dataset contains demographic and employment information from the 1994 U.S. Census database, aimed at predicting if an individual's income exceeds $50K/year.",
        "Countries": "The German Credit Data classifies individuals as good or bad credit risks based on several attributes, used commonly in credit scoring models.",
    }
    return datasets_with_explanations

if __name__ == "__main__":
    main()
