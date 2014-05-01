"""
Process the gold class classification for each url
"""

from collections import defaultdict, Counter
import json


file_name = "data/comp5046-labels.tsv"
output_name = "data/gold_standards.json"

urls = defaultdict(Counter)

with open(file_name) as f:
    content = f.readlines()  # read file and count what category for each url

for line in content:
    try:
        data = line.strip().split("\t")
        if len(data) != 3:  # not enough data in line
            continue
        urls[data[1]][data[2]] += 1
    except Exception, e:
        print e

gold_standard = []

for k in urls.keys():
    common = urls[k].most_common(2)
    gold_standard.append({
        "url": k,
        "total_votes": len(list(urls[k].elements())),
        "gold_class": urls[k].most_common(1)[0][0],
        "gold_class_votes": urls[k].most_common(1)[0][1]})

f = file(output_name, "w+")
f.write(json.dumps(gold_standard))
print "Done processing"
