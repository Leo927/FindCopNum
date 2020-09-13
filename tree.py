import queue
import random
import networkx as nx
import matplotlib.pyplot as plt

#Configs
SPARES_RATIO = 0.2
MAX_CHILD = 10 # the absolute maximum number of child
MIN_CHILD = 3 # the minimum possible value of the max

def randTreeGenerator(numVertices: int, maxChild : int = 0):	

	if numVertices<=0:
		return {}

	numVertices-=1

	#set the default maxChild if not given
	if maxChild == 0:
		maxChild = min(int(numVertices * SPARES_RATIO),MAX_CHILD)
	if maxChild < MIN_CHILD:
		maxChild = MIN_CHILD

	#put the root node onto the graph
	graph = {0:[]}
	currentNumVertices=1

	#create a queue and enqueue root node
	toVisit = queue.SimpleQueue()
	toVisit.put(0)
	
	while toVisit.empty()==False and currentNumVertices <= numVertices:
		node = toVisit.get()
		numChild = int(min(random.random()*maxChild,numVertices-currentNumVertices))
		if numChild == 0:
			children = []
			if toVisit.empty() and currentNumVertices <= numVertices:
				graph.update({node:[currentNumVertices]})
				toVisit.put(currentNumVertices)
				currentNumVertices += 1
		else:
			children = list(range(currentNumVertices, currentNumVertices+numChild))
			graph.update({node:children})
			for child in children:
				toVisit.put(child)
			currentNumVertices+=numChild		
	return graph

def drawGraph(graph:dict, savePath:str="simple_path.png", show:bool=False):	
	G=nx.Graph()
	for key in graph:
		for child in graph[key]:
			G.add_edge(key,child)
	#tex.insert(tk.END,'\n')
	#tex.insert(tk.END, "Nodes of graph: ")
	#tex.insert(tk.END, G.nodes())
	#tex.insert(tk.END,'\n')
	#tex.insert(tk.END, "Edges of graph: ")
	#tex.insert(tk.END, G.edges())
	#tex.insert(tk.END,'\n')
	#tex.see(tk.END)
	plt.figure(figsize=(50,30))
	nx.draw(G, with_labels=True)
	
	plt.savefig(savePath) # save as png
	if show:
		plt.show()

def autoGenGraph():
	for x in range(30,151,30):
		drawGraph(randTreeGenerator(x), str(x)+' vertices.png')
	#tk.messagebox.showinfo(title=None,message='The generated files are in the same directory as the program')
	plt.show()

def generateGraph(numVertices:str):	
	plt.close('all')
	if numVertices.isnumeric() == False:
		return;
	drawGraph(randTreeGenerator(int(numVertices)), numVertices+' vertices.png', show=True)