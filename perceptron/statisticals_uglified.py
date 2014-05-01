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

    @staticmethod
    def _partition(lst, n):  # http://stackoverflow.com/a/2660034
        """
        @description: partition a list into N parts and return it
        """
        division = len(lst) / float(n)
        return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n)]

    def _normal_folds_cross(self, n=10):
        """
        @description: Non-stratified cross fold validation
        """
        p = self.perceptron  # alias
        instances = p.training_data
        shuffle(instances)  # shuffle the data
        if len(instances) < n:
            raise Exception("Cannot cross validate. Not enough training data")

        folds = self._partition(instances, n)
        res = [None] * n

        for i in xrange(0, n):  # For each fold
            print "Calculating fold %d" % (i+1)
            res[i] = []
            data = []
            for j in xrange(0, n):  # Create training set
                if i == j:
                    continue
                data = data + folds[j]
            p.training_data = data  # reset training data
            p.train()
            for item in folds[i]:  # classify each item in non-training set
                score, classified = p.classify(item["weights"])
                res[i].append({"gold": item['class'], "classified": classified})
        return res

    def _stratified_folds_cross(self, n=10):  # TODO - if I have time
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

    def calculate_micro_fscore(self, folds):
        """
        @description: Calculates micro f_score
        @args
            - folds (list): the return of the cross_validation
        """
        true_positives = 0
        false_negatives = 0
        false_positives = 0

        classes = self.perceptron.classes

        for f in folds:  # for each fold
            for c in classes:  # for each class
                for item in f:  # for each item in the fold
                    if item['classified'] == c:  # classifier has said C
                        if item['gold'] == c:  # correct classification
                            true_positives += 1
                        else:  # classifier mistakes as C
                            false_positives += 1
                    elif item['gold'] == c:  # gold is C but not classifier
                        false_negatives += 1

        print true_positives, false_negatives, false_positives
        precision = float(true_positives)/(true_positives + false_positives)
        recall = float(true_positives)/(true_positives + false_negatives)
        f_score = (2.0 * precision * recall)/(precision + recall)

        return precision, recall, f_score

    def calculate_macro_fscore(self):  # TODO - if I have time
        pass
