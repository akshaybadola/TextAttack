# Author: Brahmani Nutakki
# Modification of beam search


"""
Basic Greedy Search
=================
"""
from textattack.search_methods import SearchMethod
import numpy as np


class BasicGreedySearch(SearchMethod):

    def perform_search(self, initial_result):
        beam = [initial_result.attacked_text]
        best_result = initial_result
        potential_next_beam = []

        for text in beam:
            transformations = self.get_transformations(
                text, original_text=initial_result.attacked_text
            )
            potential_next_beam += transformations

        if len(potential_next_beam) == 0:
            # If we did not find any possible perturbations, give up.
            return initial_result

        results, search_over = self.get_goal_results(potential_next_beam)
        scores = np.array([r.score for r in results])
        best_result = results[scores.argmax()]

        return best_result

    def is_black_box(self):
        return True
