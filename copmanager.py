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
import logging
from label import Label, SV


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def reverseList(rt):
    reversedList = []
    __reverseListRecur(rt.directed, rt.root, reversedList)
    return reversedList


def __reverseListRecur(tree, root, output):
    children = dict(nx.bfs_successors(tree, root, 1))[root]
    for child in children:
        __reverseListRecur(tree, child, output)
    output.append(root)


def isKPreBranching(rt, node, k):
    #TODO - test
    return (c1Star(subForest(rt, node, 2)) == k and
            c1(joinByU(rt)) == k)


def isKWeaklyBranching(rt, node, k):
    #TODO - test
    forests = [subForest(rt, node, 0),
               subForest(rt, node, 1),
               subForest(rt, node, 2)]
    # It is exactly one
    numForestMeetCondition = 0
    for forest in forests:
        if sum(isKPreBranching(component, component.root, k) == True
               for component in forest) == 2:
            numForestMeetCondition += 1
    if numForestMeetCondition == 1:
        return True
    return False


def isKBranching(rt, node, k):
    #TODO - test
    right = True
    right &= (c1Star(subForest(rt, node, 2)) == k)
    right &= (sum(isKWeaklyBranching(rooted_tree, rooted_tree.root, k)
                  for rooted_tree in subForest(rt, node, 2)) == 1)
    right &= (sum(isKWeaklyBranching(rooted_tree, rooted_tree.root, k)
                  for rooted_tree in subForest(rt, node, 3)) == 0)
    return right


def joinByU(rt):
    newLabels = copy.deepcopy(rt.labels)
    for key in rt.labels:
        newLabels[key + 1 + len(rt)] = rt.labels[key]
    for key in rt.labels:
        newLabels[key + 1] = rt.labels[key]
    newLabels[0] = None

    return RootedTree(nx.join([(rt.tree, rt.root),
                               (rt.tree, rt.root)]), 2*len(rt), newLabels)


def subForest(rt, node, distance=0):
    '''Return a forst of RootedTree by removing neigbhor of node 
    in given distance'''
    distance += 1
    digraph = nx.bfs_tree(rt.directed, node)
    children = nx.descendants_at_distance(digraph, node, distance)
    return [RootedTree(nx.bfs_tree(digraph, child), child, rt.labels) for child in children]


def c1(rt):
    '''find cop number of a rooted tree'''
    #TODO - implement
    return getCopNumber(rt).value


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
    return int(isKPreBranching(rt, v, k))


def kWeakBranInd(rt, v, k):
    #TODO - test
    return int(isKWeaklyBranching(rt, v, k))


def kInitialCounter(rt, v, k):
    '''Definition 2.3 k-initial-counter'''
    #TODO - test
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
    logger.debug(f'finding children of type {func}')
    return [node for node in nodes if func(rt, v, k) == True]


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
    return len(descOfType(rt, v, k, lambda _rt, _vj, _k: c1(_rt.subTree(_vj)) == _k))


def maxInitialCounter(rt, v, k):
    '''Definiton 2.6
    h^k(T^[u] - u) = max{J^k(vj) for j in v.chidren'''
    logger.debug(f'descendant of v = {descendant(rt, v)}')
    children = descendant(rt, v)
    if len(children) == 0:
        return 0
    return max([kInitialCounter(rt, vj, k) for vj in descendant(rt, v)])


def maxWeaklyCounter(rt, v, k):
    '''Definiton 2.6
    h^k_w(T^[u] -u)) = max{J^k_w(vj) for vj in v.children}'''
    logger.debug(f'maxWeaklyCounter(rt={rt}, v={v}, k={k})')
    logger.debug(f'descendant of v = {descendant(rt, v)}')
    children = descendant(rt, v)
    if len(children) == 0:
        return 0
    return max([kWeakCounter(rt, vj, k) for vj in children])


def getCopNumber(rt: RootedTree):
    '''Algorithem 1
    Compute the copnumber of a tree
    root is picked randomly if not given
    return the label of the root'''

    # 2
    revNodes = reverseList(rt)
    logger.debug(f'revNodes = {revNodes}')
    if rt.labels == None:
        rt.labels = dict((node, Label.noChild() if len(descendant(rt, node)) == 0
                          else None) for node in revNodes)
    logger.debug(f'labels = {rt.labels}')

    # 3
    while(rt.labels[rt.root] == None):
        getNextLabel(rt, revNodes)
    return rt.labels[rt.root]


def getNextLabel(rt, revNodes):
    # get the first unlabeled node
    u = nextUnlabled(rt, revNodes)
    logger.debug(f'u = {u}')
    children = rt.descendant(u)
    logger.debug(f'children of u = {children}')
    I_perpen, Ib = splitContainPerp(rt, children)
    logger.debug(f'I_perpen={I_perpen}')
    logger.debug(f'Ib = {Ib}')
    # construct T1[u]
    logger.debug('T1 is drawn')
    T1 = findT1(rt, u)
    treedrawer.drawRootedTree(T1, title="T1")
    # compute c1(T1)
    LT1u = compute_label(T1, u)[1]
    logger.debug(f'LT1u = {LT1u}')
    # 7
    L = getLeadingLabels(children, I_perpen, LT1u)
    logger.debug(f'L = {L}')
    # 8, #9
    distinctKey, largestRepeatedKey = keyRepeated(L)
    logger.debug(f'distinctKeys = {distinctKey}')
    logger.debug(f'k = {largestRepeatedKey}')
    if(largestRepeatedKey == None):
        rt.labels[u] = copy.deepcopy(LT1u)
        rt.labels[u].sv = rt.labels[u].sv + L[0:-1]
        return rt.labels[u]

    # 10
    K = decreasingWithMinimum(distinctKey, largestRepeatedKey)

    # 11
    h = findh(K)
    K = updateK(K, h)
    X = findX(L, K)
    rt.labels[u] = X
    return rt.labels[u]


