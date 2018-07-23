from py2neo import Graph, Node, Relationship
import json

class CollabGraph:

    def __init__(self, fnames, pswd, bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        if portType == "bolt":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, bolt_port=portNum, user=user, password=pswd)
        elif portType == "https":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, https_port=portNum, user=user, password=pswd)
        else:
            self.graph = Graph(bolt=bolt, secure=secure, host=host, http_port=portNum, user=user, password=pswd)
        self.graph.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.id IS UNIQUE")
        nodeList = []
        for fn in fnames:
            o = open(fn, "r")
            f = json.load(o)
            for i in range(len(f["authors"])-1):
                auth = Node("Author", name=f["authors"][i]["name"], org=f["authors"][i]["org"])
                self.graph.merge(auth)
                if auth not in nodeList:
                    nodeList.append(auth)
                for j in range(i+1, len(f["authors"])):
                    auth2 = Node("Author", name=f["authors"][j]["name"], org=f["authors"][j]["org"])
                    self.graph.merge(auth2)
                    if auth2 not in nodeList:
                        nodeList.append(auth2)
                    rel1 = Relationship(auth, "CoAuth", auth2)
                    rel2 = Relationship(auth2, "CoAuth", auth)
                    self.graph.merge(rel1 | rel2)
        for idx, node in enumerate(nodeList):
            node["id"] = idx
            self.graph.push(node)
        self.numNodes = len(nodeList)

#    def getAdj(self, nodeIdx):

    def addAuthor(self, name, org):
        auth = Node("Author", name=name, org=org, id=self.numNodes)
        self.graph.merge(auth)
        self.numNodes += 1

    def addAuthor(self, node):
        assert(isinstance(node, Node))
        node["id"] = self.numNodes
        self.graph.merge(node)
        self.numNodes += 1

    def __add__(self, node):
        if isinstance(node, Node):
            addAuthor(node)
        elif node is list or node is tuple:
            addAuthor(node[0], node[1])
        else:
            raise TypeError("Parameter `node` must be a Py2Neo Node, Python list, or Python tuple.")
        return

    def __len__(self):
        return self.numNodes

    def __contains__(self, name):
        query = "MATCH (a:Author {{name:\"{0:s}\"}}) RETURN a".format(name)
        return self.graph.run(query).data()

    def __getitem__(self, index):
        query = "MATCH (a:Author {{id:{0:d} }}) RETURN a".format(index)
        return self.graph.run(query).data()
