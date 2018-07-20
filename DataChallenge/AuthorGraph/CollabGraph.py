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
        for fn in fnames:
            o = open(fn)
            f = json.load(fn)
            for i in len(f["authors"]):
                auth = Node("Author", name=f["authors"][i]["name"], org=f["authors"][i]["org"])
                if not self.graph.exists(auth):
                    self.graph.create(auth)
                for j in range(i+1, len(f["authors"])):
                    auth2 = Node("Author", name=f["authors"][j]["name"], org=f["authors"][j]["org"])
                    if not self.graph.exists(auth2):
                        self.graph.create(auth2)
                    rel1 = Relationship(auth, "CoAuth", auth2)
                    rel2 = Relationship(auth2, "CoAuth", auth)
                    if (not self.graph.exists(rel1)) and (not self.graph.exists(rel2)):
                        self.graph.create(rel1)
                        self.graph.create(rel2)
