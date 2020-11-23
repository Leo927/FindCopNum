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

class SV:
    def __init__(self, s, v):
        self.s = s 
        self.v = v

class Label:
    
    def __init__(self):
        self.sv = []
        self.ind = [None for i in range(5)]
        
    def __index__(self, i):
        return self.sv[i-1]#compensate for 1 start
    
    def append(self, s = None, v=None):
        self.sv.append(SV(s,v))
    
    @property
    def value(self):
        return self[1].s


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
    


def c1(rt):
    '''find cop number of a rooted tree'''
    return LTv(rt,rt.root).value
        
def c1Star(forest):
    #TODO - test
    result = 0
    for rt in forest:
        result = max(result, c1(rt))
    return result

def descendant(rt, node, distance = 1):
    '''return descendant within distance(default = 1)
    does not include node it self'''
    #TODO - test
    return dict(nx.bfs_successors(rt.directed,node,distance))[node]  

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
        k_pre_branching_child = [child for child in descendant(rt, v) 
                                 if isKPreBranching(rt, child, k)]
        k_weakly_branching_child = [child for child in descendant(rt, v) 
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

def descOfType(rt, v, k, func):
    '''return the list of children of v that meet a condition'''
    nodes = descendant(rt, v) 
    return [node for node in nodes if func(rt, v, k)]

def numKPreBranChild(rt, v, k):
    '''Definiton 2.6 return the number of descendants that are k-pre-branching vertex
    #^k_pb(T^[u] - u)'''    
    #TODO - test
    return len(descOfType(rt, v, k, isKPreBranching))
    
def numKWeakBranChild(rt, v, k):
    '''Definition 2.6 return the number of descendents 
    #^k_wb(T^[u] - u)'''
    #TODO - test
    return len(descOfType(rt, v, k, isKWeaklyBranching))
    
def numKC1Child(rt, v, k):
    '''Definiton 2.6
    #_c^k(T^[u] - u) = |{j for c1(T^[vj]) =k for vj in u.children'''
    #TODO - test
    return len(descOfType(rt, v, k, lambda vj: c1(rt.subTree(vj)) == k))

def maxInitialCounter(rt, v, k):
    '''Definiton 2.6
    h^k(T^[u] - u) = max{J^k(vj) for j in v.chidren'''
    return max([kInitialCounter(rt, vj, k) for vj in descendant(rt, v)])

def maxWeaklyCounter(rt, v, k):
    '''Definiton 2.6
    h^k_w(T^[u] -u)) = max{J^k_w(vj) for vj in v.children}'''
    return max([kWeakCounter(rt, vj, k) for vj in descendant(rt, v)])

def getCopNumber(tree, root = None):
    if(len(tree) < 12):
        raise Exception('number of vertices in tree must be at least 12');
    if(root == None):
        root = tree.nodes[random.randint(0, len(tree) - 1)]
    rt = RootedTree(tree, root)
    revNodes = reverseList(rt)
    labels = [None for node in revNodes]
    

@DeprecationWarning
def LTv(rt, v_origin):
    '''Definition 2.4 label of v in T[v]'''
    #TODO - test
    if len(rt) == 1:
        return [(1, constant.PERPEN_SYM), 0, 0, 0, 0]
    
    v = copy.deepcopy(v_origin)
    T1 = copy.deepcopy(rt)
    label = Label()
    while(True):
        i = 1        
        label.append()
        label[i].s = c1(T1)
        #(a)
        if (isKBranching(rt, v, label[i].s)):
            label[i].v = v
            label.ind = [0,0,0,0]
            return label
        
        #(b)
        si_branching_descendants = kBranchingDescendent(rt, v, label[i].s)
        if (len(si_branching_descendants) > 0):
            label[i].v = si_branching_descendants[0]
            T1 = trimTreeFromNode(T1, label[i].v)
            i += 1
            continue
        
        #(c)
        if (isKWeaklyBranching(T1, v, label[i].s)):
            label[i].v = constant.PERPEN_SYM
            #TODO - not sure the counter is based on T1 or T
            label.ind = [1, kWeakCounter(T1, v, label[i].s), 0, 0]
            return label
        
        #(d)
        if (isKPreBranching(T1, v, label[i].s)):
            label[i].v = constant.PERPEN_SYM
            label.ind = [0,0,1,0]
            return label
            
        #(e)
        label[i].v = constant.PERPEN_SYM
        label.ind = [0,0,0,kInitialCounter(T1, v, label[i].s)]
        

def kBranchingDescendent(rt, v, k):    
    descendents = nx.bfs_successors(rt.directed, v)
    return [node for node in descendents if isKBranching(rt, v, k)]

def trimTreeFromNode(rt, v):
    #TODO - test
    tempTree = copy.deepcopy(rt)
    nodesToRemove = nx.dfs_tree(rt.directed, v).nodes
    tempTree.tree.remove_nodes_from(nodesToRemove)
    return tempTree
    

rt = RootedTree.load(1)
treedrawer.drawRootedTree(rt)
print(descendant(rt, 1))
    