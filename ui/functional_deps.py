import pandas as pd
import numpy as np
from scipy.stats import entropy

def calculate_functional_dependencies(df, grouping_attribute, epsilon=0.1):
    """
    Calculate functional dependencies based on conditional entropy.

    :param df: pandas DataFrame containing the dataset
    :param grouping_attribute: str, the attribute to group by (e.g., 'Country')
    :param epsilon: float, threshold for considering an attribute as functionally dependent
    :return: list of attributes that are functionally dependent on the grouping attribute
    """
    functional_dependencies = []

    # Calculate entropy of the grouping attribute
    grouping_entropy = entropy(df[grouping_attribute].value_counts(normalize=True))

    for column in df.columns:
        if column != grouping_attribute:
            # Calculate conditional entropy
            conditional_entropy = calculate_conditional_entropy(df, grouping_attribute, column)

            # Calculate normalized conditional entropy
            normalized_conditional_entropy = conditional_entropy / grouping_entropy if grouping_entropy != 0 else 0

            # If normalized conditional entropy is close to 0, consider it a functional dependency
            if normalized_conditional_entropy < epsilon:
                functional_dependencies.append(column)

    return functional_dependencies

def calculate_conditional_entropy(df, x, y):
    """
    Calculate conditional entropy H(Y|X)

    :param df: pandas DataFrame
    :param x: str, column name for X (grouping attribute)
    :param y: str, column name for Y
    :return: float, conditional entropy
    """
    # Calculate joint probability
    joint_prob = df.groupby([x, y]).size() / len(df)

    # Calculate marginal probability of X
    x_prob = df[x].value_counts(normalize=True)

    # Calculate conditional probability P(Y|X)
    cond_prob = joint_prob / x_prob

    # Calculate conditional entropy
    cond_entropy = -np.sum(joint_prob * np.log2(cond_prob))

    return cond_entropy

# Example usage
if __name__ == "__main__":
    # Load your data
    df = pd.read_csv("data/so_countries_col_new.csv")
    # Set the grouping attribute (e.g., 'Country')
    grouping_attribute = 'Country'

    # df = pd.read_csv("data/german_credit_data_new.csv")
    # grouping_attribute = 'purpose'

    # df = pd.read_csv("data/adult_new.csv")
    # grouping_attribute = 'occupation'


    # Calculate functional dependencies
    fds = calculate_functional_dependencies(df, grouping_attribute)

    # add the grouping attribute to the list of functional dependencies as the first element
    fds = [grouping_attribute] + fds

    print(f"Functional dependencies for {grouping_attribute}:")
    print(fds)

    # TODO: add this function to the UI app.py file
