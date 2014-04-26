from abc import ABCMeta, abstractmethod
from . import database


class Perceptron(object):
    """
    @description: Base perceptron class
    @type - Abstract Class
    """

    __metaclass__ = ABCMeta

    def __init__(self, db="perceptron"):
        self.db = db  # relative location of database
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

    def update_weight(self, klass, weight_set):
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

    def __init__(self, db):
        parent = super(AveragedPerceptron, self)
        parent.__init__(db)

    def initialise_perceptron(self, classes, features, iterations=1, training_data=None):
        """
        @description: Initialise the perceptron with data and write to db
            - will set classes/features/iterations
            - if training data is provided, it will write the data to the DB
        """
        if database.create_db(self.db):
            print "Database %s.db created" % self.db
        else:
            return False

        # Set the details for the actual object
        self.set_iterations(iterations)
        self.add_class(classes)
        self.add_feature(features)
        self.initialise_weights()

        try:  # create tables  - change this later to massive if and TODO
            if not database._create_perceptron_details_table(self.db):
                raise Exception()
            if not database._create_classes_table(self.db):
                raise Exception()
            if not database._create_features_table(self.db):
                raise Exception()
            if not database._create_training_datas_table(self.db, self.features):
                raise Exception()
            if not database._create_weights_table(self.db, self.features):
                raise Exception()
            if not database._create_historical_weights_table(self.db, self.features):
                raise Exception()
            if not database._create_classification_data_table(self.db, self.features):
                raise Exception()
        except:
            print "Error during table creation. Deleting database."
            try:
                database.destroy_db(self.db)
            except:
                pass
            return False

        try:  # insert initial data into tables
            if not database._insert_perceptron_details(self.db, self.iterations):
                raise Exception()
            if not database._insert_classes(self.db, self.classes):
                raise Exception()
            if not database._insert_features(self.db, self.features):
                raise Exception()
            for c in self.weights.keys():
                if not database._insert_weights(c, self.weights[c]):
                    raise Exception()
        except:
            print "Error during data insertion. Deleting database."
            try:
                database.destroy_db(self.db)
            except:
                pass
            return False

        return True

    def train(self):
        pass  # TODO

    def classify(self, feature_data_set):  # TODO - test this
        """
        @description: sum the feature vector against the Perceptron weights to
        classify the vector
        @feature_vector - dict e.g. {"featureA": 0, "featureB": 1 ..}
        """
        best = -100000000.0
        best_class = None
        weights = self.weights
        for c in self.classes:
            score = 0.0
            for feature in feature_data_set.keys():
                score += feature_data_set[feature] * weights[c][feature]
            if score > best:
                best = score
                best_class = c
        return best, best_class

    def calculate_averaged_weights(self):
        # TODO
        weight_set = []
        for k in self.classes:
            res = database.get_all_historical_weights_for_class(k)
            weight_set[k] = compute_average_for_class(res)
        return weight_set
