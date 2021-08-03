# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Several graph algorithms."""

# With DFS, we can classify the edges in a directed or undirected graph:
# 
# 1. A tree edge is (u,v) if v was first discovered by exploring edge (u,v). All the edges in the depth-first forest G(parent) (aka the predecessor subgraph) are tree edges (but the reverse does not always hold - not all tree edges are in G(pa)).
# 2. A back edge is (u,v) connecting u to an ancestor v in a depth-first tree. For 
# directed graphs, we consider self-loops to be back edges.
# 3. A forward edge is a non-tree edge (u,v) connecting u to a descendant v.
# 4. All other edges that is not any of the above kind are called cross edges.
# 5. For undirected graphs, we classify the edge as the first type in the list 
# above; and we classify the edge according to whichever of (u,v) or (v,u) the DFS 
# encounters first.
#
# When we first explore an edge (u,v), if:
# a) v.color = WHITE: then this is a tree edge.
# b) v.color = GRAY: then this is a back edge, since the gray vertices always form 
# a linear chain of descendants corresponding to the stack of active _dfs_visit() 
# invocations. Exploration always proceeds from the deepest (latest) gray vertex, 
# so an edge that reaches another gray vertex must have reached an ancestor.
# c) v.color = BLACK (only possible for a directed graph): then this is a forward 
# or cross edge. When u.grayed_time < v.grayed_time, it is a forward edge; if >, 
# it is a cross edge.
#
# According to CLRS Theorem 22.10, for an undirected graph, every edge is either a 
# tree edge or a back edge (ie there are no forward or cross edges).
# Hence, for an undirected graph, it has a cycle if and only if DFS finds a back 
# edge.

from typing import Sequence, Tuple

import enum

class Color(enum.Enum):
    """Color definition for Graph."""
    
    WHITE = enum.auto()
    GRAY = enum.auto()
    BLACK = enum.auto()

