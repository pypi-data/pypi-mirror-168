from __future__ import annotations

import logging
import re
from typing import Dict, List, Tuple

import pandas
import sklearn
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from tqdm import tqdm

from te2rules.adapter import (
    ScikitGradientBoostingClassifierAdapter,
    ScikitRandomForestClassifierAdapter,
)
from te2rules.rule import Rule
from te2rules.tree import RandomForest

log = logging.getLogger()


class ModelExplainer:
    """
    The :mod:`te2rules.explainer.ModelExplainer` module explains
    Tree Ensemble models (TE) like XGBoost, Random Forest, trained
    on a binary classification task, using a rule list. The algorithm used by TE2Rules
    is based on Apriori Rule Mining.
    For more details on the algorithm, please check out our paper
    `TE2Rules: Extracting Rule Lists from Tree Ensembles
    <https://arxiv.org/abs/2206.14359/>`_.
    """

    def __init__(
        self, model: sklearn.ensemble, feature_names: List[str], verbose: bool = False
    ):
        """
        Initialize the explainer with the trained tree ensemble model
        and feature names used by the model.

        Returns a ModelExplainer object

        Parameters
        ----------
        model: sklearn.ensemble.GradientBoostingClassifier or \
            sklearn.ensemble.RandomForestClassifier
            The trained Tree Ensemble model to be explained.
            The model is expected to be a binary classifier.
        feature_name: List[str]
            List of feature names used by the `model`. Only alphanumeric characters and
            underscores are allowed in feature names.
        verbose: bool, optional
            Optional boolean value to give more insights on the running of the
            explanation algorithm.
            Default = False

        Returns
        -------
        self: te2rules.explainer.ModelExplainer
            A ModelExplainer object initialized with the model to be explained.

        Raises
        ------
        ValueError:
            when `model` is not a supported Tree Ensemble Model.
            Currently, only Scikit Learn's GradientBoostingClassifier and
            RandomForestClassifier are supported.

        ValueError:
            when `feature_name` list contains a name that has any character other
            than alphanumeric characters or underscore.

        Warning
        ------
        The implementation works fine with scikit learn's GradientBoostingClassifier.
        For now, we are still testing the case when the `model` is scikit learn's
        RandomForestClassifier.
        """
        if verbose is True:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(format="%(message)s")

        if isinstance(model, GradientBoostingClassifier):
            self.random_forest = ScikitGradientBoostingClassifierAdapter(
                model, feature_names
            ).random_forest
        elif isinstance(model, RandomForestClassifier):
            self.random_forest = ScikitRandomForestClassifierAdapter(
                model, feature_names
            ).random_forest
        else:
            raise ValueError(
                "Only GradientBoostingClassifier and RandomForestClassifier "
                + "are supported. But received "
                + str(type(model))
            )
        for f in feature_names:
            if re.search("[^a-zA-Z0-9_]", f):
                raise ValueError(
                    "Only alphanumeric characters and underscores are allowed "
                    + "in feature names. But found feature name: "
                    + str(f)
                )

    def explain(
        self,
        X: List[List[float]],
        y: List[int],
        num_stages: int = None,
        min_precision: float = 0.95,
    ) -> List[str]:
        """
        A method to extract rule list from the tree ensemble model.
        This method takes in input features used by the model and predicted class
        output by the model.

        Returns a List of rule strings.

        Parameters
        ----------
        X: 2d np.array
            2 dimensional input data used by the `model`
        y: 1d np.array
            1 dimensional model class predictions (0 or 1) from the `model`
        num_stages: int, optional
            The algorithm runs in stages starting from stage 1, stage 2 to all the way
            till stage n where n is the number of trees in the ensemble.
            Stopping the algorithm at an early stage  results in a few short rules
            (with quicker run time, but less coverage in data). By default,
            the algorithm explores all stages before terminating.
        min_precision: float, optional
            This paramter controls the minimum precision of extracted rules.
            Setting it to a smaller threhsold, allows extracting shorter
            (more interpretable, but less faithful) rules.
            By default, the algorithm uses a minimum precision threshold of 0.95.

        Returns
        -------
        rules: List[str]
            A List of human readable rules.

        Raises
        ------
        ValueError:
            when `X` and `y` are of different length.

        ValueError:
            when entries in `y` are other than 0 and 1. Only binary
            classification is supported.

        Notes
        -----
        The data is used for extracting rules with relevant
        combination of input features. Without data, explainer would need
        to extract rules for all possible combinations of input features,
        including those combinations which are extremely rare in the data.

        Examples
        --------
        >>> from te2rules.explainer import ModelExplainer
        >>> model_explainer = ModelExplainer(model=model, feature_names=feature_names)
        >>> rules = model_explainer.explain(X=x_train, y=y_train_pred)
        """

        self.rule_builder = RuleBuilder(
            random_forest=self.random_forest,
            num_stages=num_stages,
            min_precision=min_precision,
        )
        if len(X) != len(y):
            raise ValueError("X and y should have the same length")
        for i in range(len(y)):
            if y[i] not in [0, 1]:
                raise ValueError("entries y should only be 0 or 1.")
        rules = self.rule_builder.explain(X, y)
        rules_as_str = [str(r) for r in rules]
        return rules_as_str

    def _apply(self, df: pandas.DataFrame) -> List[float]:
        return self.rule_builder.apply(df)

    def get_fidelity(
        self,
    ) -> Tuple[float, float, float]:
        """
        A method to evaluate the rule list extracted by the `explain` method

        Returns a fidelity on positives, negative, overall

        Parameters
        ----------

        Returns
        -------
        fidelity: [float, float, float]
            Fidelity is the fraction of data for which the rule list agrees
            with the tree ensemble. Returns the fidelity on overall data,
            positive predictions and negative predictions by the model.

        Examples
        --------
        >>> (fidelity, fidelity_pos, fidelity_neg) = model_explainer.get_fidelity()
        """

        return self.rule_builder.get_fidelity()


