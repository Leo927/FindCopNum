# -*- coding: utf-8 -*-
import treebuilder
import treedrawer
import constant
import networkx as nx
import copmanager
import matplotlib.pyplot as plt
import graphtraversal
from pprint import pprint
root = 2

rooted_tree = treebuilder.getRandom(30)
treedrawer.drawRootedTree(rooted_tree, 0)
graphtraversal.bfs(rooted_tree.tree, 0, func = print )


