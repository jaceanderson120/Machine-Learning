
############################################################
# Imports
############################################################


import email
import math
import os

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    parsedFile = []
    usableFile = open(email_path, "r")
    fileLines = email.message_from_file(usableFile)
    for fileLine in email.iterators.body_line_iterator(fileLines):
        fileLine = fileLine.replace("\n", " ")
        fileLine = fileLine.replace("\t", " ")
        fileLine = fileLine.replace("\r", " ")
        for i in fileLine.split(" "):
            if i != "":
                parsedFile.append(i)
    return parsedFile



def log_probs(email_paths, smoothing):
    wordsList = []
    setOfWords = set()

    for path in email_paths:
        words = load_tokens(path)
        setOfWords.update(words)
        wordsList.extend(words)

    wordDict = {}

    for i in setOfWords:
        wordDict[i] = 0

    for i in wordsList:
        wordDict[i] = wordDict[i] + 1

    probDict = {}

    for key in wordDict.keys():
        probDict[key] = math.log((wordDict[key] + smoothing) / (len(wordsList) + (smoothing * (len(setOfWords) + 1))))
    probDict["<UNK>"] = math.log(smoothing / (len(wordsList) + (smoothing * (len(setOfWords) + 1))))

    return probDict


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_dirs = [os.path.join(spam_dir, fileName) for fileName in os.listdir(spam_dir)]
        ham_dirs = [os.path.join(ham_dir, fileName) for fileName in os.listdir(ham_dir)]


        self.spam = log_probs(spam_dirs, smoothing)
        self.ham = log_probs(ham_dirs, smoothing)

        directory_length = len(os.listdir(spam_dir)) + len(os.listdir(ham_dir))

        self.prob_spam = len(os.listdir(spam_dir)) / directory_length
        self.prob_not_spam = len(os.listdir(ham_dir)) / directory_length
    
    def is_spam(self, email_path):
        sum_spam = math.log(self.prob_spam)
        sum_ham= math.log(self.prob_not_spam)

        parsedFile = load_tokens(email_path)

        for item in parsedFile:
            if item in self.spam:
                sum_spam += self.spam[item]
            else:
                sum_spam += self.spam["<UNK>"]

            if item in self.ham:
                sum_ham += self.ham[item]
            else:
                sum_ham += self.ham["<UNK>"]
                

        if sum_spam > sum_ham:
            return True
        return False

    def most_indicative_spam(self, n):
        wordProbs = {}
        for word in self.spam:
            if word in self.ham:
                prob_spam = math.exp(self.spam[word])
                prob_ham = math.exp(self.ham[word])

                wordProbs[word] = math.log(prob_spam / ((prob_spam + prob_ham) / 2))

        returnWords = sorted(wordProbs, key=wordProbs.get, reverse=True)
        returnWords = returnWords[:n]
        return returnWords

    def most_indicative_ham(self, n):
        wordProbs = {}
        for word in self.spam:
            if word in self.ham:
                prob_spam = math.exp(self.spam[word])
                prob_ham = math.exp(self.ham[word])

                wordProbs[word] = math.log(prob_ham / ((prob_spam + prob_ham) / 2))

        returnWords = sorted(wordProbs, key=wordProbs.get, reverse=True)
        returnWords = returnWords[:n]
        return returnWords

