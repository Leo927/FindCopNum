# -*- coding: utf-8 -*-
import TreeBuilder
import TreeDrawer
import constant
import networkx as nx
import CopManager

root = 1
#tree = TreeBuilder.getRandom(30)
tree = TreeBuilder.fromFile(constant.treeFilePath, root)
#subForest = CopManager.subForest(tree, 26, 2)
#print(subForest)
TreeDrawer.drawGraph(tree,root=2)

#print(CopManager.reverseList(tree,root))