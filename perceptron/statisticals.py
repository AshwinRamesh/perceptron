from .perceptron import AveragedPerceptron
from random import shuffle


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
        self.perceptron = perceptron
        self.cross_validations = {}
        pass

    @staticmethod
    def _partition(lst, n):  # http://stackoverflow.com/a/2660034
        division = len(lst) / float(n)
        return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n)]

    def _normal_folds_cross(self, n=10):
        p = self.perceptron  # alias
        instances = p.training_data
        shuffle(instances)  # shuffle the data
        if len(instances) < n:
            raise Exception("Cannot cross validate. Not enough training data")

        folds = self.partition(instances, n)
        res = []

        for i in range(0, n):  # For each fold
            res[i] = []
            data = []
            for j in range(0, n):  # Create training set
                if i == j:
                    continue
                    data + folds[i]
            p.training_data = data  # reset training data
            p.train()
            for k in len(folds[i]):  # classify each item in non-training set
                score, classified = p.classify(folds[i][k]["weights"])
                res[i].append({"gold": folds[i][k]['class'], "classified": classified})
        return res

    def _stratified_folds_cross(self, n=10):
        pass

    def cross_validation(self, n=10, stratified=False):
        """
        @description: performs cross fold validation
        on the perceptron
        @args:
            n (int) - number of folds
            equal_folds (bool) - all folds have an approx.
                equal representation of each class
        """
        if stratified:
            return self._equal_folds_cross(n)
        else:
            return self._normal_folds_cross(n)

    def calculate_micro_fscore(self):
        pass

    def calculate_macro_fscore(self):
        pass
