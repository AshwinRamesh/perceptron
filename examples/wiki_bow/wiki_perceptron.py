from perceptron.perceptron_optimised import AveragedPerceptron
from collections import defaultdict, Counter
from perceptron.statisticals_optimised import Statisticals
import string
import json


def bow_generic_valued(gold_file, data_path):
    """
    @description: Generic BOW (valued features)
    """
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)
        for url_data in gold_data:  # iterate through each block of url data
            errors = []
            try:
                f = open("%s/%s.txt" % (data_path, url_data['url'].split("wiki/")[-1]))
                # remove punctuation
                document_words = f.read().strip().lower()
                for char in string.punctuation:
                    document_words = document_words.replace(char, " ")
                document_words = document_words.split()
                f.close()
                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit():
                        words[w] = 0
                        training[url_data['url']][w] += 1
                        classes[url_data['gold_class']] += 1
                url_class[url_data['url']] = url_data['gold_class']
            except Exception, e:
                errors.append(str(e))

        perceptron_features = words.keys()
        perceptron_classes = classes.keys()
        training_data = []
        print "Processing Training Data"
        for u_key in training.keys():  # iterate through each url and create training_data
            training_data.append({"class": url_class[u_key], "weights": dict(training[u_key])})

        print "starting"
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_generic_valued")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_generic_boolean(gold_file, data_path):
    """
    @description: Generic BOW (boolean features)
    """
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)
        for url_data in gold_data:  # iterate through each block of url data
            errors = []
            try:
                f = open("%s/%s.txt" % (data_path, url_data['url'].split("wiki/")[-1]))
                # remove punctuation
                document_words = f.read().strip().lower()
                for char in string.punctuation:
                    document_words = document_words.replace(char, " ")
                document_words = document_words.split()
                f.close()
                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit():
                        words[w] = 0
                        training[url_data['url']][w] = 1
                        classes[url_data['gold_class']] += 1
                url_class[url_data['url']] = url_data['gold_class']
            except Exception, e:
                errors.append(str(e))

        perceptron_features = words.keys()
        perceptron_classes = classes.keys()
        training_data = []
        print "Processing Training Data"
        for u_key in training.keys():  # iterate through each url and create training_data
            training_data.append({"class": url_class[u_key], "weights": dict(training[u_key])})

        print "starting"
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_generic_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove500_valued(gold_file, data_path):
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/500common.txt")
        common = f.read().strip().lower()
        for char in string.punctuation:
            common = common.replace(char, " ")
        common = common.split()
        f.close()

        for url_data in gold_data:  # iterate through each block of url data
            errors = []
            try:
                f = open("%s/%s.txt" % (data_path, url_data['url'].split("wiki/")[-1]))
                # remove punctuation
                document_words = f.read().strip().lower()
                for char in string.punctuation:
                    document_words = document_words.replace(char, " ")
                document_words = document_words.split()
                f.close()
                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit() and w not in common:
                        words[w] = 0
                        training[url_data['url']][w] += 1
                        classes[url_data['gold_class']] += 1
                url_class[url_data['url']] = url_data['gold_class']
            except Exception, e:
                errors.append(str(e))

        perceptron_features = words.keys()
        perceptron_classes = classes.keys()
        training_data = []
        print "Processing Training Data"
        for u_key in training.keys():  # iterate through each url and create training_data
            training_data.append({"class": url_class[u_key], "weights": dict(training[u_key])})

        print "starting"
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove500_valued")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove1000_valued(gold_file, data_path):
    pass


def bow_remove5000_valued(gold_file, data_path):
    pass


def bow_remove500_boolean(gold_file, data_path):
    pass


def bow_remove1000_boolean(gold_file, data_path):
    pass


def bow_remove5000_boolean(gold_file, data_path):
    pass


def process_perceptron(classes, features, training_data, name):
    """
    Process the perceptron through statisticals and write data into a file
    """
    iterations = [1, 3, 5]
    fold_num = 10
    output = []  # output data to be written into file

    # Process Averaged
    for x in [True, False]:
        for i in iterations:
            perceptron = AveragedPerceptron(features, classes, training_data, i, x)
            data = {}
            print "Processing %s | Averaged: %s | Iterations: %d" % (name, str(not(x)), i)
            s = Statisticals(perceptron)
            folds = s.cross_validation(fold_num)

            # Micro-Averaging
            p, r, f = s.calculate_micro_fscore(folds)
            micro = {"precision": p, "recall": r, "f-score": f}

            # Simple Averaging
            avgs = {}
            for i in range(0, len(folds)):
                correct = 0
                incorrect = 0
                for item in folds[i]:
                    if item['gold'] == item['classified']:
                        correct += 1
                    else:
                        incorrect += 1
                avgs["fold_%d" % (i+1)] = {"correct": correct, "incorrect": incorrect, "accuracy": ((float(correct)/float(len(folds[i]))) * 100)}

            data["micro_average"] = micro
            data["standard_average"] = avgs
            data["details"] = {"iterations": i, "num_features": len(perceptron.features), "averaged": not(x)}
            output.append(data)
    # Write to file
    f = file("%s_data.json" % name, "w+")
    f.write(json.dumps(output))
    f.close()
    print "Finished %s!" % name


def main():
    bow_generic_valued("data/gold_standards.json", "data/comp5046-articles")


main()
