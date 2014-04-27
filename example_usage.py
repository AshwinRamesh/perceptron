from perceptron.perceptron import AveragedPerceptron

classes = ["ClassA", "ClassB"]
features = ["FeatureC", "FeatureD"]
iterations = 10
training_data = [
    {"class": "ClassA", "feature_vector": {"FeatureC": 1.2, "FeatureD": 1.4}},
    {"class": "ClassB", "feature_vector": {"FeatureC": 1.5, "FeatureD": 0.9}}
]
a = AveragedPerceptron("test_db")
a.initialise_perceptron(classes, features, iterations, training_data)
a.train(averaged=True, reset_data=False)

print "Finished training"

# a.update_weight("ClassA", {"FeatureC": 5.3, "FeatureD": 0.24})
# a.add_historical_weight(1, "ClassA", {"FeatureC": 5.3, "FeatureD": 0.24})
# a.add_classifier_data("ClassB", {"FeatureC": 5.3, "FeatureD": 0.24})
# print a.training_data_count
