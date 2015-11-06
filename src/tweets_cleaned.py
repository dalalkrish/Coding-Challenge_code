# example of program that calculates the number of tweets cleaned
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

    def textRow(self):
        row = "\t".join((
            self.clean_text(),
            "("+str(self.date)+")"
        ))
        row = "%s\n"%row
        return row

    def clean_text(self):
        cleanedText = filter(lambda x: x in string.printable, self.text.replace("\n"," "))
        self.cleaned = self.text == cleanedText
        return cleanedText

    def isCleaned(self):
        return self.text == filter(lambda x: x in string.printable, self.text)

    def parse(self,jsonObj):
        self.date=jsonObj["created_at"]
        self.text=jsonObj["text"]




allTweets={}
cleanedCount = 0
def parse(tweet):
    tw=Tweet()
    tw.parse(tweet)
    return tw



fhOverall=None

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
    if tweet.isCleaned():
        cleanedCount = cleanedCount + 1
    fhOverall.write(tweet.textRow())
fhOverall.write("%s"%cleanedCount+" tweets contained unicode.")


fhOverall.close()


