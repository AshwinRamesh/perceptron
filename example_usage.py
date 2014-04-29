from perceptron.perceptron import AveragedPerceptron
from time import time

classes = ["ClassA", "ClassB"]
features = ["FeatureC", "FeatureD"]
iterations = 10
training_data = [
    {"class": "ClassA", "feature_vector": {"FeatureC": 1.2, "FeatureD": 1.4}},
    {"class": "ClassB", "feature_vector": {"FeatureC": 1.5, "FeatureD": 0.9}}
]


a = AveragedPerceptron(skip_averaging=False, lazy_update=True)
a.initialise_perceptron(classes, features, iterations, training_data)
a.train()
print a.averaged_weights

a = AveragedPerceptron(skip_averaging=False, lazy_update=False)
a.initialise_perceptron(classes, features, iterations, training_data)
a.train()
print a.averaged_weights
