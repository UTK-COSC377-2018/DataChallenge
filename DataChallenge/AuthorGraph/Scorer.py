from NeoControl import hasNeo
import numpy as np
from collections import deque

if hasNeo:
    from PubGraph import *
else:
    from PubGraphNetwork import *

class Scorer:

    """
    Scorer:

    This class implements the scoring method outlined in the A. Pal and S. Ruj paper.
    """

    def __init__(self, fnames, pswd="neo4j", bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        """
        This function creates the publication graph (uses PubGraph if the user has access to neo4j and py2neo; PubGraphNetwork
        otherwise). It also initializes other members and sets the normalization factors.
        """
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
        """
        This helper function updates the score of the graph node with index nodeIdx.
        It also adds the adjacencies of the node represented by nodeIdx to nodes.

        Parameters:
        * nodeIdx: the graph index of the node whose score is being updated.
        * scores: a numpy array of scores (usually, this is a temporary score array)
        * nodes: a deque of node indexes used to control the recursion.
        """
        adj = self.graph.getAdj(nodeIdx)
        scores[nodeIdx] = 0
        for a in adj:
            scores[nodeIdx] += scores[a]*self.normFactors[a]
            nodes.append(a)

    def _compareScores(self, cpy, tol=1e-3):
        """
        This function determines if the iteration is complete.

        Parameters:
        * cpy: a numpy array representing the updated scores.
        * tol: the comparison tolerance

        Returns:
        * True if all elements in cpy are within tol of the elements of self.scores.
        * False otherwise.
        """
        return np.allclose(cpy, self.scores, rtol=0.0, atol=tol)

    def calculateScores(self):
        """
        This function controls the score calculation process.
        """
        # nodes is a deque that is used to control the flow of the recursion.
        # A deque was chosen over a stack because the deque will allow the score of all nodes to be updated at least once
        # faster than a stack would.
        nodes = deque([self.authStart])
        # boolList's elements state whether a node's score has been updated.
        boolList = [False for s in self.scores]
        # scoreCpy is a numpy array that stores the intermediate scores.
        scoreCpy = self.scores.copy()
        # If there are no more adjacencies, the recursion ends.
        # This loop should NEVER exit from this condition because the author-author edges should ALWAYS form cycles.
        while len(nodes) != 0:
            nodeIdx = nodes.popleft()
            # Calculate the updated score for the current node and add the node's adjacencies to the deque.
            self._calcSingleScore(nodeIdx, scoreCpy, nodes)
            # If the current node's score has not been previously updated, set the corresponding element of boolList to True.
            if not boolList[nodeIdx]:
                boolList[nodeIdx] = True
            # The iteration termination condition is only checked once all nodes have had their score updated at least once.
            if all(boolList):
                # If the itermation termination condition is met for all scores, end the recursion.
                if self._compareScores(scoreCpy):
                    break
                # Otherwise, copy the intermediate scores to self.scores.
                else:
                    self.scores = scoreCpy.copy()
        # The intermediate condition has to be copied to self.scores (the final score array) one last time.
        self.scores = scoreCpy.copy()

    def __getitem__(self, index):
        """
        Returns the score corresponding to the provided index.
        """
        return self.scores[index]

    def getGraph(self):
        """
        Returns the PubGraph or PubGraphNetwork object
        """
        return self.graph
