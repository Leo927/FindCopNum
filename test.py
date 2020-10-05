# -*- coding: utf-8 -*-
import TreeBuilder
import TreeDrawer
import constant
import networkx as nx

#tree = nx.random_tree(20)

tree = TreeBuilder.Builder.fromFile(constant.treeFilePath, 0)
TreeDrawer.Drawer.drawGraph(tree)