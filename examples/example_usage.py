from perceptron.perceptron import AveragedPerceptron
from time import time

classes = ["ClassA", "ClassB"]
features = ["FeatureC", "FeatureD"]
iterations = 10
training_data = [
    {"class": "ClassA", "feature_vector": {"FeatureC": 1, "FeatureD": 0}},
    {"class": "ClassB", "feature_vector": {"FeatureC": 0, "FeatureD": 1}}
]


a = AveragedPerceptron(skip_averaging=False, lazy_update=True, debug=False)
a.initialise_perceptron(classes, features, iterations, training_data)
a.train()
print "Poo"
print a.averaged_weights

a = AveragedPerceptron(skip_averaging=False, lazy_update=False, debug=False)
a.initialise_perceptron(classes, features, iterations, training_data)
a.train()
print "bum"
print a.averaged_weights
