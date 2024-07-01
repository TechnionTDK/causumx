import pandas as pd
from pyfd import *

# Sample data creation
data = {
    'Country': ['USA', 'Canada', 'Germany', 'Japan', 'India'],
    'GDP': [60000, 45000, 50000, 40000, 30000],
    'HDI': [0.92, 0.91, 0.94, 0.93, 0.89],
    'GINI': [41, 33, 31, 29, 35],
    'Continent': ['North America', 'North America', 'Europe', 'Asia', 'Asia']
}
df = pd.DataFrame(data)

# Initialize PyFD
pyfd = pyfd.PyFD()

# Find functional dependencies
fds = pyfd.fit(df)

# Print functional dependencies
for fd in fds:
    print(fd)
