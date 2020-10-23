from rootedtree import RootedTree
import treedrawer
import constant
import networkx as nx
import copmanager

command = ''
rooted_tree = None
while command != 'q':
    print('Please enter a command:')
    print('generate: generate a new graph and store into a txt file')
    print('save: save the current graph to file')
    print('load <root>: load the saved tree and appoint a root')
    print('pr: print reverse list where all children are printed before their parent')
    print('addweight <start>: add weight to the graph, will try to make a long path from the start')
    print('findpath <start>: find the longest path starting from the <start> ')
    print('draw <root>: draw the current rooted tree, can indicate root')
    print('exit: quit')
    command = input().split(" ")  
    if command[0] == 'generate':
        if len(command) < 2:
            print("please indicate the number of vertices")
            command.append(input())  
        numVertices = int(command[1])
        rooted_tree = RootedTree.random(numVertices)
        print("a rooted tree is generated\n")
        
    if command[0] == 'load':
        if len(command) < 2:
            print("please indicate the root")
            command.append(input())  
        root = int(command[1])        
        rooted_tree = RootedTree.load(root)        
        print("the rooted tree is loaded\n")
        
    if command[0] == 'save':
        if rooted_tree==None:
            print("ERROR: No tree to save")
            continue
        rooted_tree.save()
        print("the rooted tree is saved\n")
        
    if command[0] == 'addweight':
        if len(command) < 2:
            print("please indicate the start")
            command.append(input())  
        start = int(command[1])  
        rooted_tree.add_long_weight(start)
        print("random weight added\n")
        
    if command[0] == 'findpath':
        if len(command) < 2:
            print("please indicate the start")
            command.append(input())  
        start = int(command[1])               
        print(copmanager.findLongestEqualWeightPath(rooted_tree, start))
        
    if command[0] == 'draw':
        tempRoot = rooted_tree.root
        if len(command) >=2:            
            rooted_tree.root = int(command[1])
        if rooted_tree==None:
            print("ERROR: No tree to draw")
            continue
        treedrawer.drawRootedTree(rooted_tree)
        rooted_tree.root = tempRoot
        
    if command[0] == 'pr':
        print(copmanager.reverseList(rooted_tree.tree,root))         
        
    if command[0] == 'exit':
        print("terminated by user")      
        break