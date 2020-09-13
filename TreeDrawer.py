from TreeBuilder import TreeBuilder
import networkx as nx
import matplotlib.pyplot as plt

class TreeDrawer(object):
	def __init__(self):
		return super().__init__()

	@classmethod
	def drawGraph(self, graph:nx.classes.graph.Graph, savePath:str, show:bool):	
		plt.figure(figsize=(max(10,len(graph)/5),max(5,len(graph)/10)))
		nx.draw(graph, with_labels=True)
		
		if savePath!=None:
			plt.savefig(savePath) # save as png
		if show:
			mng = plt.get_current_fig_manager()			
			mng.window.state('zoomed')
			plt.show()

	@classmethod
	def generateAndDraw(self, numVertices:str):	
		plt.close('all')
		if numVertices.isnumeric() == False:
			return;
		graph = TreeBuilder.getRandom(int(numVertices))
		TreeDrawer.drawGraph(graph, numVertices+' vertices.png', show=True)