from perceptron.perceptron_uglified import AveragedPerceptron
from perceptron.statisticals_uglified import Statisticals
import time


def standardise_dataset(data_file):
    """
    Read in the data file and return a standardised format
    that the perceptron class can understand and read
    """
    data = []
    with open(data_file) as f:
        for line in f:
            line = line.split(",")
            line = map(str.strip, line)
            data.append(line[3:])

    # Get the features:

    example = list(data[0])
    del(example[-1])
    features = []

    for i in range(0, len(example)):
        features.append("feature" + str(i+1))

    # Convert the training data into a dictionary

    training_data = []
    for d in data:
        t = {}
        t['weights'] = {}
        try:
            for i in range(0, len(d) - 1):
                t["weights"]["feature" + str(i + 1)] = float(d[i])
            t["class"] = d[-1].strip(".")
            training_data.append(t)
        except:
            pass
    return features, training_data


def main():
    features, training_data = standardise_dataset("data/ad.data")
    classes = ["ad", "nonad"]
    iterations = 3
    start_time = time.time()
    p = AveragedPerceptron(features, classes, training_data, iterations, False)
    start_processing_time = time.time()
    # Do stuff here
    s = Statisticals(p)
    folds = s.cross_validation(10)
    p, r, f = s.calculate_micro_fscore(folds)
    print "Precision: %s Recall: %s F-Score: %s" % (str(p), str(r), str(f))
    print "Total Time taken: %s (Training Time: %s)" % (str(time.time() - start_time), str(time.time() - start_processing_time))
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
    f = file("folds.json", "w+")
    import json
    f.write(json.dumps(avgs))

main()
