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

def reverseList(tree,root):
    reversedList = []
    __reverseListRecur(tree, root, reversedList)
    return reversedList

def __reverseListRecur(tree, root, output):    
    children = dict( nx.bfs_successors(tree,root,1))[root]    
    for child in children:
        __reverseListRecur(tree, child, output)    
    output.append(root)


        
    
    