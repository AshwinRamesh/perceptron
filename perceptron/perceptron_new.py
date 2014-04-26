from abc import ABCMeta, abstractmethod
from . import database


class Perceptron(object):
    """
    @description: Base perceptron class
    @type - Abstract Class
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.db = "perceptron"  # relative location of database
        self.iterations = 1
        self.weights = []
        self.features = []
        self.classes = []

    @staticmethod
    def load_from_db(db_name):
        """
        @description: Create the perceptron model from an existing database
        """
        pass

    def add_feature(self, feature):
        """
        @description: add feature(s) to the perceptron
        """
        if type(feature) is list:
            for f in feature:
                if f not in self.features:
                    self.features.append(f)
        elif type(feature) is str:
            if feature not in self.features:
                self.features.append(feature)

    def add_class(self, klass):
        """
        @description: add class(es) to the perceptron
        """
        if type(klass) is list:
            for k in klass:
                if k not in self.features:
                    self.classes.append(k)
        elif type(klass) is str:
            if klass not in self.features:
                self.classes.append(klass)

    def set_iterations(self, iterations=1):
        """
        @description: set the number of iterations to run through training data
        """
        if iterations <= 0:
            raise Exception("Iterations must be minimum 1.")
        self.iterations = iterations





    @abstractmethod
    def initialise_perceptron(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def classify(self):
        pass
