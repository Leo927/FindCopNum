# -*- coding: utf-8 -*-
from rootedtree import RootedTree
import treedrawer
import constant
import networkx as nx
import copmanager
import matplotlib.pyplot as plt
import graphtraversal
from pprint import pprint
root = 2

rooted_tree = RootedTree.random(30)
rooted_tree.root = 5
rooted_tree.add_long_weight(5)
print(copmanager.findLongestEqualWeightPath(rooted_tree, 5))

treedrawer.drawRootedTree(rooted_tree)