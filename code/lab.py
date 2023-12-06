from collections import deque

class DiGraphLL:
    def __init__(self):
        """Every node is an element in the dictionary.
        The key is the node id and the value is a dictionary
        with second node as key and the weight as value
        """
        self.__nodes = dict()

    def insertNode(self, node):
        test = self.__nodes.get(node, None)

        if test == None:
            self.__nodes[node] = {}
            #print("Node {} added".format(node))

    def insertEdge(self, node1, node2, weight):
        test = self.__nodes.get(node1, None)
        test1 = self.__nodes.get(node2, None)
        if test != None and test1 != None:
            #if both nodes exist othewise don't do anything
            test = self.__nodes[node1].get(node2, None)
            if test != None:
                exStr = "Edge {} --> {} already existing.".format(node1,node2)
                raise Exception(exStr)
            else:
                #print("Inserted {}-->{} ({})".format(node1,node2,weight))
                self.__nodes[node1][node2] = weight

    def deleteNode(self, node):
        test = self.__nodes.get(node, None)
        if test != None:
            self.__nodes.pop(node)
        # need to loop through all the nodes!!!
        for n in self.__nodes:
            test = self.__nodes[n].get(node, None)
            if test != None:
                self.__nodes[n].pop(node)

    def deleteEdge(self, node1,node2):
        test = self.__nodes.get(node1, None)
        if test != None:
            test = self.__nodes[node1].get(node2, None)
            if test != None:
                self.__nodes[node1].pop(node2)

    def __len__(self):
        return len(self.__nodes)

    def nodes(self):
        return list(self.__nodes.keys())

    def graph(self):
        return self.__nodes

    def __str__(self):
        ret = ""
        for n in self.__nodes:
            for edge in self.__nodes[n]:
                ret += "{} -- {} --> {}\n".format(str(n),
                                                  str(self.__nodes[n][edge]),
                                                  str(edge))
        return ret

    def adjacent(self, node):
        """returns a list of nodes connected to node"""
        ret = []
        test = self.__nodes.get(node, None)
        if test != None:
            for n in self.__nodes:
                if n == node:
                    #all outgoing edges
                    for edge in self.__nodes[node]:
                        ret.append(edge)
                else:
                    #all incoming edges
                    for edge in self.__nodes[n]:
                        if edge == node:
                            ret.append(n)
        return ret

    def adjacentEdge(self, node, incoming = True):
        """
        If incoming == False
        we look at the edges of the node
        else we need to loop through all the nodes.
        An edge is present if there is a
        corresponding entry in the dictionary.
        If no such nodes exist returns None
        """
        ret = []
        if incoming == False:
            edges = self.__nodes.get(node,None)
            if edges != None:
                for e in edges:
                    w = self.__nodes[node][e]
                    ret.append((node, e, w))
                return ret
        else:
            for n in self.__nodes:
                edge = self.__nodes[n].get(node,None)
                if edge != None:
                    ret.append((n,node, edge))
            return ret

    def edges(self):
        """Returns all the edges in a list of triplets"""
        ret = []
        for node in self.__nodes:
            for edge in self.__nodes[node]:
                w = self.__nodes[node][edge]
                ret.append((node,edge, w))
        return ret

    def edgeIn(self,node1,node2):
        """Checks if edge node1 --> node2 is present"""
        n1 = self.__nodes.get(node1, None)
        if n1 != None:
            n2 = self.__nodes[node1].get(node2, None)
            if n2 != None:
                return True
            else:
                return False
        else:
            return False
        



