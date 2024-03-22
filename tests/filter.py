import pandas as pd

# Load the CSV file
df = pd.read_csv('so_countries_col_new.csv')

# Group by 'Country' and calculate the average 'Salary' for each country
country_salary_avg = df.groupby('Country')['ConvertedSalary'].mean().reset_index()

# Sort the countries by the size of their groups in descending order
# and then take the top 15
top_countries = df['Country'].value_counts().head(15).index.tolist()

# Filter the average salary DataFrame to include only the top 15 countries
top_countries_avg_salary = country_salary_avg[country_salary_avg['Country'].isin(top_countries)]

# Sort the result by average salary in descending order to see the top countries by average salary
top_countries_avg_salary_sorted = top_countries_avg_salary.sort_values(by='ConvertedSalary', ascending=False)

# Display the result
print(top_countries_avg_salary_sorted)



gdp_data = pd.read_csv('data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_2.csv')

# sort by the 2022 GDP
gdp_data = gdp_data.sort_values(by='2022', ascending=False)

# create a function that checks if a country has a high GDP
def is_high_GDP(country):
    return gdp_data[gdp_data['Country Name'] == country]['2022'].values[0] > high_GDP_threshold


# Load the GINI index data
data = pd.read_csv('data/API_SI.POV.GINI_DS2_en_csv_v2_16.csv')
# Filter out the columns not related to the years and the GINI index values
years_columns = data.columns[
                4:-1]  # Exclude 'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', and the last unnamed column

# For each country, get the rightmost non-empty (non-NaN) value for GINI index
rightmost_non_empty_values = data.apply(
    lambda row: row[years_columns].dropna().iloc[-1] if not row[years_columns].dropna().empty else "", axis=1)

# Combine the country names with their corresponding rightmost non-empty GINI index values
country_gini = pd.DataFrame({
    "Country Name": data["Country Name"],
    "Rightmost GINI Index": rightmost_non_empty_values
})

def is_high_Gini(country):
    return country_gini[country_gini['Country Name'] == country]['Rightmost GINI Index'].values[0] > high_Gini_threshold

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

def process_data_2():
    csv_file = open('data/so_countries_col_new.csv', 'r')

    data = pd.read_csv(csv_file)

    # st.bar_chart(data.set_index('Country')['ConvertedSalary'])

    # Set the index to 'Country' if it's not already
    data = data.set_index('Country')

    # add gdps to the data
    data['GDP'] = data.index.map(lambda country: gdp_data[gdp_data['Country Name'] == country]['2022'].values[0])

    # add gini coefficients to the data
    data['Gini'] = data.index.map(lambda country: country_gini[country_gini['Country Name'] == country]['Rightmost GINI Index'].values[0])

        # count the number of records with countries in Europe
    records_from_europe_countries = data[data.index.isin(european_countries)]

    records_from_countries_with_high_gdp = data[data['GDP'] > high_GDP_threshold]
    records_from_countries_with_high_gini = data[data['Gini'] > high_Gini_threshold]
