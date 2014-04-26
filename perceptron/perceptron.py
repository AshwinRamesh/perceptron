from abc import ABCMeta, abstractmethod
import numpy as np
from . import database


class Perceptron(object):
    """
    @description: Abstract class defining a Perceptron model
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = "Perceptron"
        self.iterations = 1
        self.weights = {}
        self.features = []
        self.classes = []

    def _add_feature_set(self, feature_set):
        """
        @description: add a set of features
        @args:
            - featureset - the array set of features
        """
        for feature in feature_set:
            if feature not in self.features:
                self.features.append(feature)

    def add_feature(self, feature):
        """
        @description: adds a feature to the set of features
        """
        if feature not in self.features:
            self.features.append(feature)
        raise Exception()

    def _add_class_set(self, class_set):
        for klass in class_set:
            if klass not in self.classes:
                self.classes.append(klass)

    def add_class(self, class_name):
        """
        @description: adds a class to the set of classes
        """
        if class_name not in self.classes:
            self.classes.append(class_name)
        raise Exception()

    def _initialise_weights(self):
        """
        @description: initialises the weights
        """
        print "hellogdsg"
        self.weights = [0] * len(self.features)

    @abstractmethod
    def train(self):
        pass


class AveragedPerceptron(Perceptron):
    """
    @description: Averaged Perceptrion implementation
    @args:
        - Features: a vector of size N which describes a given input
        - Classes: a string which represents the output of a given feature set
    """

    @staticmethod
    def load_perceptron_from_db(perceptron_name):
        """
        @description: load a perceptron from a given sqlite database
        """
        return AveragedPerceptron()
        pass  # TODO

    def __init__(self, name="Perceptron", iterations=1):
        parent = super(AveragedPerceptron, self)
        parent.__init__()
        self.name = name
        self.training_data_count = 0
        self.history = []  # historical weights after each iteration
        self.iterations = iterations

    @staticmethod
    def create(name, features, classes, iterations=1):
        """
        returns a new perceptron model to use
        """
        if iterations < 1:
            raise Exception("Iterations must be >= 1")

        if database.create_db(name):  # create perceptron database
            pass
        else:
            return False

        if database.create_tables(name, classes, features, iterations):
            pass
        else:
            return False

        p = AveragedPerceptron(name=name, iterations=iterations)
        p._add_feature_set(features)
        p._add_class_set(classes)
        p._initialise_weights()

        return p

    def add_training_data(self, data):
        self.training_data_count += 1
        database.add_training_data(self.name, data)
        return True

    def _initialise_weights(self):
        """
         need to have classes and features defined before calling this function
        """
        for klass in self.classes:
            print klass
            self.weights[klass] = np.zeros(len(self.features))

    def _initialise_history(self):
        self.history = {}
        i = self.iterations
        for klass in self.classes:
            self.history[klass] = [None] * i

    def train(self, training_data, do_validation=True):
        """
        @description: train the perceptron with training data provided
        @args: training_data -> array of dicts
            dict representation example: {"feature_vector": [1,0,1,1], "class": "Dog"}
        """

        if do_validation:
            self.validate_data(training_data)  # this is done before the perceptron is trained so that any data errors can be computed early.

        weights = self.weights
        history = self.history

        for i in range[0:self.iterations]:
            # TODO - randomise the training data order
            for data in training_data:
                klass = training_data["class"]  # class
                v = training_data["feature_vector"]  # vector
                res = self.classify(weights, v)
                if res is not klass:  # the correct class != the predicted class

                    pass
                    # TODO - do vector shit here
                #TODO - save the weight to vi
        # TODO - calculate avg

    def classify(self, feature_vector):
        """
        @description: sum the feature vector against the Perceptron weights to
        classify the vector
        @feature_vector - dict e.g. {"featureA": 0, "featureB": 1 ..}
        """
        best = -np.inf
        best_class = None
        weights = self.weights
        for c in self.classes:
            score = 0.0
            for feature in feature_vector.keys():
                score += feature_vector[feature] * weights[c][feature]
            if score > best:
                best = score
                best_class = c
        return best, best_class

    def predict(self, feature_vector):
        """
        @description: Given a feature vector that complies with the given perceptron model,
         the ML classifier will attempt to correctly predict the class of the vector.
        """
        pass