class DiGraphLLAnalyzer(DiGraphLL):
    """
        Every node is an element in the dictionary.
        The key is the node id and the value is a dictionary
        with key second node and value the weight
    """

    def getTopConnected_incoming(self):

        topN = ""
        #accumulator to count connections
        conn = [0]*len(self.nodes())
        for node in self.nodes():
            for el in self.graph()[node]:
                elInd = self.nodes().index(el)
                conn[elInd] +=1
        M = max(conn)
        ind = [x for x in range(len(conn)) if conn[x] == M]
        return [self.nodes()[x] for x in ind]

    def getTopConnected_outgoing(self):
        """Returns the node(s)"""
        topN = []
        conn = -1

        for node in self.nodes():
            n = len(self.graph()[node])
            if n > conn:
                topN = [node]
                conn = n
            else:
                if n == conn:
                    topN.append(node)

        return topN

    def hasPathAux(self, node1,node2):
        if node1 not in self.nodes() or node2 not in self.nodes():
            return False
        else:
            Q = deque()
            Q.append(node1)
            visited = set()
            while len(Q) > 0:
                curN = Q.popleft()
                #do not travel on already visited nodes
                if curN not in visited:
                    visited.add(curN)
                    #get all outgoing nodes of Q
                    for edge in self.graph()[curN]:
                        if edge == node2:
                            return True
                        else:
                            Q.append(edge)

            return False

    def hasPath(self, node1, node2):
        #checks both paths and returns True or false
        res = self.hasPathAux(node1,node2)
        if res:
            return True
        else:
            return self.hasPathAux(node2,node1)


    def DFSvisit(self, root, preorder = True, visited = set()):
        visited.add(root)
        if preorder:
            print("{}".format(root))
        #remember that the self.adjacentEdge method returns:
        #[('node1','node2', weight1), ...('node1', 'nodeX', weightX)]
        outGoingEdges = self.adjacentEdge(root, incoming = False)
        nextNodes = []
        if len(outGoingEdges) > 0:
            nextNodes = [x[1] for x in outGoingEdges]
            #print(nextNodes)
            for nextN in nextNodes:
                if nextN not in visited:
                    print("\tfrom {} --> {}".format(root, nextN))
                    self.DFSvisit(nextN, preorder, visited)
        if not preorder:
            print("{}".format(root))
        return visited

    def DFS(self):
        print("Nodi visitati ", visited)
        nodo_mancante = visited.intersection()



if __name__ == "__main__":
    G = DiGraphLLAnalyzer()
    for i in range(1,11):
        G.insertNode("Node_" + str(i))

    G.insertEdge("Node_1", "Node_2",1)
    G.insertEdge("Node_2", "Node_1",1)
    G.insertEdge("Node_1", "Node_3",1)
    G.insertEdge("Node_1", "Node_5",1)
    G.insertEdge("Node_2", "Node_3",1)
    G.insertEdge("Node_2", "Node_5",1)
    G.insertEdge("Node_3", "Node_4",1)
    G.insertEdge("Node_3", "Node_6",1)
    G.insertEdge("Node_5", "Node_3",1)
    G.insertEdge("Node_5", "Node_5",1)
    G.insertEdge("Node_6", "Node_4",1)
    G.insertEdge("Node_6", "Node_6",1)
    G.insertEdge("Node_7", "Node_5",1)
    G.insertEdge("Node_5", "Node_8",1)
    G.insertEdge("Node_8", "Node_7",1)
    G.insertEdge("Node_9", "Node_2",1)
    

    print("Preorder:")
    G.DFSvisit("Node_1", preorder = True, visited = set())              # visito preorder
    print("\nPostorder:")
    G.DFSvisit("Node_1", preorder = False, visited = set())             # visito postorder

    print("\nPreorder from Node_9")
    visited = G.DFSvisit("Node_9", preorder = True, visited = set())

    print("NUMERO DI NODI: ", len(G.nodes()))
    print("Nodi: ", G.nodes())
    print("NUMERO DI VISITATI: ", len(visited))
    print("Nodi visitati ", visited)

    all_nodes = set(G.nodes())
    all_nodes = [str(x) for x in all_nodes]
    visited = [str(x) for x in visited]

    all_nodes = set(all_nodes)
    visited = set(visited)

    c = all_nodes.symmetric_difference(visited)
    print(c)
    #G.DFS()




    

    