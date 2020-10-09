import TreeBuilder
import TreeDrawer
import constant
import networkx as nx
import CopManager

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
        tree = TreeBuilder.getRandom(numVertices)
        TreeDrawer.drawGraph(tree.tree, root=0)
    if command == 'r':
        print('Please enter the root\n')
        root = int(input())
        tree = TreeBuilder.fromFile(constant.treeFilePath, root)
        TreeDrawer.drawGraph(tree.tree, root=root)
    if command == 'pr':
        print(CopManager.reverseList(tree.tree,root))                

