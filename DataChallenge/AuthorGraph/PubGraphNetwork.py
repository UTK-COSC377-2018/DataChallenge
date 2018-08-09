import networkx as nx
import json
import matplotlib.pyplot as plt

def getKey(dictionary, value):
    keys = list()
    items = dictionary.items()
    for item in items:
        if item[1] == value:
            keys.append(item[0])
    return keys

def authDictCheck(name, org, nodeList):
    for n in nodeList:
        if n["name"] == name and n["org"] == org:
            auth = n
            nodeList.remove(n)
            return auth
    return None

def matchNameOrgPair(name, org, nodeList):
    for i, n in enumerate(nodeList):
        if n["name"] == name and n["org"] == org:
            return i
    return -1

class PubGraphNetwork:

    def __init__(self, fnames):
        self.graph = nx.MultiDiGraph()
        self.numPapers = len(fnames)
        venueid = len(fnames)
        nodeList = []
        jsonidDict = {}
        for idx, fn in enumerate(fnames):
            o = open(fn, "r")
            f = json.load(o)
            if idx not in self.graph:
                self.graph.add_node(idx, title=f["title"], jid=f["id"])
                data = self.graph.nodes(data=True)
            if f["id"] in jsonidDict:
                for jid in jsonidDict[f["id"]]:
                    attrs = nx.get_node_attributes(self.graph, "jid")
                    keys = getKey(attrs, jid)
                    if len(keys) == 0:
                        continue
                    else:
                        assert(len(keys) == 1)
                        ind = keys[0]
                        if not self.graph.has_edge(idx, ind):
                            self.graph.add_edge(idx, ind)
            if "venue" in f:
                vname = f["venue"]
            elif "isbn" in f:
                vname = "{0:s} {1:s}".format(f["publisher"], f["isbn"])
            else:
                vname = "{0:s}{1:s}".format(f["publisher"], f["doc_type"])
            attrs = nx.get_node_attributes(self.graph, "vname")
            keys = getKey(attrs, vname)
            if len(keys) == 0:
                self.graph.add_node(venueid, vname=vname)
                vkey = venueid
                venueid += 1
            else:
                assert(len(keys) == 1)
                vkey = keys[0]
            self.graph.add_edge(idx, vkey)
            self.graph.add_edge(vkey, idx)
            for i in range(len(f["authors"])-1):
                auth = authDictCheck(f["authors"][i]["name"], f["authors"][i]["org"], nodeList)
                if auth is None:
                    auth = { "name":f["authors"][i]["name"], "org":f["authors"][i]["org"],
                             "paperAdj":[idx], "venueAdj":[vkey], "authAdj":[] }
                else:
                    auth["paperAdj"].append(idx)
                    auth["venueAdj"].append(vkey)
                for j in range(i+1, len(f["authors"])):
                    auth2 = authDictCheck(f["authors"][j]["name"], f["authors"][j]["org"], nodeList)
                    if auth2 is None:
                        auth2 = { "name":f["authors"][j]["name"], "org":f["authors"][j]["org"],
                                 "paperAdj":[idx], "venueAdj":[vkey], "authAdj":[] }
                    else:
                        auth2["paperAdj"].append(idx)
                        auth2["venueAdj"].append(vkey)
                    auth["authAdj"].append((auth2["name"], auth2["org"]))
                    auth2["authAdj"].append((auth["name"], auth["org"]))
                    nodeList.append(auth2)
                nodeList.append(auth)
            for ref in f["references"]:
                attrs = nx.get_node_attributes(self.graph, "jid")
                keys = getKey(attrs, ref)
                if len(keys) == 0:
                    if ref not in jsonidDict:
                        jsonidDict[ref] = [ f["id"] ]
                    else:
                        jsonidDict[ref].append(f["id"])
                else:
                    assert(len(keys) == 1)
                    ind = keys[0]
                    self.graph.add_edge(ind, idx)
        self.numVenues = venueid - self.numPapers
        for idx, node in enumerate(nodeList):
            ind = idx + venueid
            if ind not in self.graph:
                self.addAuthNode(ind, venueid, node, nodeList)
        self.numAuthors = len(nodeList)

    def addAuthNode(self, ind, venueid, node, nodeList):
        self.graph.add_node(ind, name=node["name"], org=node["org"])
        for p in node["paperAdj"]:
            self.graph.add_edge(ind, p)
            self.graph.add_edge(p, ind)
        for v in node["venueAdj"]:
            self.graph.add_edge(ind, v)
            self.graph.add_edge(v, ind)
        for a in node["authAdj"]:
            i = matchNameOrgPair(a[0], a[1], nodeList)
            if i != -1:
                adj = i+venueid
                if adj not in self.graph:
                    self.addAuthNode(adj, venueid, nodeList[i], nodeList)
                self.graph.add_edge(ind, adj)
                self.graph.add_edge(adj, ind)

    def visualize(self):
        nx.draw(self.graph)
        plt.show()

    def printData(self):
        data = self.graph.nodes(data=True)
        for d in data:
            if d[0] < self.numPapers:
                print("id: {0:d} Title: {1:s} JSON-ID: {2:s}".format(d[0], d[1]["title"], d[1]["jid"]))
            elif d[0] < self.numPapers + self.numVenues:
                print("id: {0:d} Name: {1:s}".format(d[0], d[1]["vname"]))
            else:
                print("id: {0:d} Name: {1:s} Org: {2:s}".format(d[0], d[1]["name"], d[1]["org"]))

    def numNodes(self):
        return self.numPapers, self.numVenues, self.numAuthors

    def __getitem__(self, index):
        data = self.graph.nodes(data=True)
        if index < self.numPapers + self.numVenues + self.numAuthors:
            return data[index]
        else:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))

    def __len__(self):
        return self.numPapers + self.numVenues + self.numAuthors

    def getAdj(self, index):
        if index >= self.numPapers + self.numVenues + self.numAuthors:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))
        adj = []
        graph_keys = self.graph[index].keys()
        for k in graph_keys:
            adj.append(k)
        adj.sort(reverse=True)
        return adj
