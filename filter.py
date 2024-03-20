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
