

############################################################
# Imports
############################################################


import math


############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    returnLst = []

    file = open(path, "r")
    for line in file:
        helperLst = []
        words = line.split(" ")
        for word in words:
            word = word.replace('\n', '')
            word = word.replace('\t', '')
            word = word.replace('\r', '')
            word = word.split("=")
            helperLst.append((word[0], word[1]))
        returnLst.append(helperLst)
    file.close()

    return returnLst


class Tagger(object):

    def __init__(self, sentences):
        self.startProb = {}
        totalStart = {}

        allTags = set()

        for line in sentences:
            for word in line:
                allTags.add(word[1])

        for line in sentences:
            if line[0][1] in totalStart:
                totalStart[line[0][1]] += 1
            else:
                totalStart[line[0][1]] = 1

        for key in allTags:
            helper = 0
            if key in totalStart:
                helper = totalStart[key] + 1
            else:
                helper = 1
            self.startProb[key] = helper / (len(sentences) + len(allTags))
        
        totalTransitions = {}
        self.transitionProbs = {}

        uniqueTags = set()

        for line in sentences:
            for i in range(len(line) - 1):
                uniqueTags.add(line[i][1])
                if line[i][1] in totalTransitions:
                    totalTransitions[line[i][1]] += 1
                else:
                    totalTransitions[line[i][1]] = 1
                if line[i][1] in self.transitionProbs:
                    if line[i + 1][1] in self.transitionProbs[line[i][1]]:
                        self.transitionProbs[line[i][1]][line[i + 1][1]] += 1
                    else:
                        self.transitionProbs[line[i][1]][line[i + 1][1]] = 1
                else:
                    self.transitionProbs[line[i][1]] = {}
                    self.transitionProbs[line[i][1]][line[i + 1][1]] = 1

        for key in uniqueTags:
            if key not in self.transitionProbs:
                self.transitionProbs[key] = {}
            for key2 in uniqueTags:
                if key2 not in self.transitionProbs[key]:
                    self.transitionProbs[key][key2] = 0
                self.transitionProbs[key][key2] = (
                    self.transitionProbs[key][key2] + 1
                ) / (totalTransitions.get(key, 0) + len(uniqueTags))

        
        self.wordTransitionProbs = {}
        totalWords = {}

        uniqueWords = set()

        for line in sentences:
            for i in range(len(line)):
                uniqueWords.add(line[i][0])
                if line[i][1] in totalWords:
                    totalWords[line[i][1]] += 1
                else:
                    totalWords[line[i][1]] = 1
                if line[i][1] in self.wordTransitionProbs:
                    if line[i][0] in self.wordTransitionProbs[line[i][1]]:
                        self.wordTransitionProbs[line[i][1]][line[i][0]] += 1
                    else:
                        self.wordTransitionProbs[line[i][1]][line[i][0]] = 1
                else:
                    self.wordTransitionProbs[line[i][1]] = {}
                    self.wordTransitionProbs[line[i][1]][line[i][0]] = 1


        for key in uniqueTags:
            if key not in self.wordTransitionProbs:
                self.wordTransitionProbs[key] = {}
            for key2 in uniqueWords:
                if key2 not in self.wordTransitionProbs[key]:
                    self.wordTransitionProbs[key][key2] = 0
                self.wordTransitionProbs[key][key2] = (
                    self.wordTransitionProbs[key][key2] + 1
                ) / (totalWords.get(key, 0) + len(uniqueWords))




    def most_probable_tags(self, tokens):
        returnLst = []

        for token in tokens:
            maxProb = float('-inf')
            listAppend = None
            for key in self.wordTransitionProbs:
                if token in self.wordTransitionProbs[key]:
                    if self.wordTransitionProbs[key][token] > maxProb:
                        maxProb = self.wordTransitionProbs[key][token]
                        listAppend = key
            returnLst.append(listAppend)

        return returnLst

    def viterbi_tags(self, tokens):
        returnLst = []

        probabilities = []
        previousTag = []

        for x in range(len(tokens)):
            probabilities.append({})
            previousTag.append({})

        firstToken = tokens[0]

        tags = self.transitionProbs.keys()

        for tag in tags:
            probabilities[0][tag] = math.log(self.startProb[tag]) + math.log(self.wordTransitionProbs[tag][firstToken])


        for token in range(1, len(tokens)):
            for tag1 in tags:
                maxProb = float('-inf')
                tagToAdd = None
                for tag2 in tags:
                    viterbiProb = math.log(self.wordTransitionProbs[tag1][tokens[token]]) + math.log(self.transitionProbs[tag2][tag1]) + probabilities[token - 1][tag2]
                    if viterbiProb > maxProb:
                        maxProb = viterbiProb
                        tagToAdd = tag2
                probabilities[token][tag1] = maxProb
                previousTag[token][tag1] = tagToAdd

        maxTag = float('-inf')
        finalTag = None
        for tag in tags:
            if probabilities[-1][tag] > maxTag:
                maxTag = probabilities[-1][tag]
                finalTag = tag

        returnLst.append(finalTag)

        rangeNum = len(tokens) - 1
        for token in range(rangeNum, 0, -1):
            returnLst.insert(0, previousTag[token][returnLst[0]])

        
        return returnLst


