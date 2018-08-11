from py2neo import Graph, Node, Relationship
import json

class PubGraph:

    """
    PubGraph

    This class creates the Publication Graph for determining experts. It uses the neo4j
    graph database and the corresponding py2neo Python library. It also provides a way
    to easily access the graph's data and a node's adjacencies.
    """

    def __init__(self, fnames, pswd, bolt=None, secure=False, host="localhost", portNum=7474, portType="http", user="neo4j"):
        """
        Creates the Publication Graph using the paper JSONs in fnames.
        
        Parameters:
        * fnames: a list of absolute paths to the JSON files to be used in making the graph
        * pswd: the password for the neo4j database to be used
        * bolt (Default = None): specifies whether to use the Bolt protocol for connection (None means autodetect). This is not needed for py2neo v4.0 or higher, as it uses bolt by default.
        * secure (Default = False): specifies whether to use a secure connection
        * host (Default = \"localhost\"): specifies the database server host name, which is \"localhost\" by default in neo4j.
        * portNum (Default = 7474): specifies the database server port, which is 7474 by default for an http connection in neo4j.
          - Note: In py2neo v4.0, the default connection type is bolt, not http. As a result, portnum should probably be set to 7687.
        * portType (Default = \"http\"): specifies the type of port that you want to use. Can be \"bolt\", \"https\", or \"http\". If set to a different value, it will assume \"http\".
          - Note: In py2neo v4.0, the default connection type is bolt. As a result, it is best to set portType to \"bolt\", although you can still use the others.
        * user (Default = \"neo4j\"): the user used to authenticate the connection to the neo4j database.
        """
        # Initializes the neo4j graph
        if portType == "bolt":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, bolt_port=portNum, user=user, password=pswd)
        elif portType == "https":
            self.graph = Graph(bolt=bolt, secure=secure, host=host, https_port=portNum, user=user, password=pswd)
        else:
            self.graph = Graph(bolt=bolt, secure=secure, host=host, http_port=portNum, user=user, password=pswd)
        # Creates constraints so that the id numbers must be unique
        self.graph.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.id IS UNIQUE")
        self.graph.run("CREATE CONSTRAINT ON (v:Venue) ASSERT v.id IS UNIQUE")
        self.graph.run("CREATE CONSTRAINT ON (p:Paper) ASSERT p.id IS UNIQUE")
        # nodeList stores the author nodes of the graph so that their ids can be added later
        nodeList = []
        # jsonidDict is used to store citations between a paper in the graph and a paper not yet in the graph.
        # Each element has the cited paper as the key and a list of papers that cite the cited paper as the data.
        jsonidDict = {}
        for idx, fn in enumerate(fnames):
            # Opens the current JSON and adds the paper it represents to the graph if it is not already present
            f = json.loads(fn)
            paper = Node("Paper", title=f["title"], jid=f["id"], id=idx)
            self.graph.merge(paper)
            # If other papers have cited this paper, add the citations as directed edges from the cited paper to the citing papers.
            if f["id"] in jsonidDict:
                for jid in jsonidDict[f["id"]]:
                    citer = self.graph.evaluate("MATCH (p:Paper {{jid:\"{0:s}\"}}) RETURN p".format(jid))
                    if citer is not None:
                        self.graph.merge(Relationship(paper, "Cites", citer))
            # Obtain the "venue name"
            if "venue" in f:
                vname = f["venue"]
            elif "isbn" in f:
                vname = "{0:s} {1:s}".format(f["publisher"], f["isbn"])
            else:
                vname = "{0:s} {1:s}".format(f["publisher"], f["doc_type"])
            # Check if the venue already has a node in the graph
            vexists = self.graph.evaluate("MATCH (v:Venue {{name:\"{0:s}\"}}) RETURN v".format(vname))
            # If the venue is not in the graph, add it to the graph, and add an undirected edge between it and the paper published in it.
            if vexists is None:
                venueid = self.graph.evaluate("MATCH (v:Venue) RETURN count(*)")
                venueid += len(fnames)
                venue = Node("Venue", name=vname, id=venueid)
                self.graph.merge(venue)
                self.graph.merge(Relationship(paper, "Published_In", venue) | Relationship(venue, "Published_In", paper))
            # If the venue is in the graph, add an undirected edge between its node and the paper published in it.
            else:
                venue = vexists
                self.graph.merge(Relationship(paper, "Published_In", vexists) | Relationship(vexists, "Published_In", paper))
            for i in range(len(f["authors"])-1):
                # Creates a node in the graph for the current author if a node doesn't already exist
                auth = Node("Author", name=f["authors"][i]["name"], org=f["authors"][i]["org"])
                self.graph.merge(auth)
                # Adds the node to nodeList if it isn't already present
                if auth not in nodeList:
                    nodeList.append(auth)
                # Adds undirected edges between the author and the current paper and venue
                self.graph.merge(Relationship(auth, "Authored", paper) | Relationship(paper, "Authored", auth))
                self.graph.merge(Relationship(auth, "Pubed", venue) | Relationship(venue, "Pubed", auth))
                # This for loop associates the current author with all other authors in the paper
                for j in range(i+1, len(f["authors"])):
                    # Creates a node in the graph for the current author if a node doesn't already exist
                    auth2 = Node("Author", name=f["authors"][j]["name"], org=f["authors"][j]["org"])
                    self.graph.merge(auth2)
                    # Adds the node to nodeList if it isn't already present
                    if auth2 not in nodeList:
                        nodeList.append(auth2)
                    # Adds undirected edges between the author and the current paper and venue
                    self.graph.merge(Relationship(auth2, "Authored", paper) | Relationship(paper, "Authored", auth2))
                    self.graph.merge(Relationship(auth2, "Pubed", venue) | Relationship(venue, "Pubed", auth2))
                    # Adds a undirected edge between the two authors because they are co-authors
                    rel1 = Relationship(auth, "CoAuth", auth2)
                    rel2 = Relationship(auth2, "CoAuth", auth)
                    self.graph.merge(rel1 | rel2)
            # Adds the references
            for ref in f["references"]:
                pexists = self.graph.evaluate("MATCH (p:Paper {{jid:\"{0:s}\"}}) RETURN p".format(ref))
                # If the cited paper is not already in the graph, adds the current and cited papers to jsonidDict.
                if pexists is None:
                    if ref not in jsonidDict:
                        jsonidDict[ref] = [ f["id"] ]
                    else:
                        jsonidDict[ref].append(f["id"])
                # Otherwise, creates a directed edge from the cited paper to the current paper
                else:
                    self.graph.merge(Relationship(pexists, "Cites", paper))
        # Sets member variables for number of papers and venues
        self.numPapers = self.graph.evaluate("MATCH (p:Paper) RETURN count(*)")
        self.numVenues = self.graph.evaluate("MATCH (v:Venue) RETURN count(*)")
        # Adds the ids for all the author nodes
        for idx, node in enumerate(nodeList):
            node["id"] = idx + self.numPapers + self.numVenues
            self.graph.push(node)
        # Sets member variable for number of authors
        self.numAuthors = self.graph.evaluate("MATCH (a:Author) RETURN count(*)")

    def numNodes(self):
        """
        Returns the tuple (Number of Papers, Number of Venues, Number of Authors)
        """
        return self.numPapers, self.numVenues, self.numAuthors

    def __getitem__(self, index):
        """
        Returns the py2neo Node object with the provided index. If the index is not in the graph, raises an IndexError.

        Parameters:
        * index: an integer corresponding to an id in the graph
        """
        if index < self.numPapers:
            return self.graph.evaluate("MATCH (p:Paper {{id:{0:d} }}) RETURN p".format(index))
        elif index < self.numPapers+self.numVenues:
            return self.graph.evaluate("MATCH (v:Venue {{id:{0:d} }}) RETURN v".format(index))
        elif index < self.numPapers+self.numVenues+self.numAuthors:
            return self.graph.evaluate("MATCH (a:Author {{id:{0:d} }}) RETURN a".format(index))
        else:
            raise IndexError("Index must be less than {0:d}".format(self.numPapers+self.numVenues+self.numAuthors))

    def __len__(self):
        """
        Returns the number of nodes in the graph
        """
        return self.numPapers + self.numVenues + self.numAuthors

    def getAdj(self, index):
        """
        Generates a list of node ids for the nodes that are adjacent to the node represented by index.
        If the index is not in the graph, raises an IndexError.

        Parameters:
        * index: an integer corresponding to an id in the graph

        Returns: a list of node id values corresponding to the adjacencies of the desired node.
        """
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
        # This guarantees that there are no duplicates in adj.
        adj = list(set(adj))
        adj.sort(reverse=True)
        return adj
