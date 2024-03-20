import streamlit as st
from src.causumx import CauSumX
from ui.explanation_visualizer import get_causal_explanation

st.set_page_config(page_title="CauSumX UI", layout="wide")

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Example data
countries = ["USA", "Canada", "Germany", "UK", "France"]
values = [10, 20, 30, 40, 50]

import pandas as pd
import streamlit as st


# Function to process the data
def process_data(csv_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Group by 'Country' and calculate the average 'Salary' for each country
    country_salary_avg = df.groupby('Country')['ConvertedSalary'].mean().reset_index()

    # Sort the countries by the size of their groups in descending order
    # and then take the top 15
    top_countries = df['Country'].value_counts().head(15).index.tolist()

    # Filter the average salary DataFrame to include only the top 15 countries
    top_countries_avg_salary = country_salary_avg[country_salary_avg['Country'].isin(top_countries)]

    # Sort the result by average salary in descending order to see the top countries by average salary
    top_countries_avg_salary_sorted = top_countries_avg_salary.sort_values(by='ConvertedSalary', ascending=False)

    return top_countries_avg_salary_sorted




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
        format_func=lambda x: f"{x} - {dataset_options_with_explanations[x]}"
    )

    # Default GROUP-BY SQL query for demo
    st.sidebar.header('2. Enter Your Query')
    default_query = ("SELECT Country, AVG(Salary) FROM Stack-Overflow GROUP BY Country")
    query_input = st.sidebar.text_area("Enter GROUP-BY SQL Query", value=default_query, height=150)
    size_constraint = st.sidebar.slider("Constraint on Explanation's Size", min_value=1, max_value=10, value=3)

    execute_button = st.sidebar.button('Execute Query')

    if True:
        if not query_input.strip():
            st.error("Please enter a valid SQL GROUP-BY query.")
        else:
            if selected_dataset == "Uploaded Dataset":
                causumx = CauSumX("uploaded")
            else:
                causumx = CauSumX(selected_dataset)

            # Get explanation (mock functionality for demonstration)
            explanation = {"summary": "This is a mock explanation based on the selected dataset and query."}

            if explanation:
                explanation, dot_graph = get_causal_explanation(query_input, size_constraint)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 💬 Causal Explanation")

                    europe_tooltip = """<span class="tooltip">Europe<span class="tooltiptext">2123 records</span></span>"""

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

                    tooltip_html += f"""<p>For countries in {europe_tooltip}, the most substantial effect on high salaries (effect size of 36K, 𝑝 < 1e-3) is observed for individuals under 35 with a Master’s degree. 
                    Conversely, being a student has the greatest adverse impact on annual income (effect size: -39K, 𝑝 < 1e-3).</p>"""

                    high_GDP_level_tooltip = """<span class="tooltip" style="background-color: blue;">high GDP level<span class="tooltiptext">1000 records</span></span>"""

                    tooltip_html += f"""<p>For countries with a {high_GDP_level_tooltip}, the most substantial effect on high salaries (effect size of 41K, 𝑝 < 1e-3 ) is observed for C-level executives. 
                    Conversely, being over 55 with a bachelor’s degree has the greatest adverse impact on annual income (effect size: -35K,𝑝 < 1e-4 ).</p>"""

                    high_Gini_coefficient_tooltip = """<span class="tooltip" style="background-color: purple;">high Gini coefficient<span class="tooltiptext">500 records</span></span>"""

                    tooltip_html += f"""<p>For countries with a {high_Gini_coefficient_tooltip}, the most substantial effect on high salaries (effect size of 29K, 𝑝 < 1e-4) is observed for white individuals under 45. 
                    Conversely, being having no formal degree has the greatest adverse impact on annual income (effect size: -28K, 𝑝 < 1e-3).</p>"""

                    st.markdown(tooltip_html, unsafe_allow_html=True)

                    st.markdown("### 📊 Result Visualization")

                    # Plotting
                    # fig = plot_bar_chart(countries, values)

                    st.text('Top 15 Countries by Average Salary')

                    # File uploader allows user to add their own CSV
                    csv_file = open('so_countries_col_new.csv', 'r')

                    if csv_file is not None:
                        data = process_data(csv_file)

                        # Display the DataFrame
                        # st.write(data)

                        # Create a bar chart
                        st.bar_chart(data.set_index('Country')['ConvertedSalary'])


                    # Use Streamlit to display the figure
                    # TODO: all the country in europe should be yellow
                    # TODO: countries with a high GDP level should be green
                    # TODO: hover over "Europe" - "There are 2000 individuals in the dataset from Europe"
                    # TODO: countries with a high GDP - "There are 1000 individuals in the dataset from countries with a high GDP"
                    # TODO: countries with a high Gini coefficient  - "There are 500 individuals in the dataset from countries with a high Gini coefficient"
                    # countries with a high Gini coefficient should be pink
                    # st.pyplot(fig)

                with col2:
                    st.markdown("### 📊 Visualization")
                    st.graphviz_chart(dot_graph, use_container_width=True)


            else:
                st.error("Failed to generate an explanation. Please check the query and try again.")


def load_dataset_options():
    datasets_with_explanations = {
        "adult": "The Adult Income dataset contains demographic and employment information from the 1994 U.S. Census database, aimed at predicting if an individual's income exceeds $50K/year.",
        "german": "The German Credit Data classifies individuals as good or bad credit risks based on several attributes, used commonly in credit scoring models.",
        "stackoverflow": "Derived from Stack Overflow, this dataset includes data on posts, comments, votes, and more, ideal for analyzing software development trends."
    }
    return datasets_with_explanations

if __name__ == "__main__":
    main()
