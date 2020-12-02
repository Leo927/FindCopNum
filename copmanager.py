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


logger = logging.getLogger("copmanager")

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(funcName)s line %(lineno)d - %(levelname)s - %(message)s')

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
    if rt.labels[node] != None:
        return bool(rt.labels[node].prebranInd) and rt.labels[node].value == k
    logger.warning("node is not labeled")
    joined = joinByU(rt)
    return (c1Star(subForest(rt, node, 2)) == k and
            c1(joined) == k)


def isKWeaklyBranching(rt, node, k):
    #TODO - test
    if rt.labels[node] != None:
        return bool(rt.labels[node].weakBranInd) and rt.labels[node].value == k
    logger.warning("node is not labeled")
    forests = [subForest(rt, node, 0),
               subForest(rt, node, 1),
               subForest(rt, node, 2)]
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

    nx.set_node_attributes(rt.tree, rt.labels, 'label')

    joined = nx.join([(rt.tree, rt.root), (rt.tree, rt.root)])

    newLabels = nx.get_node_attributes(joined, 'label')
    newLabels[0] = None

    newRT = RootedTree(joined, 0, newLabels)
    return newRT


def subForest(rt, node, distance=0):
    '''Return a forst of RootedTree by finding subTree of children at
    the distance'''
    distance += 1
    children = nx.descendants_at_distance(rt.directed, node, distance)
    subForests = [rt.subTree(child) for child in children]
    return subForests


def c1(rt):
    '''find cop number of a rooted tree'''
    #TODO - implement
    if rt.labels[rt.root] != None:
        return rt.labels[rt.root].value
    logger.warning("node is not labeled")
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
    #TODO - tes
    if rt.labels[v] != None:
        return rt.labels[v].initialCounter and rt.labels[v].value == k
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
    if rt.labels[v] != None:
        return rt.labels[v].weaklyCounter and rt.labels[v].value == k
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
    return [node for node in nodes if func(rt.subTree(node), node, k) == True]


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
    #_c^k(T^[u] - u) = |{j if c1(T^[vj]) =k for vj in u.children'''
    #TODO - test
    return len(descOfType(rt, v, k, lambda _rt, _vj, _k: c1(_rt.subTree(_vj)) == _k))


def maxInitialCounter(rt, v, k):
    '''Definiton 2.6
    h^k(T^[u] - u) = max{J^k(vj) for j in v.chidren'''
    logger.debug(f'descendant of v = {descendant(rt, v)}')
    children = descendant(rt, v)
    if len(children) == 0:
        raise Exception("no children is given to maxWeaklyCounter")
    return max([rt.labels[vj].initialCounter for vj in descendant(rt, v)])


def maxWeaklyCounter(rt, v, k):
    '''Definiton 2.6
    h^k_w(T^[u] -u)) = max{J^k_w(vj) for vj in v.children}'''
    #BUG - no children is given
    logger.debug(f'maxWeaklyCounter(rt={rt}, v={v}, k={k})')
    logger.debug(f'descendant of v = {descendant(rt, v)}')
    children = descendant(rt, v)
    if len(children) == 0:
        raise Exception("no children is given to maxWeaklyCounter")
    return max([rt.labels[vj].weaklyCounter for vj in children])


def getCopNumber(rt: RootedTree):
    '''Algorithem 1
    Compute the copnumber of a tree
    root is picked randomly if not given
    return the label of the root'''

    if rt.labels != None and rt.labels[rt.root] != None:
        logger.debug(f"the cop number is already knonwn for rt = {rt}")
        return rt.labels[rt.root]
    logger.debug(f'rt = {rt}')
    # 2
    revNodes = reverseList(rt)
    if rt.labels == None:
        rt.labels = dict((node, Label.noChild() if len(descendant(rt, node)) == 0
                          else None) for node in revNodes)
        logger.debug(f'rt = {rt}')

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
    T1 = findT1(rt, u)
    logger.debug(f'T1 = {T1}')
    # compute c1(T1)
    LT1u = compute_label(T1, u)
    logger.debug(f'LT1u = {LT1u}')
    # 7
    L = getLeadingLabels(rt, children, I_perpen, LT1u)
    logger.debug(f'L = {L}')
    # 8, #9
    distinctKey, largestRepeatedKey = keyRepeated(L)
    logger.debug(f'distinctKeys = {distinctKey}')
    logger.debug(f'k* = {largestRepeatedKey}')
    if(largestRepeatedKey == None):
        rt.labels[u] = copy.deepcopy(LT1u)
        rt.labels[u].sv = L[0:-1] + rt.labels[u].sv
        return rt.labels[u]

    # 10
    K = decreasingWithMinimum(distinctKey, largestRepeatedKey)
    logger.debug(f'K = {K}')
    # 11
    h = findh(K)
    logger.debug(f'h = {h}')
    K = updateK(K, h)
    logger.debug(f'update K = {K}')

    X = findX(L, K)
    logger.debug(f'X = {X}')
    rt.labels[u] = X
    return rt.labels[u]


