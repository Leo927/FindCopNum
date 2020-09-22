import queue
import random
import networkx as nx
import logging
from networkx.readwrite import json_graph
import json
    ###########################
class Builder(object):
    sparesRatio :float = 0.2
    childLimit :int = 10
    minChild :int =3
    def __init__(self,_sparesRatio=None, _childLimit=None,_minChild=None):
        if _sparesRatio!=None:
            self.sparesRatio = _spares_ratio
        if _maxChild!=None:
            self.childLimit = _childLimit
        if _minChild!=None:
            self.minChild = _minChild
        return super().__init__(*args, **kwargs)
    
    @classmethod
    def getRandom(self, numVertices:int):
        if numVertices <= 0:
            return nx.Graph()

        

        numVertices-=1

        #calculate maxChild
        maxChild = min(int(numVertices * self.sparesRatio),self.childLimit)
        if maxChild < self.minChild:
            maxChild = self.minChild

        #put the root node onto the graph
        graph = nx.DiGraph()
        graph.add_node(0)
        
        currentNumVertices = 1

        #create a queue and enqueue root node
        toVisit = queue.SimpleQueue()
        toVisit.put(0)
    
        while toVisit.empty() == False and currentNumVertices <= numVertices:
            #get one node from the queue
            node = toVisit.get()
            #calculate number of child for this node
            numChild = int(min(random.random() * maxChild,numVertices - currentNumVertices))

            if numChild == 0:
                children = []

                #if the queue is drained and there isn't enough vertices yet
                if toVisit.empty() and currentNumVertices <= numVertices:
                    #add one vertex to the graph
                    graph.add_edge(node,currentNumVertices)
                    toVisit.put(currentNumVertices)
                    currentNumVertices += 1
            else:
                children = list(range(currentNumVertices, currentNumVertices + numChild))
                for child in children:
                    graph.add_edge(node,child)
                    toVisit.put(child)
                currentNumVertices+=numChild    
        
        #convert to json and
        graphJson = json_graph.adjacency_data(graph)
        graphText = json.dumps(graphJson, indent=4)
        
        #log the json. it is hooked up to the gui textbox
        logging.info(graphText)
        
        print(graphText)
        return graph

    @classmethod
    def fromString(input:str):
        pass

def subTree(graph:nx.classes.graph.Graph,root:int):
    
    pass


Builder.getRandom(20)