class RuleBuilder:
    def __init__(
        self,
        random_forest: RandomForest,
        num_stages: int = None,
        min_precision: float = 0.95,
    ):
        self.random_forest = random_forest
        # if num_stages not set by user, will set it to the number of trees
        # note that we neednum_stages <= num_trees
        if num_stages is not None:
            self.num_stages = min(num_stages, self.random_forest.get_num_trees())
        else:
            self.num_stages = self.random_forest.get_num_trees()
        self.min_precision = min_precision

    def explain(self, X: List[List[float]], y: List[int]) -> List[Rule]:
        self.data = X
        self.labels = y

        self.positives = []
        for i in range(len(self.labels)):
            if self.labels[i] == 1:
                self.positives.append(i)
        log.info("")
        log.info("Positives: " + str(len(self.positives)))

        log.info("")
        log.info("Rules from trees")
        self.candidate_rules = self.random_forest.get_rules(data=self.data)
        self.solution_rules: List[Rule] = []
        log.info(str(len(self.candidate_rules)) + " candidate rules")

        log.info("Deduping")
        self.candidate_rules = self.deduplicate(self.candidate_rules)
        self.solution_rules = self.deduplicate(self.solution_rules)
        log.info(str(len(self.candidate_rules)) + " candidate rules")

        self.generate_solutions()

        log.info("Simplifying Solutions")
        self.solution_rules = self.shorten(self.solution_rules)
        self.solution_rules = self.deduplicate(self.solution_rules)
        log.info(str(len(self.solution_rules)) + " solutions")

        log.info("")
        log.info("Set Cover")
        total_support: List[int] = []
        for r in self.solution_rules:
            total_support = list(set(total_support).union(set(r.decision_support)))
        self.rules_to_cover_positives(
            list(set(total_support).intersection(set(self.positives)))
        )
        log.info(str(len(self.solution_rules)) + " rules found")

        return self.solution_rules

    def rules_to_cover_positives(self, positives: List[int]) -> None:
        original_rules = {}
        positive_coverage = {}
        for r in self.solution_rules:
            positive_coverage[str(r)] = list(
                set(positives).intersection(set(r.decision_support))
            )
            original_rules[str(r)] = r

        selected_rules: List[Rule] = []
        covered_positives: List[int] = []

        while (len(covered_positives) < len(positives)) and (
            len(selected_rules) < len(self.solution_rules)
        ):
            max_coverage_rule = list(positive_coverage.keys())[0]
            for rule in list(positive_coverage.keys()):
                if len(positive_coverage[rule]) > len(
                    positive_coverage[max_coverage_rule]
                ):
                    max_coverage_rule = rule
                else:
                    if len(positive_coverage[rule]) == len(
                        positive_coverage[max_coverage_rule]
                    ):
                        if len(original_rules[rule].decision_rule) < len(
                            original_rules[max_coverage_rule].decision_rule
                        ):
                            max_coverage_rule = rule

            selected_rules.append(original_rules[max_coverage_rule])
            new_covered_positives = positive_coverage[max_coverage_rule]
            covered_positives = list(
                set(covered_positives).union(set(new_covered_positives))
            )

            for rule in list(positive_coverage.keys()):
                positive_coverage[rule] = list(
                    set(positive_coverage[rule]).difference(set(new_covered_positives))
                )
                if len(positive_coverage[rule]) == 0:
                    positive_coverage.pop(rule)

        self.solution_rules = selected_rules

    def generate_solutions(self) -> None:
        log.info("")
        log.info("Running Apriori")
        log.info("")

        positives_to_explain = self.positives
        for stage in range(self.num_stages):
            if len(positives_to_explain) == 0:
                continue

            log.info("")

            log.info("Rules from " + str(stage + 1) + " trees")

            new_candidates = []
            new_solutions = []
            if stage == 0:
                for i in tqdm(range(len(self.candidate_rules))):
                    r = self.candidate_rules[i]
                    is_solution, keep_candidate = self.filter_candidates(r, self.labels)
                    if is_solution is True:
                        new_solutions.append(r)
                    if keep_candidate is True:
                        new_candidates.append(r)
            else:
                join_indices = self.get_join_indices(self.candidate_rules)
                for (i, j) in tqdm(join_indices):
                    joined_rule = self.candidate_rules[i].join(self.candidate_rules[j])
                    if joined_rule is not None:
                        is_solution, keep_candidate = self.filter_candidates(
                            joined_rule, self.labels
                        )
                        if is_solution is True:
                            new_solutions.append(joined_rule)
                        if keep_candidate is True:
                            new_candidates.append(joined_rule)

            self.candidate_rules = new_candidates
            self.solution_rules = self.solution_rules + new_solutions
            log.info(str(len(self.candidate_rules)) + " candidates")
            log.info(str(len(self.solution_rules)) + " solutions")

            for rule in new_solutions:
                positives_to_explain = list(
                    set(positives_to_explain).difference(set(rule.decision_support))
                )

            log.info("Unexplained Positives")
            log.info(len(positives_to_explain))

            log.info("Pruning Candidates")
            self.candidate_rules = self.prune(
                self.candidate_rules, positives_to_explain
            )
            log.info(str(len(self.candidate_rules)) + " candidates")

            log.info("Deduping")
            self.candidate_rules = self.deduplicate(self.candidate_rules)
            self.solution_rules = self.deduplicate(self.solution_rules)
            log.info(str(len(self.candidate_rules)) + " candidates")
            log.info(str(len(self.solution_rules)) + " solutions")

            fidelity, fidelity_positives, fidelity_negatives = self.get_fidelity()

            log.info("Fidelity")
            log.info(
                "Total: "
                + f"{fidelity:.6f}"
                + ", Positive: "
                + f"{fidelity_positives:.6f}"
                + ", Negative: "
                + f"{fidelity_negatives:.6f}"
            )
            log.info("")

    def score_rule_using_data(self, rule: Rule, labels: List[int]) -> List[int]:
        decision_value = []
        for data_index in rule.decision_support:
            decision_value.append(labels[data_index])
        return decision_value

    """
    def score_rule_using_model(self, rule: Rule) -> Tuple[float, float]:
        min_score, max_score = self.random_forest.get_rule_score(rule.decision_rule)
        return min_score, max_score
    """

    def filter_candidates(self, rule: Rule, labels: List[int]) -> Tuple[bool, bool]:
        scores = self.score_rule_using_data(rule, labels)
        max_score = max(scores)
        avg_score = sum(scores) / len(scores)

        min_precision = avg_score

        if min_precision >= self.min_precision:
            # solution, throw candidate: it is already a solution
            return True, False
        else:
            if max_score == 0:
                # not solution, throw candidate: it cannot become a solution
                return False, False
            else:
                # not solution, keep candidate: it can become a solution
                return False, True

    def get_fidelity(self, use_top: int = None) -> Tuple[float, float, float]:
        if use_top is None:
            use_top = len(self.solution_rules)

        support: List[int] = []
        for i in range(use_top):
            r = self.solution_rules[i]
            support = support + r.decision_support
        support = list(set(support))

        y_pred_rules = [0] * len(self.labels)
        for s in support:
            y_pred_rules[s] = 1

        positives = 0
        fidelity_positives = 0
        negatives = 0
        fidelity_negatives = 0
        for i in range(len(self.labels)):
            if self.labels[i] == 1:
                positives = positives + 1
                if y_pred_rules[i] == self.labels[i]:
                    fidelity_positives = fidelity_positives + 1
            if self.labels[i] == 0:
                negatives = negatives + 1
                if y_pred_rules[i] == self.labels[i]:
                    fidelity_negatives = fidelity_negatives + 1

        return (
            (fidelity_positives + fidelity_negatives) / (positives + negatives),
            fidelity_positives / positives,
            fidelity_negatives / negatives,
        )

    def deduplicate(self, rules: List[Rule]) -> List[Rule]:
        rules_map = {}
        for i in range(len(rules)):
            key = str(rules[i])
            if key not in rules_map:
                rules_map[key] = rules[i]
            else:
                rules_map[key].identity = list(
                    set(rules_map[key].identity).union(set(rules[i].identity))
                )

        dedup_rules = [rules_map[r] for r in rules_map]
        return dedup_rules

    def shorten(self, rules: List[Rule]) -> List[Rule]:
        for i in range(len(rules)):
            pred_dict = {}
            for pred in rules[i].decision_rule:
                f, op, val = pred.split()
                # determine direction of op
                op_type = "equal"
                if op in ("<", "<="):
                    op_type = "less than"
                elif op in (">", ">="):
                    op_type = "greater than"
                # store value if haven't seen (f, op_type)
                if (f, op_type) not in pred_dict:
                    pred_dict[(f, op_type)] = (op, val)
                # otherwise, combine rules
                else:
                    old_op, old_val = pred_dict[(f, op_type)]
                    if (old_op == "<=" and op == "<" and val == old_val) or (
                        old_op == ">=" and op == ">" and val == old_val
                    ):
                        pred_dict[(f, op_type)] = (op, val)
                    elif (op_type == "less than" and val < old_val) or (
                        op_type == "greater than" and val > old_val
                    ):
                        pred_dict[(f, op_type)] = (op, val)
            # make shorter rule from predicate list
            final_rule = []
            for (f, _) in pred_dict:
                op, val = pred_dict[(f, _)]
                final_rule.append((" ").join([f, op, val]))
            rules[i].decision_rule = final_rule
        return rules

    def apply(self, df: pandas.DataFrame) -> List[float]:
        coverage: List[int] = []
        for r in self.solution_rules:
            support = df.query(str(r)).index.tolist()
            coverage = list(set(coverage).union(set(support)))

        y_rules: List[float] = [0.0] * len(df)
        for i in coverage:
            y_rules[i] = 1.0

        return y_rules

    def get_join_indices(self, rules: List[Rule]) -> List[Tuple[int, int]]:
        for i in range(len(rules)):
            rules[i].create_identity_map()

        left_map: Dict[str, List[int]] = {}
        right_map: Dict[str, List[int]] = {}
        for i in range(len(rules)):
            left_keys = list(rules[i].left_identity_map.keys())
            for j in range(len(left_keys)):
                if left_keys[j] not in left_map:
                    left_map[left_keys[j]] = []
                left_map[left_keys[j]].append(i)

            right_keys = list(rules[i].right_identity_map.keys())
            for j in range(len(right_keys)):
                if right_keys[j] not in right_map:
                    right_map[right_keys[j]] = []
                right_map[right_keys[j]].append(i)

        join_keys = list(set(left_map.keys()).intersection(set(right_map.keys())))

        pairs = set()
        for i in range(len(join_keys)):
            for j in left_map[join_keys[i]]:
                for k in right_map[join_keys[i]]:
                    if j < k:
                        pairs.add((j, k))
        pairs_list = list(pairs)
        pairs_list.sort()  # can be removed
        return pairs_list

    def prune(self, rules: List[Rule], positives: List[int]) -> List[Rule]:
        pruned_rules = []
        for i in range(len(rules)):
            decision_support_positive = list(
                set(rules[i].decision_support).intersection(set(positives))
            )

            if len(decision_support_positive) > 0:
                pruned_rules.append(rules[i])

        return pruned_rules
