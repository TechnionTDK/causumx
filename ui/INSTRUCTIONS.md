Think about how to implement the following algorithm:

Files:

greedy.py - The main algorithm file
Algorithms.py - getHighTreatment, No need for getHighLowTreatments (refactoring of this function is needed for the greedy algorithm, we get only getting the high treatments, no need for low treatments)

Utils.py - estimateATE (we need to filter only for the records we need), getTreatmentCATE)

Algorithm Overview:
1. Use Apriori for getting grouping patterns
2. for each grouping pattern
1. find the treatment with the highest unfairness score, which the fairness score is calculated as follows. This is done in a greedy way.
1. fairness score = CATE / | CATE - CATE_p|
1. if CATE = CATE_p => unfairness score = CATE
2. Greedy algorithm that choose the best rule (rule = grouping pattern + treatment pattern)
1. Highest CATE
2. Highest unfairness score
3. Highest coverage + protected coverage (only look at the marginal score)
1. Coverage of protected and unprotected groups
1. This is a marginal coverage - כמה מכסה לי שלא כוסו עד כה
2. כמה אנחנו מוסיפים לcoverage בהינתן מה שבחרנו בצעד הקודם
2. Unfairness score (what we calculated in the treatment)
1. \text{benefit}(r) = 
2. \begin{cases} 
3. \frac{\text{utility}(r)}{\tau - \text{utility}_{p}(r)}, & \text{if } \tau \ge \text{utility}_{p}(r) \\
4. \text{utility}(r), & \text{otherwise}
5. \end{cases} 
6. \]
3. statistical parity fairness
1. Let \( U_{r \in R} \text{coverage}(r) \), the increase in outcome (or in other words, utility) should be almost the same as that of a sampled individual from the unprotected group. This is the same intuition as that of SP for classification.
2. 
3. The expected utility of a randomly sampled individual from a protected group is:
4. 
5. \[ \frac{\text{coverage}_p(r)}{|\text{Coverage}(R)_p|} \cdot \text{utility}_p(r) \]
6. 
7. where \( \text{Coverage}(R)_p \) is the set of individuals in the protected group within the coverage of all rules \( r \in R \). Therefore, the SP group fairness constraint is:
8. \[ \left| \sum_{r} \left( \frac{\text{coverage}_p(r)}{|\text{coverage}(R)_p|} \cdot \text{utility}_p(r) - \frac{\text{coverage}_p(r)}{|\text{coverage}(R)_{\bar{p}}|} \cdot \text{utility}_{\bar{p}}(r) \right) \right| \leq \epsilon \]
4. 
4. Every time choose the rule that maximizes this value.
5. Normalize this values because each of these numbers are in different scale
6. 
7. K iterations for getting K rules.
3. Then we calculate this:
1. \[ \left| \sum_r \left( \frac{\text{coverage}_{p}(r)}{|\text{coverage}(R)_p|} \cdot \text{utility}_{p}(r) - \frac{\text{coverage}_{p}(r)}{|\text{coverage}(R)_{\overline{p}}|} \cdot \text{utility}_{p}(r) \right) \right| \leq \epsilon \]
4. 
* We try to see how much the greedy algo is far from the real algorithm, how much we are far from the fairness constraint.
TODO: Maybe a normalization step? As those numbers are not on a similar scale.
Currently, the unfairness_score and coverage_factor are in different scales
The scoring function for a rule could be: score = (utility_protected + utility_unprotected) * unfairness_score * coverage_factor
Where:
* overlap_factor is the proportion of individuals already covered by previously selected rules
* fairness_factor penalizes rules that increase the difference in utility between protected and unprotected groups
* coverage_factor rewards rules that cover more individuals, especially from the protected group

Example: choosing the best treatment pattern for a given grouping pattern:
p1: CATE = 100, CATE_p (protected) = 50 -> score = 100/(100 - 50) = 2
p2: CATE = 80, CATE_p = 70 -> score = 80/(80 - 70) = 8
p3: CATE = 30, CATE_p = 60 -> score = |30/(30 - 60)| (always do absolute value) = 1
p4: CATE = 80, CATE_p = 80 -> score = 80 (we cannot divide by 0 so we will leave the CATE only -> Score == CATE)
The best treatment pattern is p4 and the second best is p2

Example: choosing the next best rule
r1: coverage = 100, coverage_p = 20, score = 4 -> utility: 100*20*4
r2: coverage = 80

Remove the overlap objectives from the problem definition.