import Utils
import warnings
import Algorithms
import time
import json

warnings.filterwarnings('ignore')
PATH = "./data/"

APRIORI = 0.1

def cauSumX(df, DAG, ordinal_atts, targetClass, groupingAtt, fds, k, tau, actionable_atts, high, low,
            print_times=False):
    df = df.dropna()
    # num of groups in the aggregated view
    m = len(df.groupby([groupingAtt]))

    result = {}

    # step 1 - Apriori algorithm
    if print_times:
        start_time = time.time()
    groups = Algorithms.getAllGroups(df, fds, APRIORI)

    result['initial_group_count'] = len(groups)
    groups = Algorithms.filterPatterns(df, groupingAtt, groups)
    result['filtered_group_count'] = len(groups)

    if print_times:
        elapsed_time = time.time() - start_time
        result['step_1_time'] = elapsed_time

    groups_dic, t2 = Algorithms.getGroupstreatments(DAG, df, groupingAtt, groups, ordinal_atts,
                                                    targetClass, high, low, actionable_atts, print_times)
    result['step_2_time'] = t2

    # step 3
    start_time = time.time()

    groups = {}
    weights = {}
    for group in groups_dic:
        groups[group] = list(groups_dic[group][1])  # Convert set to list
        weights[group] = groups_dic[group][6]
    sol = Utils.LP_solver(groups, weights, tau, k, m)

    solution_details = []
    exp = 0
    coverage = set()
    for s in sol:
        e = groups_dic[s][6]
        exp += e
        coverage.update(groups_dic[s][1])
        solution_details.append({
            'group': s,
            'details': {
                'size': groups_dic[s][0],
                'covered': list(groups_dic[s][1]),  # Convert set to list
                't_h': groups_dic[s][2],
                'cate_h': groups_dic[s][3],
                't_l': groups_dic[s][4],
                'cate_l': groups_dic[s][5],
                'explainability': groups_dic[s][6]
            }
        })

    result['solution_details'] = solution_details
    result['overall_explainability'] = exp
    result['coverage'] = len(coverage) / m
    result['total_groups'] = len(coverage)
    result['total_groups_in_aggregated_view'] = m
    result['target_class'] = targetClass

    if print_times:
        elapsed_time = time.time() - start_time
        result['step_3_time'] = elapsed_time
        result['total_time'] = result.get('step_1_time', 0) + t2 + elapsed_time

    return json.dumps(result, indent=4)