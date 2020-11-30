import queue
import random
import networkx as nx
import logging
from networkx.readwrite import json_graph
import json
import constant
from collections import namedtuple
import numpy
import copy


class RootedTree:
    '''represents a rooted tree
        tree is networkx.Graph()'''

    def __init__(self, tree, root, labels:dict = None):
        self.tree = tree
        self.root = root
        self.attr = None
        self.labels = labels

    def __str__(self):
        return f'root: {self.root}\n {self.tree.nodes}\nlabels={self.labels}'

    def __repr__(self):
        return str(self)

    @classmethod
    def random(cls, numVertices: int):
        '''Return a random tree of given size'''
        if numVertices <= 0:
            return nx.Graph()

        graph = nx.random_tree(int(numVertices))
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
        return RootedTree(nx.dfs_tree(self.directed, v1), v1, self.labels)
    
    @property
    def nodes(self):
        return self.tree.nodes

    def save(self):
        '''Save the tree to a .txt file'''
        # convert to json and
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
        digraph = nx.dfs_tree(self.tree, start)

        node_visited = dict((key, False) for key in digraph.nodes())
        # create a queue and push the starting node
        to_visit = queue.Queue()
        to_visit.put(start)
        attribute = {}
        attribute[start] = random.randint(lowerBound, upperBound)
        # do the traversal
        while to_visit.empty() == False:
            node = to_visit.get()

            children = dict(nx.bfs_successors(digraph, node, 1))[node]
            if len(children) <= 0:
                continue

            heir = children[random.randint(0, len(children)-1)]

            for cNode in children:
                if node_visited[cNode] == False:
                    node_visited[cNode] = True
                    to_visit.put(cNode)
                    if (cNode == heir):
                        attribute[cNode] = attribute[node]
                    else:
                        attribute[cNode] = random.randint(
                            lowerBound, upperBound)
        nx.set_node_attributes(self.tree, attribute, "weight")
    def reverseList(self):
        reversedList = []
        __reverseListRecur(self.directed, self.root, reversedList)
        return reversedList

        
    def descendant(self, node, distance=1):
        '''return descendant within distance(default = 1)
        does not include node it self'''
        pairs = dict(nx.bfs_successors(self.directed, node, depth_limit=distance))
        children = []
        for key in pairs:
            children = pairs[key] + children
        return children

    

    def trimTreeFromNode(self, *arg):
        '''return a copy of the trimmed rooted tree'''
        #TODO - test
        tempTree = copy.deepcopy(self)
        for v in arg:
            nodesToRemove = self.subTree(v).tree.nodes
            tempTree.tree.remove_nodes_from(nodesToRemove)
        return tempTree

    def subForest(self, node, distance=0):
        '''Return a forst of RootedTree by removing neigbhor of node 
        in given distance'''
        distance += 1
        children = nx.descendants_at_distance(self.directed, node, distance)
        return [RootedTree(nx.bfs_tree(self.directed, child), child, self.labels) for child in children]








def __reverseListRecur( tree, root, output):
    children = dict(nx.bfs_successors(tree, root, 1))[root]
    for child in children:
        __reverseListRecur(tree, child, output)
    output.append(root)
