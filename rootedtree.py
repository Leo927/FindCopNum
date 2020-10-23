import queue
import random
import networkx as nx
import logging
from networkx.readwrite import json_graph
import json
import constant
from collections import namedtuple

class RootedTree:    
    '''represents a rooted tree
        tree is networkx.Graph()'''
    def __init__(self, tree, root):
        self.tree = tree
        self.root = root
        self.attr = "weight"
    
    @classmethod
    def random(cls, numVertices:int):
        '''Return a random tree of given size'''
        if numVertices <= 0:
            return nx.Graph()    
        
        graph=nx.random_tree(int(numVertices))
        return cls(graph, 0)
    
    @classmethod
    def load(cls, root, path=constant.treeFilePath):
        '''Return a tree with tree in a file and a root as given'''
        file = open(path, "r")
        graphJson = json.loads(file.read())
        graphJson['directed'] = False
        graph = json_graph.adjacency_graph(graphJson)
        return cls(graph, root)
        
        
    def save(self):
        '''Save the tree to a .txt file'''
        #convert to json and
        graphJson = json_graph.adjacency_data(self.tree)
        graphText = json.dumps(graphJson, indent=4)
        
        #write to file
        file = open(constant.treeFilePath, "w")
        file.write(graphText)
        file.close()        
        logging.info(graphText)    
    
    def add_rand_weight(self):
        '''Add randome weight between 1 and n/10 for every node in a RootedTree'''
        lowerBound = 1
        upperBound = len(self.tree.nodes())/10
        attribute = {}
        for node in self.tree.nodes():
            attribute[node] = random.randint(lowerBound, upperBound)
        nx.set_node_attributes(self.tree, attribute, "weight")
        self.save()    
        self.attr = "weight"
        
    def add_long_weight(self, start):
        '''Add weight to nodes in a RootedTree so that longer paths are formed'''
        #TODO - Implement
        lowerBound = 1
        upperBound = len(self.tree.nodes())/10
        digraph= nx.dfs_tree(self.tree, start)
        
        node_visited = dict((key, False) for key in digraph.nodes())
        #create a queue and push the starting node
        to_visit = queue.Queue()
        to_visit.put(start)
        attribute = {}
        attribute[start] = random.randint(lowerBound, upperBound)
        #do the traversal
        while to_visit.empty()==False:
            node = to_visit.get()
            
            children = dict( nx.bfs_successors(digraph,node,1))[node]  
            if len(children)<=0:
                continue
            
            heir = children[random.randint(0, len(children)-1)]
            
            for cNode in children:               
                if node_visited[cNode] ==False:
                    node_visited[cNode] = True
                    to_visit.put(cNode)
                    if (cNode==heir):
                        attribute[cNode] = attribute[node]
                    else:
                        attribute[cNode] = random.randint(lowerBound, upperBound)
        nx.set_node_attributes(self.tree, attribute, "weight")
        
        