import treebuilder
import treedrawer
import constant
import networkx as nx
import copmanager

command = ''

while command != 'q':
    print('Please enter a command:\n')
    print('g: generate a new graph and store into a txt file\n')
    print('r: read from a txt file\n')
    print('pr: print reverse list where all children are printed before their parent\n')
    print('q: quit')
    command = input()    
    if command == 'g':
        print('Please enter the number of vertices.\n')
        numVertices = int(input())
        tree = treebuilder.getRandom(numVertices)
        treedrawer.drawGraph(tree.tree, root=0)
    if command == 'r':
        print('Please enter the root\n')
        root = int(input())
        tree = treebuilder.fromFile(constant.treeFilePath, root)
        treedrawer.drawGraph(tree.tree, root=root)
    if command == 'pr':
        print(copmanager.reverseList(tree.tree,root))                

