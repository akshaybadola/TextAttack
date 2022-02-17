# Modified by Brahmani Nutakki. Added probability metrics

"""

Metrics on perturbed words
---------------------------------------------------------------------

"""

import numpy as np

from textattack.attack_results import FailedAttackResult, SkippedAttackResult
from textattack.metrics import Metric


class WordsPerturbed(Metric):
    def __init__(self):
        self.total_attacks = 0
        self.all_num_words = None
        self.perturbed_word_percentages = None
        self.num_words_changed_until_success = 0
        self.max_succ_prob = 0
        self.min_succ_prob = 0
        self.avg_succ_prob = 0
        self.all_metrics = {}

    def calculate(self, results):
        """Calculates all metrics related to perturbed words in an attack.

        Args:
            results (``AttackResult`` objects):
                Attack results for each instance in dataset
        """

        self.results = results
        self.total_attacks = len(self.results)
        self.all_num_words = np.zeros(len(self.results))
        self.perturbed_word_percentages = np.zeros(len(self.results))
        self.num_words_changed_until_success = np.zeros(2 ** 16)
        self.max_words_changed = 0
        self.avg_succ_prob_skip = 0
        temp_count = 0
        label_shift_count = np.zeros(6).tolist()
        label_shift_prob = np.zeros(6).tolist()
        skip_label_count = np.zeros(3).tolist()

        for i, result in enumerate(self.results):
            self.all_num_words[i] = len(result.original_result.attacked_text.words)

            if isinstance(result, SkippedAttackResult):
                if result.perturbed_result.ground_truth_output == 0:
                    skip_label_count[0] += 1
                elif result.perturbed_result.ground_truth_output == 1:
                    skip_label_count[1] += 1
                elif result.perturbed_result.ground_truth_output == 2:
                    skip_label_count[2] += 1
            else:
                temp_prob = result.perturbed_result.succ_transformations / result.perturbed_result.total_transformations
                self.avg_succ_prob_skip += temp_prob

                if result.perturbed_result.ground_truth_output == 0 and result.perturbed_result.output == 1:
                    label_shift_prob[0] += temp_prob
                    label_shift_count[0] += 1
                elif result.perturbed_result.ground_truth_output == 0 and result.perturbed_result.output == 2:
                    label_shift_prob[1] += temp_prob
                    label_shift_count[1] += 1
                elif result.perturbed_result.ground_truth_output == 1 and result.perturbed_result.output == 0:
                    label_shift_prob[2] += temp_prob
                    label_shift_count[2] += 1
                elif result.perturbed_result.ground_truth_output == 1 and result.perturbed_result.output == 2:
                    label_shift_prob[3] += temp_prob
                    label_shift_count[3] += 1
                elif result.perturbed_result.ground_truth_output == 2 and result.perturbed_result.output == 0:
                    label_shift_prob[4] += temp_prob
                    label_shift_count[4] += 1
                elif result.perturbed_result.ground_truth_output == 2 and result.perturbed_result.output == 1:
                    label_shift_prob[5] += temp_prob
                    label_shift_count[5] += 1
                temp_count += 1

            if isinstance(result, FailedAttackResult) or isinstance(
                result, SkippedAttackResult
            ):
                continue

            num_words_changed = len(
                result.original_result.attacked_text.all_words_diff(
                    result.perturbed_result.attacked_text
                )
            )
            self.num_words_changed_until_success[num_words_changed - 1] += 1
            self.max_words_changed = max(
                self.max_words_changed or num_words_changed, num_words_changed
            )
            if len(result.original_result.attacked_text.words) > 0:
                perturbed_word_percentage = (
                    num_words_changed
                    * 100.0
                    / len(result.original_result.attacked_text.words)
                )
            else:
                perturbed_word_percentage = 0

            self.perturbed_word_percentages[i] = perturbed_word_percentage

        self.all_metrics["avg_word_perturbed"] = self.avg_number_word_perturbed_num()
        self.all_metrics["avg_word_perturbed_perc"] = self.avg_perturbation_perc()
        self.all_metrics["max_words_changed"] = self.max_words_changed
        self.all_metrics[
            "num_words_changed_until_success"
        ] = self.num_words_changed_until_success

        self.all_metrics["avg_succ_prob_skip"] = (self.avg_succ_prob_skip + self.total_attacks - temp_count) / self.total_attacks
        self.all_metrics["avg_succ_prob"] = self.avg_succ_prob_skip / temp_count

        self.all_metrics["avg_prob_con_ent"] = self.check_count(label_shift_prob[0], label_shift_count[0])
        self.all_metrics["avg_prob_con_neu"] = self.check_count(label_shift_prob[1], label_shift_count[1])
        self.all_metrics["avg_prob_ent_con"] = self.check_count(label_shift_prob[2], label_shift_count[2])
        self.all_metrics["avg_prob_ent_neu"] = self.check_count(label_shift_prob[3], label_shift_count[3])
        self.all_metrics["avg_prob_neu_con"] = self.check_count(label_shift_prob[4], label_shift_count[4])
        self.all_metrics["avg_prob_neu_ent"] = self.check_count(label_shift_prob[5], label_shift_count[5])
        self.all_metrics["skip_con"] = skip_label_count[0]
        self.all_metrics["skip_ent"] = skip_label_count[1]
        self.all_metrics["skip_neu"] = skip_label_count[2]

        return self.all_metrics

    def avg_number_word_perturbed_num(self):
        average_num_words = self.all_num_words.mean()
        average_num_words = round(average_num_words, 2)
        return average_num_words

    def avg_perturbation_perc(self):
        self.perturbed_word_percentages = self.perturbed_word_percentages[
            self.perturbed_word_percentages >= 0
        ]
        average_perc_words_perturbed = self.perturbed_word_percentages.mean()
        average_perc_words_perturbed = round(average_perc_words_perturbed, 2)
        return average_perc_words_perturbed

    def check_count(self, prob, count):
        if count == 0:
            return 0
        else:
            return prob / count
