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

def example():
    rt = RootedTree.load(0, "example4_1.txt")
    print(copmanager.getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True, show=False, savePath="example4.1.pdf")

    rt = RootedTree.load(0, "example4_2.txt")
    print(copmanager.getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True, show=False, savePath="example4.2.pdf")

    rt = RootedTree.load(0, "example4_3.txt")
    print(copmanager.getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True, show=False, savePath="example4.3.pdf")

    rt = RootedTree.load(5, "example4_3.txt")
    print(copmanager.getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True, show=False, savePath="example4.4.pdf")

    rt = RootedTree.load(0, "example4_5.txt")
    x1 = 11
    x2 = 12
    x3 = 13
    rt.labels = {0:None, 1: Label.make(4,constant.PERPEN_SYM, 0,0,1,0), 2: Label.make(4,constant.PERPEN_SYM, 0,0,1,0),
                    3: Label.make(5,x1, 0,0,0,2).append(2,constant.PERPEN_SYM), 4:Label.make(8,x2, 0,0,0,0).append(4,4),
                    5: Label.make(6,x3, 0,0,0,0).append(2,5),
                    11:Label.make(5,constant.PERPEN_SYM),
                    12:Label.make(8, constant.PERPEN_SYM),
                    13: Label.make(6, constant.PERPEN_SYM)}
    print(copmanager.getCopNumber(rt))
    treedrawer.drawRootedTree(rt, True, show=False, savePath="example4.5.pdf")

if __name__ == "__main__":
    os.makedirs("./experiment" , exist_ok=True)
    files = glob.glob('./experiment/*')
    for f in files:
        os.remove(f)
    for i in range(1, constant.NUM_TREE + 1):
        analyzeOneTree(i)
    example()