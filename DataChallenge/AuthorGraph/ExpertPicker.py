from Scorer import *
from math import ceil
import os
import json

class ExpertPicker:

    """
    ExpertPicker:

    This class divides the papers by field of study and determines the experts in each field.
    """

    def __init__(self, fnames, numFiles=100, percentage=0.05, pswd="neo4j", bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        """
        Divides the papers by field of study and determines the experts in each field.
        
        Parameters:
        * fnames: the name of the TXT file that contains the JSONs
        * numFiles (Default = 100): the number of JSONs to use
        * percentage: the decimal representation of the percentage of authors to consider experts. By default, the top 5% of authors are considered experts.
        * pswd (Default = \"neo4j\"): the password for the neo4j database to be used if using neo4j and py2neo.
        * bolt (Default = None): specifies whether to use the bolt protocol for connection to neo4j (None means autodetect).
          - Note: This is not needed for py2neo v4.0 or higher, as it uses bolt by default.
        * secure (Default = False): specifies whether to use a secure connection for neo4j.
        * host (Default = \"localhost\"): specifies the database server host name if using neo4j.
        * portNum (Default = 7474): specifies the database server port if using neo4j.
          - Note: In py2neo v4.0, the default connection type is bolt, not http. As a result, portnum should probably be set to 7687.
        * portType (Default = \"http\"): specifies the type of port that you want to use for neo4j. Can be \"bolt\", \"https\", or \"http\". If set to a different value, it will assume \"http\".
          - Note: In py2neo v4.0, the default connection type is bolt. As a result, it is best to set portType to \"bolt\", although you can still use the others.
        * user (Default = \"neo4j\"): the user used to authenticate connection to the neo4j database if neo4j is used.
        """
        self.fnames = [ line.rstrip("\n") for idx, line in enumerate(open(fnames, "r")) if idx < numFiles ]
        # Dictionaries to store the data by field (key)
        self.papersByField = {}
        self.authScoresByField = {}
        self.graphsByField = {}
        # Splits the papers by field
        for f in self.fnames:
            jf = json.loads(f)
            for fos in jf["fos"]:
                if fos not in self.papersByField:
                    self.papersByField[fos] = [ f ]
                else:
                    self.papersByField[fos].append(f)
        # Scores are calculated based on the papers in each field
        for key, paperList in self.papersByField.items():
            # Creates a Scorer object from the papers for the current field.
            scorer = Scorer(paperList, pswd, bolt, secure, host, portNum, portType, user)
            # Calculates the scores for the field
            scorer.calculateScores()
            # Stores the publication graph used for scoring in the graphsByField dict
            self.graphsByField[key] = scorer.getGraph()
            # Converts the scores into a list of index-score tuples.
            scoreList = [ (i, s) for i, s in enumerate(scorer.scores) if list(scorer.scores).index(s) >= scorer.authStart ]
            # Sorts the list by scores and extracts the experts
            scoreList.sort(key=lambda x: x[1], reverse=True)
            numExperts = ceil(len(scoreList) * percentage)
            scoreList = scoreList[:numExperts]
            # Saves the index-score pairs for experts as a dictionary in self.authScoresByField
            self.authScoresByField[key] = { s[0]: s[1] for s in scoreList }

    def printExperts(self):
        """
        Prints the names, organizations, and scores of all the experts divided by field.
        """
        for key, authDict in self.authScoresByField.items():
            graph = self.graphsByField[key]
            print("Field of Study: {0:s}".format(key))
            print("=====================")
            for i, score in authDict.items():
                print("    Name: {0:s}\n    Organization: {1:s}".format(graph[i][1]["name"].title(), graph[i][1]["org"].title()))
                print("        Score: {0:f}".format(score), end="\n\n")
            print()

    def printFieldExperts(self, field):
        """
        Prints the names, organizations, and scores of all the experts in a particular field.

        Parameters:
        * field: the name of the desired field.
        """
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

    def listFields(self):
        """
        Prints all the valid field names to stdout.
        """
        print("Fields:")
        print("=======")
        print()
        for field in self.authScoresByField:
            print(field)
        print()