class Graph:
    """Graph represented using adjacency lists. The default is undirected graph."""
    
    def __init__(
        self, num_vertices: int, edges: Sequence[Tuple], is_directed: bool = False
    ) -> None:
        # Adjacency list (ie list of all neighbors) for all vertices
        self.adjlist = [[] for _ in range(num_vertices)]
        for v1, v2 in edges:
            # `edges` is a list of tuples of vertex values like (v1, v2).
            # We want to store the edge info as neighbors for each vertex, so that 
            # we will have an adjacency list
            self.adjlist[v1].append(v2)
            if not is_directed:
                self.adjlist[v2].append(v1)
        self.color: Color = [Color.WHITE] * num_vertices
        # For source vertex and all undiscovered vertices, their parents are None
        self.parent = [None] * num_vertices
        # Distance (ie total num of edges) from source to the vertex
        self.distance = [None] * num_vertices
        # The next attrs are for DFS to store the time when a vertex turns gray/black
        self.timestamp = 0
        self.grayed_time = [None] * num_vertices
        self.blackened_time = [None] * num_vertices
        # Mark the cycle index number of a vertex; `None` if it belongs to no cycle
        self.cycle_mark = [None] * max(num_vertices, len(edges))
        # Total number of cycles in the graph
        self.num_cycles = 0
    
    def __repr__(self) -> str:
        """Representation showing neighbors of each vertex."""
        return "\n".join([f"{i}: {neighbors}" for (i, neighbors) in enumerate(self.adjlist)])
    
    def __str__(self) -> str:
        """Representation."""
        return self.__repr__()
    
    def adjacency_matrix(self) -> list:
        """Get the adjacency matrix."""
        adjmat = [[0] * len(self.adjlist) for _ in range(len(self.adjlist))]
        for i, neighbors in enumerate(self.adjlist):
            for j in neighbors:
                adjmat[i][j] = 1
        return adjmat
    
    def breadth_first_search(self, source: int) -> list:
        """Breadth-first search (BFS) of a graph from vertex `source`, cf CLRS 22.2."""
        # Time complexity: O(num_vertices + num_edges), aka O(V+E)
        
        # Note: This initialization is a must, since other methods may change defaults
        self.color = [Color.WHITE] * len(self.adjlist)
        # For source vertex and all undiscovered vertices, their parents are None
        self.parent = [None] * len(self.adjlist)
        # Distance (ie total num of edges) from source to the vertex
        self.distance = [None] * len(self.adjlist)
            
        # Source is discovered, but not all its neighbors are discovered, so gray
        self.color[source] = Color.GRAY
        self.distance[source] = 0
        queue = []  # Use-and-discard FIFO queue
        traversal = []  # Record the BFS traversal route
        queue.append(source)
        traversal.append(source)
        while queue:
            # We use queue as FIFO here
            u = queue.pop(0)
            for v in self.adjlist[u]:
                if self.color[v] == Color.WHITE:
                    # White means undiscovered, so discover it
                    self.color[v] = Color.GRAY
                    self.distance[v] = self.distance[u] + 1
                    self.parent[v] = u
                    queue.append(v)
                    traversal.append(v)
            # When u's adjlist is exhausted, turn u to black
            self.color[u] = Color.BLACK
        return traversal
    
    def shortest_path(self, source: int, vertex: int) -> list:
        """Return the shortest path from vertex `source` to `vertex`.
        
        Note
        ----
        The length of the shortest path (when one exists) is trivial: `len(returning list)-1`.
        """
        # Time complexity: O(num of vertices in the path)
        
        # First, we need to compute all vertices' parents using b_f_s()
        _ = self.breadth_first_search(source)
        if vertex == source:
            return [source]
        elif self.parent[vertex] is None:
            print(f"No path from {source} to {vertex} exists.")
            return []
        else:
            return self.shortest_path(source, self.parent[vertex]) + [vertex]
    
    def breadth_first_search_jovian(self, source: int) -> list:
        """Breadth-first search (BFS) traversal of a graph from vertex `source`."""
        # Time complexity: O(num_vertices + num_edges), aka O(V+E)
        visited = [False] * len(self.adjlist)
        queue = []  # same as `traversal` in the above breadth_first_search()
        
        # Label root (ie source) as visited
        visited[source] = True
        queue.append(source)
        
        i = 0
        while i < len(queue):
            for v in self.adjlist[queue[i]]:
                # v is a neighbor of queue[i] (starting from queue[0]=source)
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
            i += 1
        return queue


    def depth_first_search(self) -> list:
        """Depth-first search (DFS) of a graph, cf CLRS 22.3."""
        # Time complexity: Theta(V + E)
        
        # Note: This initialization is a must, since other methods may change defaults
        self.color = [Color.WHITE] * len(self.adjlist)
        # For source vertex and all undiscovered vertices, their parents are None
        self.parent = [None] * len(self.adjlist)
        self.timestamp = 0
        # `predsubg` is the predecessor subgraph: G(parent) = (V, E(parent)), where 
        # E(parent) = {(v.pa, v): v in G.V and v.pa is not None}.
        # Note: Depending on the tree structure, predsubg may not include ALL edges of 
        # the original graph. But we are sure that predsubg does not include duplicate 
        # edges, and does not have any edges that are not present in the original graph.
        predsubg = [None] * len(self.adjlist)
        for vertex in range(len(self.adjlist)):
            if self.color[vertex] == Color.WHITE:
                # Every time _dfs_visit(vertex) is called, `vertex` becomes the root of 
                # a new tree in the depth-first forest
                predsubg[vertex] = self._dfs_visit(vertex)
        return predsubg, self.grayed_time, self.blackened_time
    
    def _dfs_visit(self, vertex: int) -> list:
        # Visit all neighbors of `vertex` using DFS approach.
        traversal = []
        # White `vertex` is discovered, so it turns gray
        self.timestamp += 1
        self.grayed_time[vertex] = self.timestamp
        self.color[vertex] = Color.GRAY
        for v in self.adjlist[vertex]:
            # Edge (vertex, v) is being explored by the DFS
            if self.color[v] == Color.WHITE:
                self.parent[v] = vertex
                traversal += [(vertex, v)] + self._dfs_visit(v)
            elif self.color[v] == Color.GRAY:
                # TODO: For an undirected graph, this means (u,v) is a back edge, which means there is a cycle
                # print('cyc', traversal + [(v, self.parent[v])])
                pass
        # When all neighbors of `vertex` have been exhausted, it turns black
        self.color[vertex] = Color.BLACK
        self.timestamp += 1
        self.blackened_time[vertex] = self.timestamp
        return traversal
    
    def depth_first_search_jovian(self, source: int) -> list:
        """Depth-first search (DFS) traversal of a graph from vertex `source`."""
        # DFS is more memory efficient than BFS, since you can backtrack sooner.
        visited = [False] * len(self.adjlist)
        queue = []
        stack = [source]
        
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                for neighbor in self.adjlist[v]:
                    # Push (ie append) all neighbors of v into stack for next loop
                    stack.append(neighbor)
        return queue
    
    def is_cyclic(self) -> bool:
        """Check if the graph has any cycles."""
        visited = [False] * len(self.adjlist)
        for vertex in range(len(self.adjlist)):
            if not visited[vertex] and self._is_subgraph_cyclic(vertex, visited, -1):
                return True
        return False
    
    def _is_subgraph_cyclic(self, v: int, visited: Sequence, parent: int) -> bool:
        # Detect cycles in the subgraph reachable from vertex `v`.
        
        visited[v] = True
        for neighbor in self.adjlist[v]:
            if not visited[neighbor]:
                # If neighbor is not visited, then recurse on it
                if self._is_subgraph_cyclic(neighbor, visited, v):
                    return True
            elif parent != neighbor:
                # If neighbor has been visited and is not the parent of v, 
                # then there is a cycle
                return True
        return False
    
    def dfs_cycle(self, u: int, p: int) -> None:
        """Mark the vertices with different numbers for different cycles."""
        if p is None:
            # This initialization is a must, since other methods may change defaults
            self.color = [Color.WHITE] * len(self.adjlist)
            # For source vertex and all undiscovered vertices, their parents are None
            self.parent = [None] * len(self.adjlist)
            # Store total number of cycles found; also used as current cycle's index num
            self.num_cycles = 0
        
        if self.color[u] == Color.GRAY:
            # A vertex that is discovered but not finished.
            # For an undirected graph, this means we have discovered a back edge, which 
            # means there is a cycle. So we backtrack based on parents to find whole cyc
            self.num_cycles += 1
            current = p
            self.cycle_mark[current] = self.num_cycles
            while current != u:
                # Backtrack the parent of current, until the cycle is exhausted
                current = self.parent[current]
                self.cycle_mark[current] = self.num_cycles
        elif self.color[u] == Color.WHITE:
            # Set p to be u's parent, and mark u as (first) discovered
            self.parent[u] = p
            self.color[u] = Color.GRAY
            for v in self.adjlist[u]:
                # Edge (u, v) is being explored by the DFS
                if v != self.parent[u]:
                    self.dfs_cycle(v, u)
            # Now u is finished
            self.color[u] = Color.BLACK
    
    def print_cycles(self, edges: Sequence[Tuple]) -> None:
        """Print and return the cycles in the graph."""
        self.dfs_cycle(0, None)
        cycles = [[] for _ in range(self.num_cycles + 1)] 
        for i in range(len(self.adjlist)):
            if self.cycle_mark[i] is not None:
                print(i, self.cycle_mark, cycles)
                cycles[self.cycle_mark[i]].append(i)
        for i in range(1, self.num_cycles + 1):
            print(f"Cycle #{i}:", *cycles[i])
        print()
        return cycles[1:]


