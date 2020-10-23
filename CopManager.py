# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:53:45 2020

@author: Songhao Li
"""


import networkx as nx
import matplotlib.pyplot as plt
import copy
import treedrawer
import treebuilder
import constant
import random

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
    #TODO - test
    return c1Star(subForest(tree, node, 2))==k and c1(joinByU(tree,node))==k

def isKWeaklyBranching(tree, node, k):    
    #TODO - test
    forests=[subForest(tree, node, 0),subForest(tree, node, 1),subForest(tree, node, 2)]
    #It is exactly one 
    numForestMeetCondition = 0
    for forest in forests:
        if sum(isKPreBranching(component.tree, component.root, k) == True for component in forest) == 2:
            numForestMeetCondition += 1
    if numForestMeetCondition == 1:
        return True
    return False

def isKBranching(tree, node, k):
    #TODO - test
    right = True
    right &= c1Star(subForest(tree, node, 2))==k;
    right &= sum(isKWeaklyBranching(rooted_tree.tree, rooted_tree.root, k) for rooted_tree in subForest(tree, node, 2)) != 1
    right &= sum(isKWeaklyBranching(rooted_tree.tree,rooted_tree.root, k) for rooted_tree in subForest(tree, node, 3)) == 0
        
    
def joinByU(rooted_tree):
    return treebuilder.rooted_tree(nx.join([(rooted_tree.tree, rooted_tree.root), (rooted_tree.tree, rooted_tree.root)]),0)
    
    
def subForest(tree, node, distance:int):
    distance += 1
    digraph = nx.bfs_tree(tree,node)
    children = nx.descendants_at_distance(digraph, node, distance)
    return [treebuilder.rooted_tree(nx.bfs_tree(digraph,child),child) for child in children]
    

#The minimum cop number to cover a tree
def c1(tree):
    #TODO - implement c1
    return 1
        
def c1Star(forest):
    #TODO - test
    result = 0
    for tree in forest:
        result = max(result, c1(tree))
    return result


    
def findConnectedNodes(rooted_tree, node, data=False):
    return dict( nx.bfs_successors(rooted_tree.tree,node,1))[node]  

def getWeight(rooted_tree, node):
    return rooted_tree.tree.nodes(True)[node]['weight']

def findLongestEqualWeightPath(rooted_tree, node):
    return __findLongestEqualWeightPath(rooted_tree, None, node)

def __findLongestEqualWeightPath(rooted_tree, parent, node):
    connectedNodes = findConnectedNodes(rooted_tree, node)
    
    longestPath = []    
    for cNode in connectedNodes:
        if cNode == parent:
            continue
        if getWeight(rooted_tree, cNode) == getWeight(rooted_tree, node):
            path = __findLongestEqualWeightPath(rooted_tree, node, cNode)
            if len(path)>len(longestPath):
                longestPath = path
    longestPath.append(node)
    return longestPath
    #find all nodes that are connected to node
    
    #foreach nodes that has the same weight
        #call this function with these nodes and store the return value
    #return the longest list among the returned list and empty list
    pass


    