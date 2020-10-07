# -*- coding: utf-8 -*-
import TreeBuilder
import TreeDrawer
import constant
import networkx as nx
import CopManager

root = 1

tree = TreeBuilder.Builder.fromFile(constant.treeFilePath, root)
TreeDrawer.Drawer.drawGraph(tree)

print(CopManager.reverseList(tree,root))