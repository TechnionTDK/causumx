import pandas as pd
import numpy as np
from typing import List, Set


class Rule:
    def __init__(self, condition: str, treatment: str, covered_indices: Set[int],
                 covered_protected_indices: Set[int], utility: float, protected_utility: float):
        self.condition = condition
        self.treatment = treatment
        self.covered_indices = covered_indices
        self.covered_protected_indices = covered_protected_indices
        self.utility = utility
        self.protected_utility = protected_utility


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def get_grouping_patterns(complete this function):
    # TODO: add this - Use Apriori for getting grouping patterns
    # def cauSumX(df, DAG, ordinal_atts, targetClass, groupingAtt, fds, k, tau, actionable_atts, high, low,
    #             print_times=False):
    #     df = df.dropna()
    #     # num of groups in the aggregated view
    #     m = len(df.groupby([groupingAtt]))
    #
    #     result = {}
    #
    #     # step 1 - Apriori algorithm
    #     if print_times:
    #         start_time = time.time()
    #     groups = Algorithms.getAllGroups(df, fds, APRIORI)


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

    return (protected_utility_increase + utility_increase) * (1 - overlap_factor) * fairness_factor * coverage_factor


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
    # Load data
    df = load_data('../ui/data/so_countries_col_new.csv')

    # Define protected group (non-male in this case)
    protected_group = set(df[df['Gender'] != 'Male'].index)

    # Get the Grouping Patterns
    grouping_patterns = get_grouping_patterns()



if __name__ == "__main__":
    main()