def findT1(rt, u):
    #TODO - test
    logger.debug(f'findT1({rt.tree.nodes}, {u}')
    T = rt.subTree(u)
    logger.debug(f"rt is {rt}\nT is {T}")
    children = descendant(T, u)
    logger.debug(f'children of u = {children}')
    I_perpen, Ib = splitContainPerp(rt, children)
    logger.debug(f'I_perpen = {I_perpen}, labels for I_perpen = {[rt.labels[child] for child in I_perpen]}')
    T1 = copy.deepcopy(T)
    nodes_to_remove = []
    for child in Ib:
        if len(rt.labels[child]) >= 1:
            nodes_to_remove.append(rt.labels[child][-1].attribute)
    for child in I_perpen:
        if len(rt.labels[child]) >= 2:
            nodes_to_remove.append(rt.labels[child][-2].attribute)
    logger.debug(f'nodes to remove{nodes_to_remove}')
    T1 = T1.trimTreeFromNode(*nodes_to_remove)
    T1.labels = dict((node, rt.labels[node].lastSix() if rt.labels[node] != None else None)
                     for node in rt.labels )
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
    elif h == 2:
        K = [K[0]]
    else:
        K = K[0: h-2]
    K.append(temp)
    return K


def getLeadingLabels(rt, nodes: list, I_perpen: list, LT1u: Label):
    '''Algorithem 1 #7
    nodes: raw data type representing nodes
    labels: dict of node:Label pairs
    I_perpen: list of nodes that contains perpendicular sign
    LT1u: Label of T1
    return [SV]'''
    k = LT1u.value
    L = []
    logger.debug(f'nodes = {nodes}, I_perpen = {I_perpen}')
    for node in nodes:
        if node in I_perpen:
            numToDelete = 6
        else:
            numToDelete = 4
        logger.debug(f"node = {node}, adding {rt.labels[node].deleteLast(numToDelete)}")
        L = L + ([l for l in
                rt.labels[node].deleteLast(numToDelete)
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
    X.ind = [0,0,0,0]
    h = len(K)
    
    for index in range(1,h):
        X.append(K[index - 1], findAttributeByKey(K[index - 1], L))
    X.append(K[h-1], constant.PERPEN_SYM)
    return X

def findAttributeByKey(key, SVs:list):
    attr = next((sv.attribute for sv in SVs if sv.key == key), None)
    if attr == None:
        raise Exception(f'SVs exhausted,key = {key} in {SVs}')
    return attr


def compute_label(rt, u):
    '''rt = T1
    return T1u[u]'''
    if (len(rt.descendant(u))==0):
        rt.labels[u] = Label.noChild()
        return rt.labels[u]

    logger.debug("start")
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

    logger.debug(
        f"u = {u}, k = {k}, numKWb = {numKWb}, numKPb = {numKPb}, numKC ={numKC}, hkW = {hkW}, hk={hk}")

    # 1
    if numKWb > 1:
        rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM)
        logger.debug("#1 is triggered")
    # 3
    elif numKWb == 1 and numKPb >= 1:
        rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
        logger.debug("#3 is triggered")

    # 5
    elif (numKWb == 1 and
        numKPb == 0 and
            numKC >= 2):
        # 6
        if hkW == 2:
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
            logger.debug("#6 is triggered")
        # 8
        elif (hkW == 1 and
                hk >= 1):
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM, 0, 0, 0, 0)
            logger.debug("#8 is triggered")
        # 10
        elif (hkW == 1 and
                hk == 0):
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
            logger.debug("#10 is triggered")
        # 12
        elif (hkW == 0 and
                hk == 2):
            rt.labels[u] = Label.make(k + 1, constant.PERPEN_SYM, 0, 0, 0, 0)
            logger.debug("#12 is triggered")
        # 14
        elif (hkW == 0 and
                hk <= 1):
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 1, 0, 0)
            logger.debug("#14 is triggered")
    # 16
    elif numKWb == 1 and numKC == 1:
        # 17
        if hkW == 2:
            rt.labels[u] = Label.make(k, u)
            logger.debug("#17 is triggered")
        # 19
        elif hkW == 1:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 2, 0, 0)
            logger.debug("#19 is triggered")
        # 21
        elif hkW == 0:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 1, 0, 0)
            logger.debug("#21 is triggered")
    # 23
    elif numKWb == 0:
        # 24
        if numKPb >= 3:
            rt.labels[u] = Label.make(k+1, constant.PERPEN_SYM)
            logger.debug("#24 is triggered")
        # 26
        elif numKPb == 2:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 1, 0, 0, 0)
            logger.debug("#26 is triggered")
        # 28
        elif numKPb == 1:
            rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
            logger.debug("#28 is triggered")
        # 30
        elif numKPb == 0:
            # 31
            if hk == 2:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 1, 0)
                logger.debug("#31 is triggered")
            # 33
            elif hk == 1:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 2)
                logger.debug("#33 is triggered")
            # 35
            elif hk == 0:
                rt.labels[u] = Label.make(k, constant.PERPEN_SYM, 0, 0, 0, 1)
                logger.debug("#35 is triggered")
    if rt.labels[u] == None:
        raise Exception("nothing is changed from compute-label")
    return rt.labels[u]


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

logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    rt = RootedTree.load(10)
    print(getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True)
    


    # graph = nx.Graph()
    # graph.add_edge(0,1)
    # graph.add_edge(0,2)
    # labels = {0:Label.make(1,constant.PERPEN_SYM), 1:Label.make(1,1), 2:Label.make(1,3)}
    # rt = RootedTree(graph, 0, labels)
    # joined = joinByU(rt)

    # treedrawer.drawRootedTree(joined)
    # print(joined.labels)
