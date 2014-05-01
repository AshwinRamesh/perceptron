import traceback


class AveragedPerceptron(object):
    """
    @description: Averaged perceptron class
    """

    def __init__(self, skip_averaging=False, lazy_update=True, debug=False):
        self.debug = debug  # Show print statements if true
        self.base_weight = float(0.0)
        self.iterations = 1
        self.weights = {}
        self.averaged_weights = {}
        self.features = []
        self.classes = []
        self.training_data = []
        self.skip_averaging = skip_averaging  # Skip averaging
        self.lazy_update = lazy_update  # Use lazy update
        self.historical_weights = {}  # the sum of weights after each train
        self.last_set_weights = {}  # the last weights for each class
        self.historical_trainings = {}  # the number of iterations processed by a class (used for lazy averaging)
        self.num_trainings = 0  # total number of trainings (iterations x training items)

    def add_feature(self, feature, skip_validation=True):
        """
        @description: add feature(s) to the perceptron
        """
        if not skip_validation:
            if type(feature) is list:
                for f in feature:
                    if f not in self.features:
                        self.features.append(f)
            elif type(feature) is str:
                if feature not in self.features:
                    self.features.append(feature)
        else:
            self.features = feature

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

    def add_training_data(self, klass, training_data_set, skip_validation=True):
        """
        @description: Add training data instance into memory
        """
        if not skip_validation:
            if klass not in self.weights.keys():
                raise Exception("Undefined class")
            #if not set(self.features) == set(training_data_set.keys()):
            #    raise Exception("incorrect weight features provided")
        for f in training_data_set.keys():
            training_data_set[f] = float(training_data_set[f])  # Will throw exception if this fails.
        self.training_data.append({"class": klass, "weights": training_data_set})

    def set_iterations(self, iterations=1):
        """
        @description: set the number of iterations to run through training data
        """
        if iterations <= 0:
            raise Exception("Iterations must be minimum 1.")
        self.iterations = iterations

    def initialise_weights(self):
        """
        @description: initialise the starting weights to self.base_weight.
                      initialise the historical weights
        @note - only call this once all classes and
                features have been set in the perceptron
        """
        if not self.features or len(self.features) == 0:
            raise Exception("Cannot initialise weights. Features not set.")
        if not self.classes or len(self.classes) == 0:
            raise Exception("Cannot initialise weights. Classes not set.")

        for c in self.classes:
            temp_weight = {}
            self.historical_trainings[c] = 0
            for f in self.features:
                temp_weight[f] = self.base_weight
            self.weights[c] = dict(temp_weight)
            self.averaged_weights[c] = dict(temp_weight)
            self.historical_weights[c] = dict(temp_weight)
            self.last_set_weights[c] = dict(temp_weight)

    def initialise_perceptron(self, classes, features, iterations=1, training_data=None):
        """
        @description: Initialise the perceptron with data and write to db
            - will set classes/features/iterations
            - if training data is provided, it will write the data to the DB
        """

        # Set the details for the actual object
        self.set_iterations(iterations)
        self.add_class(classes)
        self.add_feature(features)
        self.initialise_weights()

        if training_data:
            try:  # Insert training data
                for data in training_data:
                    try:
                        self.add_training_data(data['class'], data['feature_vector'])
                    except:
                        print "error processing training data row. skipping"
            except:
                print "Error during training data insertion. Skipping."
                print traceback.print_exc()
                return False

        return True

    def lazy_update_historical_weights(self, klass=None):
        """
        @description: Lazy update of historical weights.
        @args:
            - klass (str): if None, will update all classes.
                           is str, will update specified class
        """
        debug = self.debug

        if klass is None:  # Update all classes
            for c in self.classes:
                update_level = self.num_trainings - self.historical_trainings[c]  # Number of updates class is behind by
                if debug:
                    print "Updating Class: %s | Update Backlog: %d | Number Training Items: %d" %(c, update_level, self.num_trainings)
                if update_level >= 0:
                    for f in self.features:
                        self.historical_weights[c][f] += (update_level * self.weights[c][f])
                self.historical_trainings[c] = self.num_trainings
        else:  # Update specified class
            update_level = self.num_trainings - self.historical_trainings[klass] - 1 # Number of updates class is behind by

            if debug:
                print "Updating Class: %s | Update Backlog: %d | Number Training Items: %d" %(klass, update_level, self.num_trainings)
            if update_level >= 0:
                for f in self.features:
                    self.historical_weights[klass][f] += (update_level * self.last_set_weights[klass][f]) + self.weights[klass][f]
            self.historical_trainings[klass] = self.num_trainings

    def calculate_averaged_weights(self):
        """
        @description: Calculate the averaged weights for all classes.
        @return
            - Success: Dict of averaged weights
            - Failure: False
        """
        for c in self.classes:
            for f in self.features:
                self.averaged_weights[c][f] = self.historical_weights[c][f] / self.num_trainings

    def update_training_weights(self, expected, output, data):
        """
        @description: Update the weights to nudge the model towards a better
                      classifier
                      TODO - make optimised
        """
        # Perform calculations
        for f in data.keys():
            self.last_set_weights[expected][f] = self.weights[expected][f]
            self.last_set_weights[output][f] = self.weights[output][f]
            self.weights[expected][f] += data[f]
            self.weights[output][f] -= data[f]

    def train(self):
        """
        @description: train the perceptron with training data provided
        @args:
            -averaged (bool) - perform averaging after training?
        """

        # Initialise variables and alias variables
        iterations = self.iterations
        training_data = self.training_data
        averaged = not (self.skip_averaging)
        lazy_update = self.lazy_update
        debug = self.debug

        self.initialise_weights()

        if debug:
            print "\n ====================== \n"

        for i in range(0, iterations):  # For each iteration
            if debug:
                print "------------------ \n"
                print "Iteration %d of %d" % (i + 1, iterations)

            td = 0
            for t in training_data:  # For each training item
                # td += 1
                # if td % 100 == 0:
                #     print str(td)
                if debug:
                    print "************"
                self.num_trainings += 1
                gold_class = t['class']

                output_score, output_class = self.classify(t['weights'])  # Classify item
                if debug:
                    print "Training item (iteration %d) | Classified: %s | Gold: %s" % (i + 1, output_class, gold_class)

                if not output_class == gold_class:  # Check classification and update weights
                    self.update_training_weights(gold_class, output_class, t['weights'])
                    if averaged:
                        self.lazy_update_historical_weights(gold_class)
                        self.lazy_update_historical_weights(output_class)

                if debug:
                    print "************"
            if debug:
                print "Historical Sum: %s" % str(self.historical_weights)
                print "------------------ \n"
        if averaged and lazy_update:  # Update all classes
            self.lazy_update_historical_weights(None)

        if averaged:  # Get final averaged weights
            self.calculate_averaged_weights()

        if debug:
            print "\n ====================== \n"

    def classify(self, feature_data_set):
        """
        @description: sum the feature vector against the Perceptron weights to
        classify the vector
        @feature_vector - dict e.g. {"featureA": 0, "featureB": 1 ..}
        """
        best = None
        best_class = None
        weights = self.weights
        for c in self.classes:
            score = 0.0
            for f in feature_data_set.keys():
                score += feature_data_set[f] * weights[c][f]
            if score > best or best is None:
                best = score
                best_class = c
        return best, best_class
