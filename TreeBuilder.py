import queue
import random
import networkx as nx
import logging
from networkx.readwrite import json_graph
import json
import constant
from collections import namedtuple
    ###########################

rooted_tree = namedtuple('rooted_tree','tree root')


def getRandom( numVertices:int):
    if numVertices <= 0:
        return nx.Graph()    
    
    graph=nx.random_tree(int(numVertices))
    #graph = nx.bfs_tree(graph,0)
    
    #convert to json and
    graphJson = json_graph.adjacency_data(graph)
    graphText = json.dumps(graphJson, indent=4)
    
    #write to file
    file = open(constant.treeFilePath, "w")
    file.write(graphText)
    file.close()
    
    
    #log the json. it is hooked up to the gui textbox
    logging.info(graphText)
    
    print(graphText)
    return rooted_tree(graph,0)

def fromFile(path, root):
    file = open(path, "r")
    graphJson = json.loads(file.read())
    graphJson['directed'] = False
    graph = json_graph.adjacency_graph(graphJson)
    return rooted_tree(graph,root)
    

