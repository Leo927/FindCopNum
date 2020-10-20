import treebuilder
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def drawGraph(graph:nx.classes.graph.Graph, 
              savePath='tempTree', 
              show:bool=True, 
              root=None,
              nodeAttr=None):   
        #change root if given
    if root!= None:
        graph = nx.bfs_tree(graph,root)
    #adjust the figure size based on the number of nodes
    plt.figure(figsize=(max(10,len(graph)/5),max(5,len(graph)/10)))
    
    #use pygraphviz to get layout
    pos = graphviz_layout(graph, prog='dot')
    #using the pygraphviz layout to get a tree like figure
    nx.draw(graph, pos, with_labels=True, arrows=False)    
    
    drawNodeAttr(graph, pos, nodeAttr)
    
    if savePath!=None:
        plt.savefig(savePath) # save as png
    if show:            
        #mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        plt.show()
        
def drawRootedTree(rooted_tree, nodeAttr=None):
    drawGraph(rooted_tree.tree,root=rooted_tree.root, nodeAttr=nodeAttr)
    
def drawNodeAttr(G, pos, attr):
    labelPos = offsetPos(pos, 0, -20);
    node_labels = nx.get_node_attributes(G,attr)
    nx.draw_networkx_labels(G, labelPos, labels = node_labels)
    
def offsetPos(pos, dX, dY):
    newPos = {}
    for key,value in pos.items():
        newPos[key] = (value[0]+dX, value[1]+dY)
    return newPos



    