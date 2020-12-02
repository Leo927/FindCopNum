from rootedtree import RootedTree
import copmanager
from label import Label
import treedrawer
import random
import constant
import os
import glob

def analyzeOneTree(i):
    rt = RootedTree.random(30*i)
    rt.save(f"./experiment/tree_{30*i}_adjlist.txt")
    roots = random.sample(rt.nodes, constant.NUM_VERTEX)
    for root in roots:
        newRT = RootedTree(rt.tree, root)
        copmanager.getCopNumber(newRT)
        treedrawer.drawRootedTree(newRT, showLabel=True, savePath=f"./experiment/tree_{30*i}_labels_rootedat_{root}.pdf")



if __name__ == "__main__":
    os.makedirs("./experiment" , exist_ok=True)
    files = glob.glob('./experiment/*')
    for f in files:
        os.remove(f)
    for i in range(1, constant.NUM_TREE + 1):
        analyzeOneTree(i)
