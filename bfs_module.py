"""
BFS section - Graph Traversal Techniques: Comparative analysis of BFS and DFS
 
Every function returns plain Python lists/dicts so the comparison section
can call them directly and line the results up against the DFS versions.
Graphs are adjacency lists: {node: [neighbors]}. For undirected graphs,
list each edge in both directions.
 
SECTIONS (search for the number to jump to one):
  [1] Imports
  [2] Core BFS traversal
  [3] Application: shortest path
  [4] Application: levels (for the diagram)
  [5] Application: connected components
  [6] Application: topological sort (Kahn's algorithm)
  [7] Timing helper (for the comparison section)
  [8] Demo graphs (shared with the DFS section)
  [9] Demo run
"""
 
# =============================================================================
# [1] IMPORTS
# =============================================================================
 
from collections import deque  # deque gives fast O(1) removal from the front, which a BFS queue needs
import time                    # time lets us measure how long a traversal takes
 
 
# =============================================================================
# [2] CORE BFS TRAVERSAL
# Everything else in this file is built on top of this function.
# =============================================================================
 
def bfs_traversal(graph, start):
    """Return (visit_order, parent, distance) for everything reachable from start."""
    visited = {start}               # set of nodes already discovered; the start node counts as discovered
    queue = deque([start])          # the BFS queue (first in, first out), seeded with the start node
    order = []                      # records the order in which nodes are actually visited
    parent = {start: None}          # parent[x] = the node we came from to reach x (start has no parent)
    distance = {start: 0}           # distance[x] = number of edges from start to x (start is 0 away from itself)
 
    while queue:                    # keep going until there are no more nodes waiting to be explored
        node = queue.popleft()      # take the node that has been waiting longest (front of the queue)
        order.append(node)          # visit it: add it to the visit order
        for neighbor in graph.get(node, []):              # look at every neighbor of this node (empty list if none)
            if neighbor not in visited:                   # only handle neighbors we have not seen before
                visited.add(neighbor)                     # mark it as discovered right away so it is never queued twice
                parent[neighbor] = node                   # remember which node led us to this neighbor
                distance[neighbor] = distance[node] + 1   # it is one edge farther from start than the current node
                queue.append(neighbor)                    # put it at the back of the queue to be explored later
 
    return order, parent, distance  # hand back everything the other functions need
 
 
# =============================================================================
# [3] APPLICATION: SHORTEST PATH (unweighted graphs)
# BFS reaches each node using the fewest edges,  the parent chain is the shortest path.
# =============================================================================
 
def bfs_shortest_path(graph, start, goal):
    """Fewest-edge path from start to goal, or None if goal is unreachable."""
    _, parent, distance = bfs_traversal(graph, start)   # run BFS; only parent map needed
    if goal not in parent:                              # if BFS never reached the goal, no path exists
        return None                                     # signal "unreachable" to the caller
    path = []                                           # will hold the path, built from the goal backward
    node = goal                                         # start walking backward from the goal
    while node is not None:         # the start node has parent None, which ends the loop
        path.append(node)           # add the current node to the path
        node = parent[node]         # step back to the node that led us here
    path.reverse()                  # flip it so it reads start -> goal
    return path                     # return the finished path
 
 
# =============================================================================
# [4] APPLICATION: LEVELS (useful for the BFS layer diagram)
# Groups nodes by how many edges they are from the start.
# =============================================================================
 
def bfs_levels(graph, start):
    """Group reachable nodes by their distance from start."""
    _, _, distance = bfs_traversal(graph, start)   # run BFS; only distance map needed
    levels = {}                                    # will map level number -> list of nodes on that level
    for node, d in distance.items():               # go through every reachable node and its distance
        levels.setdefault(d, []).append(node)      # create the level's list if needed, then add the node to it
    return levels                                  # return the grouped levels
 
 
# =============================================================================
# [5] APPLICATION: CONNECTED COMPONENTS (undirected graphs)
# Start a fresh BFS from every node not yet seen; each BFS finds one component.
# =============================================================================
 
def bfs_connected_components(graph):
    """Connected components of an undirected graph, as a list of node lists."""
    seen = set()                    # nodes that already belong to a component we have found
    components = []                 # the list of components we will return
    for node in graph:              # check every node in the graph
        if node not in seen:        # if it is not in any component yet, it starts a new one
            order, _, _ = bfs_traversal(graph, node)   # BFS from it reaches its whole component
            seen.update(order)                         # mark all of those nodes as accounted for
            components.append(order)                   # save this component
    return components               # one list of nodes per component
 
 