##########################################
### Driver code

edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4), (1, 3)]
g1 = Graph(5, edges)
print(g1)
print('Adjacent matrix:', g1.adjacency_matrix())
print('BFS:', g1.breadth_first_search(3))
print('BFS jovian:', g1.breadth_first_search_jovian(3))
print('Shortest path:', g1.shortest_path(2, 4))
print('DFS:', g1.depth_first_search())
print('DFS jovian:', g1.depth_first_search_jovian(0))
print('Has cycles:', g1.is_cyclic())
print(g1.print_cycles(edges))

# Has a small cycle
edges = [(0, 1), (0, 3), (1, 2), (2, 0), (3, 4)]
g = Graph(5, edges)
print(g)
print(g.depth_first_search())
print(g.is_cyclic())
print("Cycles: ", g.print_cycles(edges))

# Has a big cycle
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
g = Graph(5, edges)
print(g)
print(g.depth_first_search())
print(g.is_cyclic())
print("Cycles: ", g.print_cycles(edges))

edges = [(0, 1), (0, 3), (3, 1), (1, 4), (4, 3), (2, 4), (2, 5), (5, 5)]
g = Graph(6, edges, is_directed=True)
print(g)
print(g.depth_first_search())
print("Cycles: ", g.print_cycles(edges))

edges = [(0, 1), (1, 2), (2, 3), (1, 4), (5, 6), (5, 7)]
g = Graph(8, edges, is_directed=True)
print(g)
print(g.depth_first_search())