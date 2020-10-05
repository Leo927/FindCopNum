# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:53:45 2020

@author: Songhao Li
"""


import networkx as nx
import matplotlib.pyplot as plt

from TreeDrawer import Drawer
from TreeBuilder import Builder
import constant



class CopManager(object):
    
    def __init__(self, _tree):
        super().__init__()
        self.tree = _tree
        return
    
    @classmethod()
    def findCopNumber(self):
        pass
    
    @classmethod()
    def findLabel(self,node):
        pass
    
    #T[v]-N^k[v]
    @classmethod()
    def kthForest(self,tree,k):
        return nx.dfs_tree()
    
    #k-th close neighber
    @classmethod()
    def kthCloseNeighber(self,tree,k):
        return nx.dfs_tree(tree,self.find_root(tree,tree.nodes))
    
    @classmethod()
    def findRoot(self,G):
        return self.findRootRecursive(G, G.nodes[1])
    
    @classmethod()
    def findRootRecursive(self,G,child):
        parent = list(G.predecessors(child))
        if len(parent) == 0:
            print(f"found root: {child}")
            return child
        else:  
            return self.findRootRecursive(G, parent[0])
        
    @classmethod()
    