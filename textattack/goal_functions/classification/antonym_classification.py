# Author: Brahmani Nutakki

"""

Determine successful if word replaced by antonym
----------------------------------------------------
"""


from .classification_goal_function import ClassificationGoalFunction


class AntonymClassification(ClassificationGoalFunction):

    """
    def __init__(self, *args, target_max_score=None, **kwargs):
        self.target_max_score = target_max_score
        super().__init__(*args, **kwargs)
    """

    def _is_goal_complete(self, model_output, _):
        status = True
        if self.ground_truth_output == 0 and model_output.argmax() == 1:
            status = False
        elif self.ground_truth_output == 1 and model_output.argmax() == 0:
            status = False
        elif self.ground_truth_output == 2 and model_output.argmax() == 2:
            status = False
        elif self.ground_truth_output == model_output.argmax():
            status = False
        return status

    def _get_score(self, model_output, _):
        if self.ground_truth_output == 0:
            return model_output[1]
        elif self.ground_truth_output == 1:
            return model_output[0]
        else:
            return model_output[2]
