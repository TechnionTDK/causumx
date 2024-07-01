
import matplotlib.pyplot as plt
import streamlit as st



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
        x=alt.X(f'{group_by_value}:N', sort=alt.SortField(avg_value, order='descending'),
                axis=alt.Axis(labelFontWeight='bold', labelFontSize=15, labelColor='black')),
        y=f'{avg_value}:Q',
        color=alt.Color('Category:N', scale=income_color_scale,
                        # legend=alt.Legend(title="Income Level")
                        ),
    )

    st.altair_chart(chart, use_container_width=True)
