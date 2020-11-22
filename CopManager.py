# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:53:45 2020

@author: Songhao Li
"""


import networkx as nx
from rootedtree import RootedTree
import matplotlib.pyplot as plt
import copy
import treedrawer
import constant
import random

def reverseList(rt):
    reversedList = []
    __reverseListRecur(rt.directed(), rt.root, reversedList)
    return reversedList

def __reverseListRecur(tree, root, output):    
    children = dict( nx.bfs_successors(tree,root,1))[root]    
    for child in children:
        __reverseListRecur(tree, child, output)    
    output.append(root)

def isKPreBranching(rt, node, k):    
    #TODO - test
    tree = rt.tree
    return (c1Star(subForest(tree, node, 2))==k and 
            c1(joinByU(tree,node))==k)

def isKWeaklyBranching(rt, node, k):    
    #TODO - test
    forests=[subForest(rt, node, 0),
             subForest(rt, node, 1),
             subForest(rt, node, 2)]
    #It is exactly one 
    numForestMeetCondition = 0
    for forest in forests:
        if sum(isKPreBranching(component.tree, component.root, k) == True 
               for component in forest) == 2:
            numForestMeetCondition += 1
    if numForestMeetCondition == 1:
        return True
    return False

def isKBranching(rt, node, k):
    #TODO - test
    right = True
    right &= c1Star(subForest(rt, node, 2))==k;
    right &= (sum(isKWeaklyBranching(rt, rt.root, k) 
                 for rooted_tree in subForest(rt, node, 2)) != 1)
    right &= (sum(isKWeaklyBranching(rt.tree,rt.root, k) 
                 for rooted_tree in subForest(rt, node, 3)) == 0)
    return right
    
def joinByU(rt):
    return RootedTree(nx.join([(rt.tree, rt.root), 
                               (rt.tree, rt.root)]),rt.root)
    
    
def subForest(rt, node, distance = 0):
    '''Return a forst of RootedTree by removing neigbhor of node 
    in given distance'''
    distance += 1
    digraph = nx.bfs_tree(rt.directed,node)
    children = nx.descendants_at_distance(digraph, node, distance)
    return [RootedTree(nx.bfs_tree(digraph,child),child) for child in children]
    

#The minimum cop number to cover a tree
def c1(rt):
    #TODO - implement c1
    return 1
        
def c1Star(forest):
    #TODO - test
    result = 0
    for rt in forest:
        result = max(result, c1(rt))
    return result

def neighbor(rt, node, distance = 1):
    #TODO - test
    return dict(nx.bfs_successors(rt.directed(),node,distance))[node]  

def kPreBranInd(rt, v, k):
    #TODO - test
    if c1(rt) < 1:
        raise Exception("c1(T) < 1")
    return int(isKPreBranching(rt, v, k))
    
def kWeakBranInd(rt, v, k):
    #TODO - test
    if c1(rt) < 1:
        raise Exception("c1(T) < 1")
    return int(isKWeaklyBranching(rt, v, k))

def kInitialCounter(rt, v, k):
    '''Definition 2.3 k-initial-counter'''
    #TODO - test
    if c1(rt) < 1:
        raise Exception("c1(T) < 1")
    if(kPreBranInd(rt, v, k) == 0 and c1Star(subForest(rt, v, 0)) == k-1):
        return 0
    elif (kPreBranInd(rt, v, k) == 0 and 
          c1Star(subForest(rt, v, 1)) == k-1 and
         c1Star(subForest(rt, v)) == k):
        return 1
    elif (kPreBranInd(rt, v, k) == 0 and
          c1Star(subForest(rt, v, 2)) == k - 1 and
          c1Star(subForest(rt, v, 1)) == k):
        return 2
    else:
        return 0
    
def kWeakCounter(rt, v, k):
    '''Definition 2.3 find k-weakly-counter'''
    #TODO - test
    if (kWeakBranInd(rt, v, k) == 1):
        k_pre_branching_child = [child for child in neighbor(rt, v) 
                                 if isKPreBranching(rt, child, k)]
        k_weakly_branching_child = [child for child in neighbor(rt, v) 
                                    if isKWeaklyBranching(rt, v, k)]
        num_prebranching_child = len(k_pre_branching_child)
        num_weakly_bran_child = len(k_weakly_branching_child)
        
        if (num_prebranching_child == 2 and 
            num_weakly_bran_child == 0):
            return 0
        elif (num_weakly_bran_child == 1 and 
              kWeakCounter(rt, k_weakly_branching_child[0], k) == 0):
            return 1
        elif (num_weakly_bran_child == 1 and 
              kWeakCounter(rt, k_weakly_branching_child[0], k) == 1):
            return 2       
    
        return 0
    

def compLabel(rt, v):
    '''Definition 2.4 label of v in T[v]'''
    
    if len(rt) == 1:
        return [(1, constant.branSym), 0, 0, 0, 0]
    else:
        i = 1
        T1 = rt
    s = list(len(rt) + 1)
    s[i] = c1(T1)
    
    if isKBranching(T1, v, s[i]):
        return [()]+[0,0,0,0]
    #TODO - implement
    #TODO - test

def L(rt):
    revNodes = reverseList(rt)
    
    labels = dict((node, None) for node in revNodes)
    
    

    
    