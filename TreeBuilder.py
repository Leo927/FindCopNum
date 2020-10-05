import queue
import random
import networkx as nx
import logging
from networkx.readwrite import json_graph
import json
import constant
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
        
        
        
        
        graph=nx.random_tree(int(numVertices))
        graph = nx.bfs_tree(graph,0)
        
        #convert to json and
        graphJson = json_graph.adjacency_data(graph)
        graphText = json.dumps(graphJson, indent=4)
        
        #write to file
        file = open(constant.treeFilePath, "w")
        file.write(graphText)
        file.close()
        
        
        #log the json. it is hooked up to the gui textbox
        logging.info(graphText)
        
        print(graphText)
        return graph
    
    @classmethod
    def fromFile(self,path, root):
        file = open(path, "r")
        graphJson = json.loads(file.read())
        graphJson['directed'] = False
        graph = json_graph.adjacency_graph(graphJson)
        tree = nx.bfs_tree(graph,root)
        return tree
    

def subTree(graph:nx.classes.graph.Graph,root:int):
    
    pass

