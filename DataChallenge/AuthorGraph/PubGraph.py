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
        nodeList = []
        jsonidDict = {}
        venueid = len(fnames)
        for idx, fn in enumerate(fnames):
            o = open(fn, "r")
            f = json.load(o)
            paper = Node("Paper", title=f["title"], jid=f["id"], id=idx)
            self.graph.merge(paper)
            if f["id"] in jsonidDict:
                for jid in jsonidDict[f["id"]]:
                    citer = self.graph.evaluate("MATCH (p:Paper {{jid:\"{0:s}\"}}) RETURN p".format(jid))
                    self.graph.merge(Relationship(citer, "Cites", paper))
            vexists = self.graph.evaluate("MATCH (v:Venue {{name:\"{0:s}\"}}) RETURN v".format(f["venue"]))
            if vexists is None:
                venue = Node("Venue", name=f["venue"], id=venueid)
                venueid += 1
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
                    self.graph.merge(Relationship(paper, "Cites", pexists))
        for idx, node in enumerate(nodeList):
            node["id"] = idx + venueid
            self.graph.push(node)
        self.numNodes = len(nodeList)

