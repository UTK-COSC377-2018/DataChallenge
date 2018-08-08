from NeoControl import hasNeo
import numpy as np
from collections import deque

if hasNeo:
    from PubGraph import *
else:
    from PubGraphNetwork import *

class Scorer:

    def __init__(self, fnames, pswd="neo4j", bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        if hasNeo:
            self.graph = PubGraph(fnames, pswd, bolt, secure, host, portNum, portType, user)
        else:
            self.graph = PubGraphNetwork(fnames)
        self.scores = np.ones(len(self.graph), dtype=np.float64)
        inds = self.graph.numNodes()
        self.paperStart = 0
        self.venueStart = inds[0]
        self.authStart = inds[1] + inds[0]
        self.normFactors = np.zeros(len(self.graph), dtype=np.float64)
        for i, n in enumerate(self.normFactors):
            n = len(self.graph.getAdj(i))
            n = 1 / n
            self.normFactors[i] = n

    def _calcSingleScore(self, nodeIdx, scores, nodes):
        adj = self.graph.getAdj(nodeIdx)
        scores[nodeIdx] = 0
        for a in adj:
            scores[nodeIdx] += scores[a]*self.normFactors[a]
            nodes.append(a)

    def _compareScores(self, cpy, tol=1e-3):
        return np.allclose(cpy, self.scores, rtol=0.0, atol=tol)

    def calculateScores(self):
        nodes = deque([self.authStart])
        boolList = [False for s in self.scores]
        scoreCpy = self.scores.copy()
        while len(nodes) != 0:
            nodeIdx = nodes.popleft()
            self._calcSingleScore(nodeIdx, scoreCpy, nodes)
            if not boolList[nodeIdx]:
                boolList[nodeIdx] = True
            if all(boolList):
                if self._compareScores(scoreCpy):
                    break
                else:
                    self.scores = scoreCpy.copy()
        self.scores = scoreCpy.copy()

    def __getitem__(self, index):
        return self.scores[index]

    def getGraph(self):
        return self.graph
