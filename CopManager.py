# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:53:45 2020

@author: Songhao Li
"""


import networkx as nx
import matplotlib.pyplot as plt

import TreeDrawer
import TreeBuilder
import constant

def reverseList(tree,root):
    reversedList = []
    tree = nx.bfs_tree(tree,root)
    __reverseListRecur(tree, root, reversedList)
    return reversedList

def __reverseListRecur(tree, root, output):    
    children = dict( nx.bfs_successors(tree,root,1))[root]    
    for child in children:
        __reverseListRecur(tree, child, output)    
    output.append(root)

def isKPreBranching(tree, node, k):
    
    return c1Star()

def subForest(tree, node, distance:int):
    grandChildren = tree.descendants_at_distance(tree,node,distance)
    forest = []
    for grandChild in grandChildren:
        forest.append(tree.bfs_tree(node))
        

#The minimum cop number to cover a tree
def c1(tree):
    #TODO - implement c1
    return 1
        
def c1Star(forest):
    result = 0
    for tree in forest:
        result = max(result, c1(tree))
    return result



    