# =============================================================================
# [6] APPLICATION: TOPOLOGICAL SORT (directed acyclic graphs)
# Kahn's algorithm is the BFS-style approach: repeatedly remove nodes with no prerequisites.
# =============================================================================
 
def bfs_topological_sort(graph):
    """Kahn's algorithm. Returns an order, or None if the graph has a cycle."""
    in_degree = {node: 0 for node in graph}          # in_degree[x] = how many edges point INTO x; start every node at 0
    for node in graph:                               # go through every node...
        for neighbor in graph[node]:                 # ...and each edge leaving it
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1   # that edge adds one incoming edge to its target
 
    queue = deque(node for node, deg in in_degree.items() if deg == 0)   # start with nodes that have no prerequisites
    order = []                                       # the topological order we are building
    while queue:                                     # keep going while there are nodes with no remaining prerequisites
        node = queue.popleft()                       # take the next available node
        order.append(node)                           # place it in the order
        for neighbor in graph.get(node, []):         # "remove" this node by updating everything it points to
            in_degree[neighbor] -= 1                 # that neighbor now has one fewer unmet prerequisite
            if in_degree[neighbor] == 0:             # if it has no prerequisites left...
                queue.append(neighbor)               # ...it is ready, so queue it
 
    return order if len(order) == len(in_degree) else None   # if some nodes never got output, there is a cycle -> None
 
 
# =============================================================================
# [7] TIMING HELPER (for the comparison section)
# =============================================================================
 
def time_bfs(graph, start, runs=1000):
    """Average seconds per full traversal."""
    begin = time.perf_counter()                 # record the starting time with a high-resolution clock
    for _ in range(runs):                       # repeat many times so the average is stable
        bfs_traversal(graph, start)             # run one full BFS (result is ignored; we only want the time)
    return (time.perf_counter() - begin) / runs # total elapsed time divided by number of runs = average per run
 
 
# =============================================================================
# [8] DEMO GRAPHS
# Agree with your group on one shared set so BFS and DFS results can be compared.
# =============================================================================
 
# Undirected graph with two components (used for traversal, shortest path, components)
UNDIRECTED = {
    "A": ["B", "C"],        # A connects to B and C
    "B": ["A", "D", "E"],   # B connects to A, D, and E
    "C": ["A", "F"],        # C connects to A and F
    "D": ["B"],             # D connects only to B
    "E": ["B", "F"],        # E connects to B and F
    "F": ["C", "E"],        # F connects to C and E
    "G": ["H"],             # G and H form a second, separate component
    "H": ["G"],
}
 
# Directed acyclic graph (used for topological sorting); an edge means "must come before"
DAG = {
    "Intro": ["Data Structures", "Discrete Math"],   # Intro comes before both of these
    "Data Structures": ["Algorithms"],               # Data Structures comes before Algorithms
    "Discrete Math": ["Algorithms"],                 # Discrete Math also comes before Algorithms
    "Algorithms": ["Graph Theory"],                  # Algorithms comes before Graph Theory
    "Graph Theory": [],                              # Graph Theory has nothing after it
}
 
 
# =============================================================================
# [9] DEMO RUN (only executes when this file is run directly, not when imported)
# =============================================================================
 
if __name__ == "__main__":
    order, parent, distance = bfs_traversal(UNDIRECTED, "A")                           # run the core BFS from node A
    print("BFS visit order from A:", order)                                            # show the order nodes were visited
    print("Distances from A:", distance)                                               # show each node's edge distance from A
    print("Levels from A:", bfs_levels(UNDIRECTED, "A"))                               # show nodes grouped by level
    print("Shortest path A -> F:", bfs_shortest_path(UNDIRECTED, "A", "F"))            # shortest path within A's component
    print("Shortest path A -> G:", bfs_shortest_path(UNDIRECTED, "A", "G"))            # G is in another component, so None
    print("Connected components:", bfs_connected_components(UNDIRECTED))               # find both components
    print("Topological order (Kahn):", bfs_topological_sort(DAG))                      # prerequisite-respecting order
    print(f"Avg traversal time: {time_bfs(UNDIRECTED, 'A') * 1e6:.2f} microseconds")   # average speed in microseconds