def findT1(rt, u):
    #TODO - test
    logger.debug(f'findT1({rt.tree.nodes}, {u}')
    T = rt.subTree(u)
    logger.debug(f"rt is {rt.tree.nodes}\nT is {T.tree.nodes}")
    children = descendant(T, u)
    logger.debug(f'children of u = {children}')
    I_perpen, Ib = splitContainPerp(rt, children)
    T1 = copy.deepcopy(T)
    nodes_to_remove = []
    for child in Ib:
        if len(rt.labels[child]) >= 1:
            nodes_to_remove.append(rt.labels[child][-1].attribute)
        else:
            logger.debug("no nodes to remove from {child} in Ib = {Ib}")
    for child in I_perpen:
        if len(rt.labels[child]) >= 2:
            nodes_to_remove.append(rt.labels[child][-2].attribute)
        else:
            logger.debug(
                "no nodes to remove from {child} in I_perpen = {I_perpen}")
    T1.trimTreeFromNode(*nodes_to_remove)
    T1.labels = dict((node, rt.labels[node].lastSix())
                     for node in rt.labels if rt.labels[node] != None)
    return T1


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


def getLeadingLabels(nodes: list, I_perpen: list, LT1u: Label):
    '''Algorithem 1 #7
    nodes: raw data type representing nodes
    labels: dict of node:Label pairs
    I_perpen: list of nodes that contains perpendicular sign
    LT1u: Label of T1
    return [SV]'''
    k = LT1u.value
    L = []
    for node in nodes:
        L = L + ([l for l in
                  rt.labels[node].deleteLast(6 if node in I_perpen else 4)
                  if l.key >= k])
    L.append(LT1u[1])
    return L


def splitContainPerp(rt, nodes):
    '''seperate nodes into two sets.
    One set contains ⊥ in label.
    The other set doesn't.
    return (contains, notcontains) '''
    # I⊥ be the subset of children whose label contains ⊥
    I_perpen = []

    # Ib be the subset of children whose label does not contain ⊥
    Ib = []
    for child in nodes:
        if rt.labels[child] == None:
            logger.critical("some children hasn't got label")
        if rt.labels[child].containPerpen():
            I_perpen.append(child)
        else:
            Ib.append(child)
    return (I_perpen, Ib)


def keyRepeated(L):
    '''return distinctKeyItems, largest repeating key of L
    largestRepeatedKey =None if no repeated key'''
    count = dict((item.key, 0) for item in L)
    for item in L:
        count[item.key] = count[item.key] + 1
    return ([key for key in count],
            None if len([key for key in count if count[key] > 1]) == 0
            else max([key for key in count if count[key] > 1]))


def findX(L, K):
    X = Label()
    X.ind = [0, 0, 0, 0]
    # -1 to compensate difference of 0 base and 1 base. now we are 0 based
    h = len(K) - 1
    for idx, k_i in enumerate(K):
        if idx == h:
            X.append(k_i, constant.PERPEN_SYM)
        else:
            x_i = next(sv.attribute for sv in L if sv.key == k_i)
            X.append(k_i, x_i)
    return X


def compute_label(rt, u):
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
        rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM)
    # 3
    if numKWb == 1 and numKPb >= 1:
        rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)

    # 5
    if (numKWb == 1 and
        numKPb == 0 and
            numKC >= 2):
        # 6
        if hkW == 2:
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 8
        if (hkW == 1 and
                hk >= 1):
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 10
        if (hkW == 1 and
                hk == 0):
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
        # 12
        if (hkW == 0 and
                hk == 2):
            rt.labels[u] = Label.make(k + 1, constant.PERPEN_SYM, 0, 0, 0, 0)
        # 14
        if (hkW == 0 and
                hk <= 1):
            rt.labels[u] = Label.make(k + 1, constant.PERPEN_SYM, 1, 1, 0, 0)
    # 16
    if numKWb == 1 and numKC == 1:
        # 17
        if hkW == 2:
            rt.labels[u] = Label.make(k, u)
        # 19
        if hkW == 1:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
        # 21
        if hkW == 0:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 1, 0, 0)
    # 23
    if numKWb == 0:
        # 24
        if numKPb >= 3:
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM)
        # 26
        if numKPb == 2:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 0, 0, 0)
        # 28
        if numKPb == 1:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
        # 30
        if numKPb == 0:
            # 31
            if hk == 2:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
            # 33
            if hk == 1:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 2)
            # 35
            if hk == 0:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 1)
    raise Exception("nothing is changed from compute-label")


def nextUnlabled(rt, revNodes):
    return next(node for node in revNodes if rt.labels[node] == None)


def kBranchingDescendent(rt, v, k):
    descendents = nx.bfs_successors(rt.directed, v)
    return [node for node in descendents if isKBranching(rt, node, k)]


def trimTreeFromNode(rt, *arg):
    '''return a copy of the trimmed rooted tree'''
    #TODO - test
    tempTree = copy.deepcopy(rt)
    for v in arg:
        nodesToRemove = nx.dfs_tree(rt.directed, v).nodes
        tempTree.tree.remove_nodes_from(nodesToRemove)
    return tempTree


if __name__ == "__main__":

    rt = RootedTree.load(0)
    treedrawer.drawRootedTree(rt)
    getCopNumber(rt)

    # graph = nx.Graph()
    # graph.add_edge(0,1)

    # rt = RootedTree(graph, 0, {0:Label.make(1,0), 1:Label.make(2,1)})
    # treedrawer.drawRootedTree(rt)
    # treedrawer.drawRootedTree(joinByU(rt))
    # print(joinByU(rt).labels)
