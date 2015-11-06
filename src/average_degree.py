# example of program that calculates the average degree of hashtags
from __future__ import division
try:
    import json
except ImportError:
    import simplejson as json
import codecs
import sys
import string


outputFile = sys.argv[2]

class Tweet:
    def __init__(self):
        self.lang=""
        self.langConf=""

    def clean_text(self):
        cleanedText = filter(lambda x: x in string.printable, self.text.replace("\n"," "))
        self.cleaned = self.text == cleanedText
        return cleanedText
    def hash_tags(self):
        words = self.clean_text().split()
        tags = []
        for word in words:
            if word[0] == "#":
                if len(word[1:])>0:
                    tags.append(word[1:].lower())
        return tags

    def parse(self,jsonObj):
        self.date=jsonObj["created_at"]
        self.text=jsonObj["text"]

allTweets={}

def parse(tweet):
    tw=Tweet()
    tw.parse(tweet)
    return tw



fhOverall=None
counts = dict()
edges = dict()


with open(sys.argv[1]) as f:
    lines = f.readlines()
    key = 0
    for line in lines:
        jsonObject = json.loads(line,'UTF-8')
        if all (k in jsonObject for k in ("created_at","text")):
            allTweets[key] = parse(json.loads(line,'UTF-8'))
            key = key + 1

fhOverall=codecs.open(outputFile,"w","UTF-8")
for teet in allTweets:
    tweet=allTweets[teet]
    hashTags = sorted(tweet.hash_tags())
    for tag in hashTags:
        if tag in counts:
            counts[tag] = counts[tag] +1
        else:
            counts[tag] =1
        for nextTag in hashTags[hashTags.index(tag)+1:]:
            if tag in edges:
                if nextTag not in edges[tag]:
                    edges[tag].append(nextTag)
            else:
                edges[tag] = [nextTag]
    sumOfCounts = sum(counts.values())
    countOfEdges = 0
    for value in edges.values():
        countOfEdges = countOfEdges + len(value)
    countOfEdges = countOfEdges
    # If there are no edges considering edge to be 1
    if countOfEdges==0:
        countOfEdges=1
    degree =  sumOfCounts/countOfEdges
    fhOverall.write("%s"%degree+"\n")


fhOverall.close()
