# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:53:45 2020

@author: Songhao Li
"""

import unittest
import networkx as nx
from rootedtree import RootedTree
import matplotlib.pyplot as plt
import copy
import treedrawer
import constant
import random
from label import Label,SV


def reverseList(rt):
    reversedList = []
    __reverseListRecur(rt.directed(), rt.root, reversedList)
    return reversedList


def __reverseListRecur(tree, root, output):
    children = dict(nx.bfs_successors(tree, root, 1))[root]
    for child in children:
        __reverseListRecur(tree, child, output)
    output.append(root)


def isKPreBranching(rt, node, k):
    #TODO - test
    tree = rt.tree
    return (c1Star(subForest(tree, node, 2)) == k and
            c1(joinByU(rt)) == k)


def isKWeaklyBranching(rt, node, k):
    #TODO - test
    forests = [subForest(rt, node, 0),
               subForest(rt, node, 1),
               subForest(rt, node, 2)]
    # It is exactly one
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
    right &= c1Star(subForest(rt, node, 2)) == k
    right &= (sum(isKWeaklyBranching(rt, rt.root, k)
                  for rooted_tree in subForest(rt, node, 2)) != 1)
    right &= (sum(isKWeaklyBranching(rt.tree, rt.root, k)
                  for rooted_tree in subForest(rt, node, 3)) == 0)
    return right


def joinByU(rt):
    return RootedTree(nx.join([(rt.tree, rt.root),
                               (rt.tree, rt.root)]), rt.root)


def subForest(rt, node, distance=0):
    '''Return a forst of RootedTree by removing neigbhor of node 
    in given distance'''
    distance += 1
    digraph = nx.bfs_tree(rt.directed, node)
    children = nx.descendants_at_distance(digraph, node, distance)
    return [RootedTree(nx.bfs_tree(digraph, child), child) for child in children]


def c1(rt):
    '''find cop number of a rooted tree'''
    #TODO - implement
    pass


def c1Star(forest):
    #TODO - test
    result = 0
    for rt in forest:
        result = max(result, c1(rt))
    return result


def descendant(rt, node, distance=1):
    '''return descendant within distance(default = 1)
    does not include node it self'''
    pairs = dict(nx.bfs_successors(rt.directed, node, depth_limit=distance))
    children = []
    for key in pairs:
        children = pairs[key] + children
    return children


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


def getCopNumber(tree, root=None):
    '''Algorithem 1
    Compute the copnumber of a tree'''
    if(len(tree) < 12):
        raise Exception('number of vertices in tree must be at least 12')
    # 1
    if(root == None):
        root = tree.nodes[random.randint(0, len(tree) - 1)]
    rt = RootedTree(tree, root)

    # 2
    revNodes = reverseList(rt)
    labels = dict((node, Label.noChild() if len(descendant(rt, node)) == 0
                   else None) for node in revNodes)

    # 3
    while(labels[root] == None):
        # get the first unlabeled node
        u = nextUnlabled(revNodes, labels)
        children = descendant(rt, u)

        I_perpen, Ib = splitContainPerp(children, labels)

        # construct T1[u]
        T1 = trimTreeFromNode(rt, *Ib, *I_perpen)
        # compute c1(T1)
        LT1u = compute_label(T1, u, labels)[1]
        k = LT1u.value

        # 7
        L = getLeadingLabels(children, labels, I_perpen, LT1u)

        # 8, #9
        distinctKeyLabels, largestRepeatedKey = keyRepeated(L)
        if(largestRepeatedKey >= 0):
            labels[u] = LT1u
            labels[u] = labels[u] + L[0:-1]
            continue

        # 10
        K = decreasingWithMinimum(distinctKeyLabels, largestRepeatedKey)

        # 11
        h = findh(K)
        K = updateK(K, h)


def decreasingWithMinimum(items, minimum):
    '''Algorithm 1 step 10 calculate K'''
    return sorted([item for item in items if item >= minimum], reverse=True)


def findh(K):
    '''Algorithm 1 step 11 findh'''
    l = len(K)
    for h in range(1, l + 1):
        if sum(K[h - 1] != (K[h+i - 1] + i) for i in range(h+1, l-h + 1)) == 0:
            return h

    raise Exception("no h is returned")


def updateK(K, h):
    '''Algorithm 1 step 11 update K
    have to use like K = updateK(K,h)'''
    temp = K[h-1]+1
    if h <= 1:
        K = []
    else:
        K = K[0: h-2]
    K.append(temp)
    return K


def getLeadingLabels(nodes: list, labels: dict, I_perpen: list, LT1u: Label):
    '''Algorithem 1 #7
    nodes: raw data type representing nodes
    labels: dict of node:Label pairs
    I_perpen: list of nodes that contains perpendicular sign
    LT1u: Label of T1'''
    k = LT1u.value
    L = []
    for node in nodes:
        L = L + ([l for l in
                  labels[node].deleteLast(6 if node in I_perpen else 4)
                  if l.key >= k])
    L.append(LT1u[1])
    return L


def splitContainPerp(nodes, labels):
    '''seperate nodes into two sets.
    One set contains ⊥ in label.
    The other set doesn't.
    return (contains, notcontains) '''
    # I⊥ be the subset of children whose label contains ⊥
    I_perpen = []

    # Ib be the subset of children whose label does not contain ⊥
    Ib = []
    for child in nodes:
        if labels[child] == None:
            raise Exception("some children haven't get label")
        if labels[child].containPerpen():
            I_perpen.append(child)
        else:
            Ib.append(child)
    return (I_perpen, Ib)


def keyRepeated(L):
    '''return distinctKeyItems, largest repeating key of L'''
    count = dict((item.key, 0) for item in L)
    for item in L:
        count[item.key] = count[item.key] + 1
    return ([key for key in count],
            max([key for key in count if count[key] > 1 ]))

def findX(L, K):
    X = Label()
    X.ind = [0,0,0,0]
    h = len(K) - 1 # -1 to compensate difference of 0 base and 1 base. now we are 0 based
    for idx, k_i in enumerate(K):
        if idx == h:
            X.append(k_i, constant.PERPEN_SYM)
        else:
            x_i = next(sv.attribute for sv in L if sv.key == k_i)
            X.append(k_i, x_i)
    return X

def compute_label(rt, u, labels):
    '''rt = T1'''
    k = c1Star(subForest(rt, u))

    # ^k_wb
    numKWb = numKWeakBranChild(rt, u, k)
    # ^k_pb
    numKPb = numKPreBranChild(rt, u, k)
    # ^k_c
    numKC = numKC1Child(rt, u, k)
    # h^k_w
    hkW = maxWeaklyCounter(rt, u, k)
    # h^k
    hk = maxInitialCounter(rt, u, k)

    # 1
    if numKWb > 1:
        return Label.make(k+1, constant.PERPEN_SYM)
    # 3
    if numKWb == 1 and numKPb >= 1:
        return Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)

    # 5
    if (numKWb == 1 and
        numKPb == 0 and
            numKC >= 2):
        # 6
        if hkW == 2:
            return Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 8
        if (hkW == 1 and
                hk >= 1):
            return Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 10
        if (hkW == 1 and
                hk == 0):
            return Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
        # 12
        if (hkW == 0 and
                hk == 2):
            return Label.make(k + 1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 14
        if (hkW == 0 and
                hk <= 1):
            return Label.make(k + 1, constant.PERPEN_SYM, 1, 1, 0, 0)
    # 16
    if numKWb == 1 and numKC == 1:
        # 17
        if hkW == 2:
            return Label.make(k, u)
        # 19
        if hkW == 1:
            return Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
        # 21
        if hkW == 0:
            return Label.make(k, constant.PERPEN_SYM, 1, 1, 0, 0)
    # 23
    if numKWb == 0:
        # 24
        if numKPb >= 3:
            return Label.make(k+1, constant.PERPEN_SYM)
        # 26
        if numKPb == 2:
            return Label.make(k, constant.PERPEN_SYM, 1, 0, 0, 0)
        # 28
        if numKPb == 1:
            return Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
        # 30
        if numKPb == 0:
            # 31
            if hk == 2:
                return Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
            # 33
            if hk == 1:
                return Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 2)
            # 35
            if hk == 0:
                return Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 1)
    raise Exception("nothing is returned from compute-label")


def nextUnlabled(revNodes, labels):
    return next(node for node in revNodes if labels[node] == None)


def kBranchingDescendent(rt, v, k):
    descendents = nx.bfs_successors(rt.directed, v)
    return [node for node in descendents if isKBranching(rt, v, k)]


def trimTreeFromNode(rt, *arg):
    '''return a copy of the trimmed rooted tree'''
    #TODO - test
    tempTree = copy.deepcopy(rt)
    for v in arg:
        nodesToRemove = nx.dfs_tree(rt.directed, v).nodes
        tempTree.tree.remove_nodes_from(nodesToRemove)
    return tempTree


if __name__ == "__main__":
    labels = {1:Label.make(5, constant.PERPEN_SYM), 2:Label.make(6,constant.PERPEN_SYM), 3:Label.make(4,3), 4:Label.make(6,4), 5:Label.make(7, 5)}
    L = [labels[4][1], labels[5][1], LT1u[1]]
    distinct, largest = keyRepeated(L) 
