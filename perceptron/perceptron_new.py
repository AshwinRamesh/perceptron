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

    def add_training_data(self, training_data_set):
        pass  # TODO

    def set_iterations(self, iterations=1):
        """
        @description: set the number of iterations to run through training data
        """
        if iterations <= 0:
            raise Exception("Iterations must be minimum 1.")
        self.iterations = iterations

    def initialise_weights(self):
        """
        @description: initialise the starting weights to 0.
        @note - only call this once all classes and
                features have been set in the perceptron
        """
        if not self.features or len(self.features) == 0:
            raise Exception("Cannot initialise weights. Features not set.")
        if not self.classes or len(self.classes) == 0:
            raise Exception("Cannot initialise weights. Classes not set.")

        for c in self.classes:
            temp_weight = {}
            for f in self.features:
                temp_weight[f] = 0.0
            self.weights[c] = temp_weight

    @abstractmethod
    def initialise_perceptron(self):
        """
        @description: initialises the perceptron in both object and database form
        """
        pass

    @abstractmethod
    def train(self):
        """
        @desciption: Loads all training data from database to train the perceptron.
            Will "retrain" if previously trained
        """
        pass

    @abstractmethod
    def classify(self):
        """
        @description: Will classify a input instance
        """
        pass


class AveragedPerceptron(Perceptron):

    def __init__(self):
        parent = super(AveragedPerceptron, self)
        parent.__init__()

    def initialise_perceptron(self):
        pass  # TODO

    def train(self):
        pass  # TODO

    def classify(self, feature_data_set):
        pass  # TODO

    def calculate_averaged_weights(self):
        # TODO
        weight_set = []
        for k in self.classes:
            res = database.get_all_historical_weights_for_class(k)
            weight_set[k] = compute_average_for_class(res)
        return weight_set
