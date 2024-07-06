import pandas as pd
import numpy as np
from typing import List, Set, Tuple
import pandas as pd
import numpy as np
from typing import List, Set, Tuple
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


import pandas as pd
import numpy as np
from typing import List, Set, Tuple
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class Rule:
    def __init__(self, condition: str, treatment: str, covered_indices: Set[int],
                 covered_protected_indices: Set[int], utility: float, protected_utility: float):
        self.condition = condition
        self.treatment = treatment
        self.covered_indices = covered_indices
        self.covered_protected_indices = covered_protected_indices
        self.utility = utility
        self.protected_utility = protected_utility

def estimate_cate(df: pd.DataFrame, condition: str, treatment: str, outcome: str, covariates: List[str]):
    # Select the relevant data
    condition_mask = df.eval(condition)
    X = df[condition_mask]

    # Prepare the treatment variable
    T = X.eval(treatment).astype(int)

    # Check if we have only one class in the treatment variable
    if len(np.unique(T)) < 2:
        return 0, len(X)  # Return 0 as CATE and the number of covered samples

    # Prepare the outcome variable
    Y = X[outcome]

    # Prepare the covariates
    numeric_features = [cov for cov in covariates if X[cov].dtype in ['int64', 'float64']]
    categorical_features = [cov for cov in covariates if X[cov].dtype == 'object']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features)
        ])

    # Fit the preprocessor on all data to capture all categories
    X_processed = preprocessor.fit_transform(X[covariates])

    # Fit propensity score model
    ps_model = LogisticRegression(solver='lbfgs', max_iter=1000)
    ps_model.fit(X_processed, T)
    ps = ps_model.predict_proba(X_processed)[:, 1]

    # Fit outcome models
    outcome_model_t = LinearRegression()
    outcome_model_c = LinearRegression()

    outcome_model_t.fit(X_processed[T == 1], Y[T == 1])
    outcome_model_c.fit(X_processed[T == 0], Y[T == 0])

    # Compute CATE using doubly robust estimator
    Y_t = outcome_model_t.predict(X_processed)
    Y_c = outcome_model_c.predict(X_processed)

    dr_t = np.mean((T * (Y - Y_t) / ps) + Y_t)
    dr_c = np.mean(((1 - T) * (Y - Y_c) / (1 - ps)) + Y_c)

    cate = dr_t - dr_c

    return cate, len(X)


def generate_rules(df: pd.DataFrame, protected_attribute: str, outcome: str, covariates: List[str]) -> List[Rule]:
    rules = []
    attributes = ['Country', 'FormalEducation', 'DevType']  # Add more attributes as needed

    for attr in attributes:
        for value in df[attr].unique():
            condition = f"{attr} == '{value}'"
            for treatment_attr in attributes:
                if treatment_attr != attr:
                    for treatment_value in df[treatment_attr].unique():
                        treatment = f"{treatment_attr} == '{treatment_value}'"

                        covered = df.query(condition).index
                        covered_protected = df[df[protected_attribute] != 'Male'].query(condition).index

                        # Perform causal inference calculation
                        cate, num_covered = estimate_cate(df, condition, treatment, outcome, covariates)
                        utility = cate * num_covered

                        # Calculate protected utility
                        protected_df = df[df[protected_attribute] != 'Male']
                        protected_cate, num_protected_covered = estimate_cate(protected_df, condition, treatment,
                                                                              outcome, covariates)
                        protected_utility = protected_cate * num_protected_covered

                        rules.append(Rule(condition, treatment, set(covered), set(covered_protected), utility,
                                          protected_utility))

    return rules




def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def score_rule(rule: Rule, solution: List[Rule], covered: Set[int], covered_protected: Set[int],
               total_utility: float, protected_utility: float, protected_group: Set[int],
               coverage_threshold: float) -> float:
    new_covered = rule.covered_indices - covered
    new_covered_protected = rule.covered_protected_indices - covered_protected

    if len(rule.covered_indices) == 0:
        return float('-inf')

    overlap_factor = 1 - (len(new_covered) / len(rule.covered_indices))

    utility_increase = rule.utility
    protected_utility_increase = rule.protected_utility

    if len(covered_protected) + len(new_covered_protected) == 0:
        fairness_factor = 1
    else:
        fairness_factor = 1 - abs(
            (protected_utility + protected_utility_increase) / (len(covered_protected) + len(new_covered_protected)) -
            (total_utility + utility_increase) / (len(covered) + len(new_covered)))

    coverage_factor = (len(new_covered_protected) / len(
        protected_group)) / coverage_threshold if coverage_threshold > 0 else 1

    return (utility_increase + protected_utility_increase) * (1 - overlap_factor) * fairness_factor * coverage_factor


def greedy_fair_prescription_rules(rules: List[Rule], protected_group: Set[int], coverage_threshold: float,
                                   max_rules: int) -> List[Rule]:
    solution = []
    covered = set()
    covered_protected = set()
    total_utility = 0
    protected_utility = 0

    while len(solution) < max_rules:
        best_rule = None
        best_score = float('-inf')

        for rule in rules:
            if rule not in solution:
                score = score_rule(rule, solution, covered, covered_protected,
                                   total_utility, protected_utility, protected_group, coverage_threshold)
                if score > best_score:
                    best_score = score
                    best_rule = rule

        if best_rule is None:
            break

        solution.append(best_rule)
        covered.update(best_rule.covered_indices)
        covered_protected.update(best_rule.covered_protected_indices)
        total_utility += best_rule.utility
        protected_utility += best_rule.protected_utility

    return solution


def main():
    df = load_data('../ui/data/so_countries_col_new.csv')

    # Define protected group (non-male in this case)
    protected_group = set(df[df['Gender'] != 'Male'].index)

    # Define covariates for causal inference
    covariates = ['Age', 'YearsCoding', 'HoursComputer', 'EducationParents', 'HDI', 'GDP', 'GINI']

    # Generate rules
    rules = generate_rules(df, 'Gender', 'ConvertedSalary', covariates)

    # Run greedy algorithm
    coverage_threshold = 0.1
    max_rules = 5
    solution = greedy_fair_prescription_rules(rules, protected_group, coverage_threshold, max_rules)

    # Print results
    print(f"Selected {len(solution)} rules:")
    for i, rule in enumerate(solution, 1):
        print(f"Rule {i}:")
        print(f"  Condition: {rule.condition}")
        print(f"  Treatment: {rule.treatment}")
        print(f"  Covered individuals: {len(rule.covered_indices)}")
        print(f"  Covered protected individuals: {len(rule.covered_protected_indices)}")
        print(f"  Utility: {rule.utility:.2f}")
        print(f"  Protected utility: {rule.protected_utility:.2f}")
        print()


if __name__ == "__main__":
    main()