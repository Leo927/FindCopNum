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
        tree = TreeBuilder.Builder.getRandom(numVertices)
        TreeDrawer.Drawer.drawGraph(tree)
    if command == 'r':
        print('Please enter the root\n')
        root = int(input())
        tree = TreeBuilder.Builder.fromFile(constant.treeFilePath, root)
        TreeDrawer.Drawer.drawGraph(tree)
    if command == 'pr':
        print(CopManager.reverseList(tree,root))                

