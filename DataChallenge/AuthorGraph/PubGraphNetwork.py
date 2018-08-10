import networkx as nx
import json
import matplotlib.pyplot as plt

def getKey(dictionary, value):
    """
    A basic function that returns the key(s) from dictionary that corresponds with value.

    Parameters:
    * dictionary: the dictionary used to search for the value
    * value: the value whose key(s) is being searched for

    Returns: the key corresponding to value
    """
    keys = list()
    items = dictionary.items()
    for item in items:
        if item[1] == value:
            keys.append(item[0])
    return keys

def authDictCheck(name, org, nodeList):
    """
    This function searches through a list of dictionaries for the dictionary that contains the desired
    name and org values.

    Parameters:
    * name: a string containing the name value being searched for
    * org: a string containing the org value being searched for
    * nodeList: the list of dictionaries being searched

    Returns:
    * The dictionary containing the desired name and org values. Note that this dictionary is removed from the list before being returned
    * None if no dictionary contains the desired name and org values.
    """
    for n in nodeList:
        if n["name"] == name and n["org"] == org:
            auth = n
            nodeList.remove(n)
            return auth
    return None

def matchNameOrgPair(name, org, nodeList):
    """
    This function searches through a list of dictionaries for the dictionary that contains the desired
    name and org values.

    Parameters:
    * name: a string containing the name value being searched for
    * org: a string containing the org value being searched for
    * nodeList: the list of dictionaries being searched

    Returns:
    * The index of the dictionary containing the desired name and org values.
    * -1 if no dictionary contains the desired name and org values.
    """
    for i, n in enumerate(nodeList):
        if n["name"] == name and n["org"] == org:
            return i
    return -1

