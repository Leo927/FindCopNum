import networkx as nx
from enum import Enum
import queue

class __EdgeStatus(Enum):
    UNEXPLORED = 1
    BACKAGE = 2
    CROSS = 3
    DISCOVERY = 4


def dfs(graph, node, func=None, discovery=None, backage=None):
    node_visited = dict((key, False) for key in graph.nodes())
    edge_status = dict((key, __EdgeStatus.UNEXPLORED) for key in graph.edges())
    print(edge_status)
    __traversal(graph, node, node, node_visited, edge_status, before= func)
    
def post_order(graph, node, func=None, discovery=None, backage=None):
    node_visited = dict((key, False) for key in graph.nodes())
    edge_status = dict((key, __EdgeStatus.UNEXPLORED) for key in graph.edges())
    __traversal(graph, node, node, node_visited, edge_status, after= func)
            
def __traversal(graph, 
                parent, 
                node,                 
                node_visited, 
                edge_status, 
                before=None,
                after=None,
                discovery=None, 
                backage=None):
    
    node_visited[node] = True
    if before!=None:
        before(node)
    
    for cNode in __get_connected(graph, node):
        if cNode == parent:
            continue
        if node_visited[cNode] == False:
            if discovery!=None:
                discovery(node, cNode)
            
            __traversal(graph, 
                node, 
                cNode,                 
                node_visited, 
                edge_status, 
                before,
                after,
                discovery, 
                backage)
        else:
            if backage!=None:
                backage(node, cNode)    
    if after!=None:
        after(node)
            
        
def bfs(graph, node, func=None, discovery=None, cross=None):
    #initialize a dictionary with (node, False) to represent all node not visited
    node_visited = dict((key, False) for key in graph.nodes())
    #initialize a dict with (edge, UNEXPLORED) to represent all edges unexplored
    edge_status = dict((key, __EdgeStatus.UNEXPLORED) for key in graph.edges())
    #create a queue and push the starting node
    to_visit = queue.Queue()
    to_visit.put(node)
    
    #do the traversal
    while to_visit.empty()==False:
        node = to_visit.get()
        if func!=None:
            func(node)
        for cNode in __get_connected(graph, node):
            if __is_explored(edge_status, node, cNode) == False:                
                if node_visited[cNode] ==False:
                    __mark_edge(edge_status, (node,cNode), __EdgeStatus.DISCOVERY)
                    to_visit.put(cNode)
                    if discovery!=None:
                        discovery(node,cNode)
                else:
                    __mark_edge(edge_status, (node,cNode), __EdgeStatus.CROSS)
                    if discovery!=None:                        
                        cross(node,cNode)
    return edge_status            
            
                
def __is_explored(edge_status, node1, node2):
    return not (((node1,node2) in edge_status and
                edge_status[(node1, node2)]==__EdgeStatus.UNEXPLORED )                
                or 
                ((node2,node1) in edge_status and
                 edge_status[(node2, node1)] == __EdgeStatus.UNEXPLORED))
                
    

def __get_connected(tree, root):
    return dict( nx.bfs_successors(tree,root,1))[root]    


def __mark_edge(edge_status, edge, status):
    if edge in edge_status:
        edge_status[edge]=status
        return
    if __reverse_edge(edge) in edge_status:
        edge_status[__reverse_edge(edge)] = status
        return
    
def __reverse_edge(edge):
    return (edge[1],edge[0])

