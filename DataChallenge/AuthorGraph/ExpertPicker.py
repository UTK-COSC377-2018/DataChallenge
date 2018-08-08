from Scorer import *
from math import ceil
import os
import json

class ExpertPicker:

    def __init__(self, fnames, percentage=0.05, pswd="neo4j", bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        self.fnames = []
        if type(fnames) is list or type(fnames) is tuple:
            for f in fnames:
                self.fnames.append(os.path.abspath(f))
        elif type(fnames) is str:
            if os.path.isdir(fnames):
                for f in os.listdir(fnames):
                    if os.path.isdir(os.path.abspath(f)):
                        continue
                    else:
                        name = os.path.abspath(f)
                        try:
                            if name[-5:] == ".json":
                                self.fnames.append(name)
                        except IndexError as e:
                            continue
            else:
                try:
                    if fnames[-5:] == ".json":
                        self.fnames.append(name)
                except IndexError as e:
                    pass
        else:
            raise TypeError("fnames must be a list, tuple, or string.")
        self.papersByField = {}
        self.authScoresByField = {}
        self.graphsByField = {}
        for f in self.fnames:
            fo = open(f)
            jf = json.load(fo)
            for fos in jf["fos"]:
                if fos not in self.papersByField:
                    self.papersByField[fos] = [ f ]
                else:
                    self.papersByField[fos].append(f)
        for key, paperList in self.papersByField.items():
            scorer = Scorer(paperList, pswd, bolt, secure, host, portNum, portType, user)
            scorer.calculateScores()
            self.graphsByField[key] = scorer.getGraph()
            scoreList = [ (i, s) for i, s in enumerate(scorer.scores) if list(scorer.scores).index(s) >= scorer.authStart ]
            scoreList.sort(key=lambda x: x[1], reverse=True)
            numExperts = ceil(len(scoreList) * percentage)
            scoreList = scoreList[:numExperts]
            self.authScoresByField[key] = { s[0]: s[1] for s in scoreList }

    def printExperts(self):
        for key, authDict in self.authScoresByField.items():
            graph = self.graphsByField[key]
            print("Field of Study: {0:s}".format(key))
            print("=====================")
            for i, score in authDict.items():
                print("    Name: {0:s}\n    Organization: {1:s}".format(graph[i][1]["name"].title(), graph[i][1]["org"].title()))
                print("        Score: {0:f}".format(score), end="\n\n")
            print()

    def printFieldExperts(self, field):
        if field not in self.authScoresByField:
            print("{0:s} is not a valid field.\n".format(field))
            return
        graph = self.graphsByField[field]
        print("Field of Study: {0:s}".format(field))
        print("=====================")
        for i, score in self.authScoresByField[field].items():
            print("    Name: {0:s}\n    Organization: {1:s}".format(graph[i][1]["name"].title(), graph[i][1]["org"].title()))
            print("        Score: {0:f}".format(score), end="\n\n")
        print()
