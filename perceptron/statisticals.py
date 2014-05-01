from .perceptron import AveragedPerceptron


class Statisticals(object):
    """
    @description: statistics wrapper around the
    perceptron to calculate various stats.
    """

    def __init__(self, perceptron):
        """
        @args:
            - perceptron (obj): actual fullly loaded perceptron
        """
        self.cross_validations = {}
        pass

    def cross_validation(self, n=10, equal_folds=False):
        """
        @description: performs cross fold validation
        on the perceptron
        @args:
            n (int) - number of folds
            equal_folds (bool) - all folds have an approx.
                equal representation of each class
        """

        pass

    def calculate_micro_fscore(self):
        pass

    def calculate_macro_fscore(self):
        pass
