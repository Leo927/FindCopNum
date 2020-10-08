# -*- coding: utf-8 -*-
import TreeBuilder
import TreeDrawer
import constant
import networkx as nx
import CopManager
import matplotlib.pyplot as plt
from pprint import pprint
root = 2

rooted_tree = TreeBuilder.fromFile(constant.treeFilePath, root)
TreeDrawer.drawRootedTree(rooted_tree)

#jointed = CopManager.joinByU(rooted_tree)
#TreeDrawer.drawRootedTree(jointed)




subForest = CopManager.subForest(rooted_tree.tree, 26, 0)
# #print(subForest)
# TreeDrawer.drawGraph(tree)
# #tree = CopManager.joinByU(tree, root)
for t in subForest:
    TreeDrawer.drawGraph(t.tree)

#nx.disjoint_union_all(subForest)

#print(CopManager.reverseList(tree,root))

