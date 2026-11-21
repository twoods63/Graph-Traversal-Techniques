"""
DFS section - Graph Traversal Techniques: Comparative analysis of BFS and DFS
 
Every function returns plain Python lists/dicts matching bfs_module.py so the
comparison section can call them directly and line the results up against BFS.
Graphs are adjacency lists: {node: [neighbors]}. For undirected graphs,
list each edge in both directions.
 
SECTIONS (search for the number to jump to one):
  [1] Imports
  [2] Core DFS traversal
  [3] Application: path finding & target discovery
  [4] Application: recursion depth / branch depth map
  [5] Application: connected components
  [6] Application: topological sort (post-order with cycle detection)
  [7] Timing helpers (full traversal and target discovery)
  [8] Demo run (reuses shared graphs from bfs_module.py)
"""
 
# =============================================================================
# [1] IMPORTS
# =============================================================================
 
import time
from bfs_module import UNDIRECTED, DAG
 
 
# =============================================================================
# [2] CORE DFS TRAVERSAL
# Everything else in this file is built on top of this function.
# =============================================================================
 
def dfs_traversal(graph, start):
    """Return (visit_order, parent, depth) for everything reachable from start."""
    visited = set()                 # tracks nodes that have already been popped and visited
    stack = [start]                 # LIFO stack seeded with start node
    order = []                      # records the order in which nodes are visited
    parent = {start: None}          # parent[x] = the node we came from to reach x
    depth = {start: 0}              # depth[x] = branch depth from start (not guaranteed shortest)
 
    while stack:
        node = stack.pop()          # take the most recently added node
        if node in visited:
            continue                # skip if already visited
        visited.add(node)
        order.append(node)

        # Reverse neighbor order so the first neighbor in the adjacency list is on top of the stack.
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = node
                    depth[neighbor] = depth[node] + 1
                stack.append(neighbor)
 
    return order, parent, depth
 
 
# =============================================================================
# [3] APPLICATION: SHORTEST PATH (unweighted graphs)
# BFS reaches each node using the fewest edges,  the parent chain is the shortest path.
# =============================================================================
 
def dfs_target_search(graph, start, goal):
    """
    Early-stopping DFS from start to goal.
    Returns (path, nodes_explored) or (None, nodes_explored) if unreachable.
    """
    visited = set()
    stack = [start]
    parent = {start: None}
    nodes_explored = 0

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        nodes_explored += 1

        if node == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path, nodes_explored

        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                parent[neighbor] = node
                stack.append(neighbor)

    return None, nodes_explored

def dfs_path(graph, start, goal):
    """Valid path from start to goal via DFS, or None if unreachable."""
    path, _ = dfs_target_search(graph, start, goal)
    return path
 
 
# =============================================================================
# [4] APPLICATION: DEPTH MAP (DFS equivalent of bfs_levels)
# Groups nodes by the branch depth at which they were discovered.
# =============================================================================
 
def dfs_depths(graph, start):
    """Group reachable nodes by their DFS discovery depth from start."""
    _, _, depth = dfs_traversal(graph, start)
    depths = {}
    for node, d in depth.items():
        depths.setdefault(d, []).append(node)
    return depths
 
 
# =============================================================================
# [5] APPLICATION: CONNECTED COMPONENTS (undirected graphs)
# Start a fresh DFS from every unvisited node; each DFS finds one component.
# =============================================================================
 
def dfs_connected_components(graph):
    """Connected components of an undirected graph, as a list of node lists."""
    seen = set()
    components = []
    for node in graph:
        if node not in seen:
            order, _, _ = dfs_traversal(graph, node)
            seen.update(order)
            components.append(order)
    return components
 
 
# =============================================================================
# [6] APPLICATION: TOPOLOGICAL SORT (directed acyclic graphs)
# Post-order DFS with 3-state cycle detection (0=unvisited, 1=visiting, 2=done).
# =============================================================================
 
def dfs_topological_sort(graph):
    """DFS Post-order topological sort. Returns an order, or None if the graph has a cycle."""
    state = {node: 0 for node in graph}
    order = []

    def visit(node):
        state[node] = 1 # mark as currently on recursion stack
        for neighbor in graph.get(node, []):
            neighbor_state = state.get(neighbor, 0)
            if neighbor_state == 1:
                return False # cycle exists
            if neighbor_state == 0:
                if not visit(neighbor):
                    return False
        state[node] = 2 # finished exploring all descendents
        order.append(node)
        return True

    for node in graph:
        if state[node] == 0:
            if not visit(node):
                return None

    order.reverse()
    return order
 
 
# =============================================================================
# [7] TIMING HELPERS (for the comparison section)
# =============================================================================
 
def time_dfs(graph, start, runs=1000):
    """Average seconds per full DFS traversal."""
    begin = time.perf_counter()
    for _ in range(runs):
        dfs_traversal(graph, start)
    return (time.perf_counter() - begin) / runs

def time_dfs_target(graph, start, goal, runs=1000):
    """Average seconds until target discovery via early-stopping DFS."""
    begin = time.perf_counter()
    for _ in range(runs):
        dfs_target_search(graph, start, goal)
    return (time.perf_counter() - begin) / runs
 
 
# =============================================================================
# [8] DEMO RUN (executes when run directly, matches bfs_module.py output)
# =============================================================================
 
if __name__ == "__main__":
    order, parent, depth = dfs_traversal(UNDIRECTED, "A")
    print("DFS visit order from A:", order)
    print("Discovery depths from A:", depth)
    print("Depth groups from A:", dfs_depths(UNDIRECTED, "A"))
    print("DFS path A -> F:", dfs_path(UNDIRECTED, "A", "F"))
    print("DFS path A -> G:", dfs_path(UNDIRECTED, "A", "G"))
    print("Connected components:", dfs_connected_components(UNDIRECTED))
    print("Topological order (DFS):", dfs_topological_sort(DAG))
    print(f"Avg full traversal time: {time_dfs(UNDIRECTED, 'A') * 1e6:.2f} microseconds")
    print(f"Avg target discovery time (A -> F): {time_dfs_target(UNDIRECTED, 'A', 'F') * 1e6:.2f} microseconds")
