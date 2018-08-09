from py2neo import Graph, Node, Relationship
import json

class PubGraph:

    def __init__(self, fnames, pswd, bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        if portType == "bolt":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, bolt_port=portNum, user=user, password=pswd)
        elif portType == "https":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, https_port=portNum, user=user, password=pswd)
        else:
            self.graph = Graph(bolt=bolt, secure=secure, host=host, http_port=portNum, user=user, password=pswd)
        self.graph.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.id IS UNIQUE")
        self.graph.run("CREATE CONSTRAINT ON (v:Venue) ASSERT v.id IS UNIQUE")
        self.graph.run("CREATE CONSTRAINT ON (p:Paper) ASSERT p.id IS UNIQUE")
        nodeList = []
        jsonidDict = {}
        for idx, fn in enumerate(fnames):
            o = open(fn, "r")
            f = json.load(o)
            paper = Node("Paper", title=f["title"], jid=f["id"], id=idx)
            self.graph.merge(paper)
            if f["id"] in jsonidDict:
                for jid in jsonidDict[f["id"]]:
                    citer = self.graph.evaluate("MATCH (p:Paper {{jid:\"{0:s}\"}}) RETURN p".format(jid))
                    if citer is not None:
                        self.graph.merge(Relationship(paper, "Cites", citer))
            if "venue" in f:
                vname = f["venue"]
            elif "isbn" in f:
                vname = "{0:s} {1:s}".format(f["publisher"], f["isbn"])
            else:
                vname = "{0:s} {1:s}".format(f["publisher"], f["doc_type"])
            vexists = self.graph.evaluate("MATCH (v:Venue {{name:\"{0:s}\"}}) RETURN v".format(vname))
            if vexists is None:
                venueid = self.graph.evaluate("MATCH (v:Venue) RETURN count(*)")
                venueid += len(fnames)
                venue = Node("Venue", name=vname, id=venueid)
                self.graph.merge(venue)
                self.graph.merge(Relationship(paper, "Published_In", venue) | Relationship(venue, "Published_In", paper))
            else:
                venue = vexists
                self.graph.merge(Relationship(paper, "Published_In", vexists) | Relationship(vexists, "Published_In", paper))
            for i in range(len(f["authors"])-1):
                auth = Node("Author", name=f["authors"][i]["name"], org=f["authors"][i]["org"])
                self.graph.merge(auth)
                if auth not in nodeList:
                    nodeList.append(auth)
                self.graph.merge(Relationship(auth, "Authored", paper) | Relationship(paper, "Authored", auth))
                self.graph.merge(Relationship(auth, "Pubed", venue) | Relationship(venue, "Pubed", auth))
                for j in range(i+1, len(f["authors"])):
                    auth2 = Node("Author", name=f["authors"][j]["name"], org=f["authors"][j]["org"])
                    self.graph.merge(auth2)
                    if auth2 not in nodeList:
                        nodeList.append(auth2)
                    self.graph.merge(Relationship(auth2, "Authored", paper) | Relationship(paper, "Authored", auth2))
                    self.graph.merge(Relationship(auth2, "Pubed", venue) | Relationship(venue, "Pubed", auth2))
                    rel1 = Relationship(auth, "CoAuth", auth2)
                    rel2 = Relationship(auth2, "CoAuth", auth)
                    self.graph.merge(rel1 | rel2)
            for ref in f["references"]:
                pexists = self.graph.evaluate("MATCH (p:Paper {{jid:\"{0:s}\"}}) RETURN p".format(ref))
                if pexists is None:
                    if ref not in jsonidDict:
                        jsonidDict[ref] = [ f["id"] ]
                    else:
                        jsonidDict[ref].append(f["id"])
                else:
                    self.graph.merge(Relationship(pexists, "Cites", paper))
        self.numPapers = self.graph.evaluate("MATCH (p:Paper) RETURN count(*)")
        self.numVenues = self.graph.evaluate("MATCH (v:Venue) RETURN count(*)")
        for idx, node in enumerate(nodeList):
            node["id"] = idx + self.numPapers + self.numVenues
            self.graph.push(node)
        self.numAuthors = self.graph.evaluate("MATCH (a:Author) RETURN count(*)")

    def numNodes(self):
        return self.numPapers, self.numVenues, self.numAuthors

    def __getitem__(self, index):
        if index < self.numPapers:
            return self.graph.evaluate("MATCH (p:Paper {{id:{0:d} }}) RETURN p".format(index))
        elif index < self.numPapers+self.numVenues:
            return self.graph.evaluate("MATCH (v:Venue {{id:{0:d} }}) RETURN v".format(index))
        elif index < self.numPapers+self.numVenues+self.numAuthors:
            return self.graph.evaluate("MATCH (a:Author {{id:{0:d} }}) RETURN a".format(index))
        else:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))

    def __len__(self):
        return self.numPapers + self.numVenues + self.numAuthors

    def getAdj(self, index):
        adj = []
        if index < self.numPapers:
            label = "Paper"
        elif index < self.numPapers+self.numVenues:
            label = "Venue"
        elif index < self.numPapers+self.numVenues+self.numAuthors:
            label = "Author"
        else:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))
        cursor = self.graph.run("MATCH (a:{0:s} {{id:{1:d} }})-[]->(b) RETURN b.id".format(label, index))
        nodes = cursor.data()
        for n in nodes:
            adj.append(n["b.id"])
        adj.sort(reverse=True)
        return adj
