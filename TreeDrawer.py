from TreeBuilder import Builder
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class Drawer(object):
    def __init__(self):
        return super().__init__()

    @classmethod
    def drawGraph(self, graph:nx.classes.graph.Graph, savePath='tempTree', show:bool=True):	
        #adjust the figure size based on the number of nodes
        plt.figure(figsize=(max(10,len(graph)/5),max(5,len(graph)/10)))
        
        #use pygraphviz to get layout
        pos = graphviz_layout(graph, prog='dot')
        
        #using the pygraphviz layout to get a tree like figure
        nx.draw(graph, pos, with_labels=True, arrows=False)
        
        #use defult layout, will give random layout
        #nx.draw(graph, with_labels=True)
        
        if savePath!=None:
            plt.savefig(savePath) # save as png
        if show:            
            #mng = plt.get_current_fig_manager()
            #mng.window.state('zoomed')
            plt.show()

    @classmethod
    def generateAndDraw(self, numVertices:str):    
        plt.close('all')
        if numVertices.isnumeric() == False:
            return;
        graph = Builder.getRandom(int(numVertices))
        #graph=nx.random_tree(int(numVertices))
        Drawer.drawGraph(graph, numVertices+' vertices.png', show=True)
        