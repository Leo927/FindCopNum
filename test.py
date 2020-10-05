# -*- coding: utf-8 -*-
import TreeBuilder
import TreeDrawer
import constant
import networkx as nx

#tree = nx.random_tree(20)

tree = TreeBuilder.Builder.getRandom(300)
TreeDrawer.Drawer.drawGraph(tree)