from collections import defaultdict, Counter
from perceptron.perceptron_uglified import AveragedPerceptron
from perceptron.statisticals_uglified import Statisticals
import json
import string


def simple_bow(gold_file, data_path, output_file):
    """
    @description: A simple bag of words implementation for the wiki articles
        Reads the .txt files for each url and creates a file with data output
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
        p = AveragedPerceptron(perceptron_features, perceptron_classes, training_data, 1)
        run_perceptron(p, "simple_bow.json")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"

def remove5000common_bow(gold_file, data_path, output_file):
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
        p = AveragedPerceptron(perceptron_features, perceptron_classes, training_data, 3)
        run_perceptron(p, "simple_bow.json")
        print "DONE"
    except Exception, e:
        import traceback
        print traceback.print_exc()
        print e
        print "Failure"

def run_perceptron(perceptron, fname):
    s = Statisticals(perceptron)
    folds = s.cross_validation(10)
    p, r, f = s.calculate_micro_fscore(folds)
    print "Precision: %s Recall: %s F-Score: %s" % (str(p), str(r), str(f))
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
    total = 0
    for k in avgs.keys():
        total += avgs[k]['accuracy']
    avgs['averaged'] = total/len(folds)
    f = file(fname + ".json", "w+")
    import json
    f.write(json.dumps(avgs))

remove5000common_bow("data/gold_standards.json", "data/comp5046-articles", "words")
#simple_bow("data/gold_standards.json", "data/comp5046-articles", "words")

