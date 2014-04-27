from abc import ABCMeta, abstractmethod
from . import database
import traceback


class Perceptron(object):
    """
    @description: Base perceptron class
    @type - Abstract Class
    """

    __metaclass__ = ABCMeta

    def __init__(self, db="perceptron"):
        self.db = db  # relative location of database
        self.base_weight = float(0.0)
        self.iterations = 1
        self.weights = {}
        self.features = []
        self.classes = []
        self.training_data_count = {}

    @staticmethod
    def load_from_db(db_name):
        """
        @description: Create the perceptron model from an existing database
        """
        load_perceptron_details()
        load_features()
        load_classes()
        load_weights()
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
                    self.training_data_count[k] = 0
        elif type(klass) is str:
            if klass not in self.features:
                self.classes.append(klass)
                self.training_data_count[klass] = 0

    def add_training_data(self, klass, training_data_set):
        # Validation
        if klass not in self.weights.keys():
            raise Exception("Undefined class")
        if not set(self.features) == set(training_data_set.keys()):
            raise Exception("incorrect weight features provided")

        database._insert_training_data(self.db, klass, training_data_set)
        self.training_data_count[klass] += 1

    def update_weight(self, klass, weight_set):
        """
        @description: Update one class weight set in the perceptron model
                      and in the database
        """

        # Validation
        if klass not in self.weights.keys():
            raise Exception("Undefined class")
        if not set(self.features) == set(weight_set.keys()):
            raise Exception("incorrect weight features provided")

        # Updates
        self.weights[klass] = weight_set  # set the weights for the model
        database.update_weights(self.db, klass, weight_set)
        return True

    def set_iterations(self, iterations=1):
        """
        @description: set the number of iterations to run through training data
        """
        if iterations <= 0:
            raise Exception("Iterations must be minimum 1.")
        self.iterations = iterations

    def reset_weights(self):
        self.weights = {}
        self.initialise_weights()
        data_set = {}
        for f in self.features:
            data_set[f] = self.base_weight
        for c in self.classes:
            database.update_weights(self.db, c, data_set)
        return True

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
                temp_weight[f] = self.base_weight
            self.weights[c] = temp_weight

    def add_historical_weight(self, training_data_id, klass, feature_data_set):
        """
        @description: Add a historical weight value into the database
        """

        # Validation
        if klass not in self.weights.keys():
            raise Exception("Undefined class")
        if not set(self.features) == set(feature_data_set.keys()):
            raise Exception("incorrect weight features provided")

        database._insert_historical_weights(self.db, klass, training_data_id, feature_data_set)
        return True

    def reset_historical_weights(self):
        database.delete_historical_weights(self.db)
        return True

    def add_classifier_data(self, predicted_class, feature_data_set):
        """
        @description: Add user input classifier data into db
        """

        # Validation
        if predicted_class not in self.weights.keys():
            raise Exception("Undefined class")
        if not set(self.features) == set(feature_data_set.keys()):
            raise Exception("incorrect weight features provided")

        database._insert_classification_data(self.db, predicted_class, feature_data_set)
        return True

    def update_training_weights(self, expected, output, data):
        """
        @description: Update the weights to nudge the model towards a better
                      classifier
        """
        expected_weights = self.weights[expected]
        output_weights = self.weights[output]
        new_expected = {}
        new_output = {}

        # Perform calculations
        for f in self.features:
            new_expected[f] = expected_weights[f] + data[f]
            new_output[f] = output_weights[f] - data[f]

        # Update model weights
        self.weights[expected] = new_expected
        self.weights[output] = new_output

        # change weights in DB
        self.update_weight(output, new_output)
        self.update_weight(expected, new_expected)

        return True

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
        print self.db
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
            print traceback.print_exc()
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
                if not database._insert_weights(self.db, c, self.weights[c]):
                    raise Exception()
        except:
            print "Error during data insertion. Deleting database."
            print traceback.print_exc()
            try:
                database.destroy_db(self.db)
            except:
                pass
            return False

        try:  # Insert training data
            if not training_data:
                pass
            for data in training_data:
                try:
                    self.add_training_data(data['class'], data['feature_vector'])
                except:
                    print "error processing training data row. skipping"
                    pass
        except:
            print "Error during training data insertion. Skipping."
            print traceback.print_exc()
            return False

        return True

    def train(self, averaged=True, reset_data=False):
        """
        @description: train the perceptron with training data provided
        @args:
            -averaged (bool) - perform averaging after training?
        """

        if reset_data:  # in case that the perceptron has stale data
            self.reset_weights()
            self.reset_historical_weights()

        # Get training data ids from db
        training_ids = database.get_training_data_ids(self.db)

        # Initialise variables and alias variables
        iterations = self.iterations
        weights = self.weights

        # Iterate through iterations and training data
        for i in range(0, iterations):
            for id in training_ids:
                # Retrieve the training data item
                training_data, expected_class = database.get_training_data(self.db, id)
                if not training_data or expected_class:
                    raise Exception("Error during training data retrieval. Aborting.")

                # Classify
                output_class = self.classify(training_data)  # TODO

                # Check classification and update weights
                if output_class is not expected_class:
                    self.update_training_weights(expected_class, output_class, training_data)
                    self.add_historical_weight(id, output_class, weights[output_class])

                self.add_historical_weight(id, expected_class, weights[expected_class])

        # Perform averaging
        if averaged:
            self.calculate_averaged_weights()  # TODO

        return True

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