class PubGraphNetwork:

    """
    PubGraphNetwork:

    This class is based on the original PubGraph class. However, instead of using neo4j and py2neo to create the graph,
    this class uses the networkx library.
    """

    def __init__(self, fnames):
        """
        Creates the Publication Graph from the JSONs listed in fnames.

        Parameters:
        * fnames: a list of absolute paths to the JSONs used to create the graph
        """
        # Initializes the graph as a Multi-Digraph.
        self.graph = nx.MultiDiGraph()
        # Sets the number of papers in the graph equal to the number of JSON files.
        self.numPapers = len(fnames)
        # The ids for venues are set so that they start where the paper ids end
        venueid = len(fnames)
        # nodeList stores the author nodes of the graph so that their ids can be added later.
        nodeList = []
        # jsonidDict is used to store citations between a paper in the graph and a paper not yet in the graph.
        jsonidDict = {}
        for idx, fn in enumerate(fnames):
            # Opens the current JSON and adds the paper it represents to the graph if it is not already present
            f = json.loads(fn)
            if idx not in self.graph:
                self.graph.add_node(idx, title=f["title"], jid=f["id"])
            # If other papers have cited this paper, add the citations as directed edges from the cited paper to the citing papers
            if f["id"] in jsonidDict:
                for jid in jsonidDict[f["id"]]:
                    attrs = nx.get_node_attributes(self.graph, "jid")
                    keys = getKey(attrs, jid)
                    # If the number of keys is 0, there are no nodes with the corresponding JSON id value. So, nothing happens.
                    if len(keys) == 0:
                        continue
                    else:
                        # There should only be one paper with a given JSON id.
                        assert(len(keys) == 1)
                        ind = keys[0]
                        if not self.graph.has_edge(idx, ind):
                            self.graph.add_edge(idx, ind)
            # Obtain the "venue name"
            if "venue" in f:
                vname = f["venue"]
            elif "isbn" in f:
                vname = "{0:s} {1:s}".format(f["publisher"], f["isbn"])
            else:
                vname = "{0:s}{1:s}".format(f["publisher"], f["doc_type"])
            # Check if the venue already has a node in the graph
            attrs = nx.get_node_attributes(self.graph, "vname")
            keys = getKey(attrs, vname)
            # If the venue is not in the graph, add it to the graph, and increment venueid.
            if len(keys) == 0:
                self.graph.add_node(venueid, vname=vname)
                # vkey is used to make it easy to refer to a newly created venue node and an existing venue node in the same way
                vkey = venueid
                venueid += 1
            else:
                # There should only be one venue with a given venue name.
                assert(len(keys) == 1)
                vkey = keys[0]
            # Adds an undirected edge between the paper and venue nodes.
            self.graph.add_edge(idx, vkey)
            self.graph.add_edge(vkey, idx)
            for i in range(len(f["authors"])-1):
                # Checks if the current author is already in nodeList
                auth = authDictCheck(f["authors"][i]["name"], f["authors"][i]["org"], nodeList)
                # If the author is not in nodeList, creates a dictionary of the authors information.
                # Note: the author's data is NOT placed in the graph at this time.
                if auth is None:
                    auth = { "name":f["authors"][i]["name"], "org":f["authors"][i]["org"],
                             "paperAdj":[idx], "venueAdj":[vkey], "authAdj":[] }
                # If the author is in nodeList, adds data on the paper and venue adjacencies for the author
                else:
                    auth["paperAdj"].append(idx)
                    auth["venueAdj"].append(vkey)
                # This for loop associates the current author with all other authors in the paper.
                for j in range(i+1, len(f["authors"])):
                    # Checks if the current author is already in nodeList
                    auth2 = authDictCheck(f["authors"][j]["name"], f["authors"][j]["org"], nodeList)
                    # If the author is not in nodeList, creates a dictionary of the authors information.
                    # Note: the author's data is NOT placed in the graph at this time.
                    if auth2 is None:
                        auth2 = { "name":f["authors"][j]["name"], "org":f["authors"][j]["org"],
                                 "paperAdj":[idx], "venueAdj":[vkey], "authAdj":[] }
                    # If the author is in nodeList, adds data on the paper and venue adjacencies for the author
                    else:
                        auth2["paperAdj"].append(idx)
                        auth2["venueAdj"].append(vkey)
                    # Adds author adjacency data (edges) to the authAdj list in both authors' dictionaries.
                    auth["authAdj"].append((auth2["name"], auth2["org"]))
                    auth2["authAdj"].append((auth["name"], auth["org"]))
                    # Adds auth2's dictionary to nodeList (readds it if it previously existed).
                    nodeList.append(auth2)
                # Adds auth2's dictionary to nodeList (readds it if it previously existed).
                nodeList.append(auth)
            # Adds the references
            for ref in f["references"]:
                attrs = nx.get_node_attributes(self.graph, "jid")
                keys = getKey(attrs, ref)
                # If the cited paper is not already in the graph, adds the current and cited papers to jsonidDict.
                if len(keys) == 0:
                    if ref not in jsonidDict:
                        jsonidDict[ref] = [ f["id"] ]
                    else:
                        jsonidDict[ref].append(f["id"])
                # Otherwise, creates a directed edge from the cited paper to the current paper.
                else:
                    assert(len(keys) == 1)
                    ind = keys[0]
                    self.graph.add_edge(ind, idx)
        # Sets member variable for number of venues
        self.numVenues = venueid - self.numPapers
        # Uses the addAuthNode method to add all the authors and corresponding edges to the graph.
        for idx, node in enumerate(nodeList):
            ind = idx + venueid
            if ind not in self.graph:
                self.addAuthNode(ind, venueid, node, nodeList)
        # Sets member variable for number of authors
        self.numAuthors = len(nodeList)

    def addAuthNode(self, ind, venueid, node, nodeList):
        """
        Recursively adds author nodes and corresponding edges to the graph.

        Parameters:
        * ind: the id that will be given to the current author node.
        * venueid: the value of venueid from the constructor.
        * node: the data dictionary for the current author.
        * nodeList: the list of data dictionaries for all the authors.
        """
        # Adds the current node to the graph
        self.graph.add_node(ind, name=node["name"], org=node["org"])
        # Adds undirected edges between the author and the papers the author helped write.
        for p in node["paperAdj"]:
            self.graph.add_edge(ind, p)
            self.graph.add_edge(p, ind)
        # Adds undirected edges between the author and the venues the author published in.
        for v in node["venueAdj"]:
            self.graph.add_edge(ind, v)
            self.graph.add_edge(v, ind)
        # Loops over all other authors the current author has worked with.
        for a in node["authAdj"]:
            # Ensures the other author is in nodeList
            i = matchNameOrgPair(a[0], a[1], nodeList)
            if i != -1:
                adj = i+venueid
                # If the other author does not have a node in the graph, uses recursion to add the author.
                if adj not in self.graph:
                    self.addAuthNode(adj, venueid, nodeList[i], nodeList)
                # Adds an undirected edge between the two authors.
                self.graph.add_edge(ind, adj)
                self.graph.add_edge(adj, ind)

    def visualize(self):
        """
        This function generates a VERY basic representation of the Publication Graph.
        """
        nx.draw(self.graph)
        plt.show()

    def printData(self):
        """
        Prints all the node data to stdout.
        """
        data = self.graph.nodes(data=True)
        for d in data:
            if d[0] < self.numPapers:
                print("id: {0:d} Title: {1:s} JSON-ID: {2:s}".format(d[0], d[1]["title"], d[1]["jid"]))
            elif d[0] < self.numPapers + self.numVenues:
                print("id: {0:d} Name: {1:s}".format(d[0], d[1]["vname"]))
            else:
                print("id: {0:d} Name: {1:s} Org: {2:s}".format(d[0], d[1]["name"], d[1]["org"]))

    def numNodes(self):
        """
        Returns the tuple (Number of Papers, Number of Venues, Number of Authors)
        """
        return self.numPapers, self.numVenues, self.numAuthors

    def __getitem__(self, index):
        """
        Returns the data for the node with the provided index. If the index is not in the graph, raises an IndexError.

        Parameters:
        * index: an integer corresponding to an id in the graph.

        Returns:
        * A tuple of the form (index, data), where index is the index provided and data is a dictionary containing the node data.
        """
        data = self.graph.nodes(data=True)
        if index < self.numPapers + self.numVenues + self.numAuthors:
            return data[index]
        else:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))

    def __len__(self):
        """
        Returns the number of nodes in the graph.
        """
        return self.numPapers + self.numVenues + self.numAuthors

    def getAdj(self, index):
        """
        Generates a list of node ids for the nodes that are adjacent to the node represented by index.
        If the index is not in the graph, raises an IndexError.

        Parameters:
        * index: an integer corresponding to an id in the graph.

        Returns: a list of node id values corresponding to the adjacencies of the desired node.
        """
        if index >= self.numPapers + self.numVenues + self.numAuthors:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))
        adj = []
        graph_keys = self.graph[index].keys()
        for k in graph_keys:
            adj.append(k)
        # This guarantees that there are no duplicates in adj
        adj = list(set(adj))
        adj.sort(reverse=True)
        return adj
