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
        self.attr = None
    
    @classmethod
    def random(cls, numVertices:int):
        '''Return a random tree of given size'''
        if numVertices <= 0:
            return nx.Graph()    
        
        graph=nx.random_tree(int(numVertices))
        return cls(graph, 0)
    
    def __len__(self):
        return len(self.tree)
    
    @classmethod
    def load(cls, root, path=constant.treeFilePath):
        '''Return a tree with tree in a file and a root as given'''
        graph = nx.read_adjlist(constant.treeFilePath)
        mapping = dict((node, int(node)) for node in graph.nodes)
        graph = nx.relabel_nodes(graph, mapping)
        return cls(graph, root)
    
    @property
    def directed(self):
        return nx.dfs_tree(self.tree, self.root)
    
    def subTree(self, v1):
        '''return a subtree rooted at v1'''
        return RootedTree(nx.dfs_tree(self.tree, v1), v1)
         
    def save(self):
        '''Save the tree to a .txt file'''
        #convert to json and
        nx.write_adjlist(self.directed, constant.treeFilePath)  
    
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
        
        