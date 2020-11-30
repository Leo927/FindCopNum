import rootedtree
import networkx as nx
import copy
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def drawGraph(graph:nx.classes.graph.Graph, 
              savePath='tempTree', 
              show:bool=True, 
              root=None,
              nodeAttr=None,
              title = None):   
        #change root if given
    digraph = copy.deepcopy(graph)
    if root!= None:
        digraph = nx.bfs_tree(graph,root)
    #adjust the figure size based on the number of nodes
    plt.figure(num = title, figsize=(max(10,len(graph)/5),max(5,len(graph)/10)))
    
    #use pygraphviz to get layout
    pos = graphviz_layout(digraph, prog='dot')
    #using the pygraphviz layout to get a tree like figure
    nx.draw(graph, pos, with_labels=True, arrows=False)    
    
    __drawNodeAttr(graph, pos, nodeAttr)
    
    if savePath!=None:
        plt.savefig(savePath) # save as png
    if show:            
        #mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        plt.show()
        
        
def drawRootedTree(rooted_tree, title=None):
    drawGraph(rooted_tree.tree,root=rooted_tree.root, nodeAttr=rooted_tree.attr, title=title)
    
    
def __drawNodeAttr(G, pos, attr):
    if attr == None:
        return
    labelPos = __offsetPos(pos, 0, 30)
    node_labels = nx.get_node_attributes(G,attr)
    nx.draw_networkx_labels(G, labelPos, labels = node_labels, font_size=6, font_color='r')
    
    
def __offsetPos(pos, dX, dY):
    newPos = {}
    for key,value in pos.items():
        newPos[key] = (value[0]+dX, value[1]+dY)
    return newPos



    