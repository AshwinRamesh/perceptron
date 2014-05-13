from perceptron.perceptron_optimised import AveragedPerceptron
from collections import defaultdict, Counter, Iterable
from perceptron.statisticals_optimised import Statisticals
import string
import json


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, basestring):
            for x in flatten(item):
                yield x
            else:
                yield item


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
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/1000common.txt")
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove1000_valued")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove5000_valued(gold_file, data_path):
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/5000common.txt")
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove5000_valued")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove500_boolean(gold_file, data_path):
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove500_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove1000_boolean(gold_file, data_path):
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/1000common.txt")
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove1000_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_remove5000_boolean(gold_file, data_path):
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        print classes
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/5000common.txt")
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
                        training[url_data['url']][w] = 1
                        classes[url_data['gold_class']] += 1
                url_class[url_data['url']] = url_data['gold_class']
            except Exception, e:
                errors.append(str(e))

        perceptron_features = words.keys()
        perceptron_classes = classes.keys()
        print classes.keys()
        training_data = []
        print "Processing Training Data"
        for u_key in training.keys():  # iterate through each url and create training_data
            training_data.append({"class": url_class[u_key], "weights": dict(training[u_key])})

        print "starting"
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_remove5000_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_wiki_json_boolean(gold_file, data_path):
    """
    Features are all words (without top 1000 common) + all category words in .json provided
    """
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/1000common.txt")
        common = f.read().strip().lower()
        for char in string.punctuation:
            common = common.replace(char, " ")
        common = common.split()
        f.close()

        for url_data in gold_data:  # iterate through each block of url data
            errors = []
            try:
                f = open("%s/%s.json" % (data_path, url_data['url'].split("wiki/")[-1]))
                document = json.load(f)
                f.close()
                # remove punctuation
                document_words = document["paragraph_text"].strip().lower()
                for char in string.punctuation:
                    document_words = document_words.replace(char, " ")
                document_words = document_words.split()

                # Add the words under templates into words
                lst = flatten(document['templates'])
                for w in lst:
                    w = str(w).strip().lower()
                    if w not in ["was", "is", "[]", "an", "had", "were", "has", "been", "are", "born"]:
                        document_words.append(w)

                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit() and w not in common:
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_with_json_boolean2")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def bow_wiki_json_minimal_boolean(gold_file, data_path):
    """
    Only use data from templates. Split data into words, remove _, etc
    Remove 500 top words
    """
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
                f = open("%s/%s.json" % (data_path, url_data['url'].split("wiki/")[-1]))
                document = json.load(f)
                f.close()

                # Add the words under templates into words after processing
                document_words = []
                lst = flatten(document['templates'])
                for w in lst:
                    w = str(w).strip().lower()
                    w = w.replace("_", " ")
                    for char in string.punctuation:
                        w = w.replace(char, " ")
                    wrds = w.split()
                    document_words += wrds

                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit() and w not in common:
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
        process_perceptron(perceptron_classes, perceptron_features, training_data, "bow_wiki_json_minimal_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"


def count_words(gold_file, data_path):
    """
    Only use data from templates. Split data into words, remove _, etc
    Remove 500 top words
    """
    """
    Features are all words (without top 1000 common) + all category words in .json provided
    """
    try:
        with open(gold_file) as data_file:
            gold_data = json.load(data_file)
        words = defaultdict(int)
        classes = defaultdict(int)
        wc = Counter()
        url_class = {}
        training = defaultdict(Counter)

        f = open("data/1000common.txt")
        common = f.read().strip().lower()
        for char in string.punctuation:
            common = common.replace(char, " ")
        common = common.split()
        f.close()

        for url_data in gold_data:  # iterate through each block of url data
            errors = []
            try:
                f = open("%s/%s.json" % (data_path, url_data['url'].split("wiki/")[-1]))
                document = json.load(f)
                f.close()
                # remove punctuation
                document_words = document["paragraph_text"].strip().lower()
                for char in string.punctuation:
                    document_words = document_words.replace(char, " ")
                document_words = document_words.split()

                # Add the words under templates into words
                lst = flatten(document['templates'])
                for w in lst:
                    document_words.append(str(w).strip().lower())

                for w in document_words:
                    # dont include one character words or words starting with numbers
                    if len(w) > 1 and not w[0].isdigit() and w not in common:
                        words[w] = 0
                        wc[w] += 1
                        training[url_data['url']][w] = 1
                        classes[url_data['gold_class']] += 1
                url_class[url_data['url']] = url_data['gold_class']
            except Exception, e:
                errors.append(str(e))

        perceptron_features = words.keys()
        perceptron_classes = classes.keys()
        f = file("wordcount.txt", "w+")
        for c in wc.most_common(1000):
            print c
            f.write("%s (%d)\n" % (c[0], c[1]))
        for c in wc.most_common()[-1000:]:
            f.write("%s (%d)\n" % (c[0], c[1]))
        f.close()
        training_data = []
        print "Processing Training Data"
        for u_key in training.keys():  # iterate through each url and create training_data
            training_data.append({"class": url_class[u_key], "weights": dict(training[u_key])})

        print "starting"
        process_perceptron(perceptron_classes, perceptron_features, training_data, "BOW_with_json_boolean")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"



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
            for j in range(0, len(folds)):
                correct = 0
                incorrect = 0
                for item in folds[j]:
                    if item['gold'] == item['classified']:
                        correct += 1
                    else:
                        incorrect += 1
                avgs["fold_%d" % (j+1)] = {"correct": correct, "incorrect": incorrect, "accuracy": ((float(correct)/float(len(folds[j]))) * 100)}

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
    bow_wiki_json_boolean("data/gold_standards.json", "data/comp5046-articles")


main()
