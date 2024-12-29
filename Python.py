import random
import time
from collections import deque
import tracemalloc  # Importing tracemalloc for memory tracking

class EdmondsKarp:
    def __init__(self, vertices):
        self.V = vertices
        self.capacity = [[0] * self.V for _ in range(self.V)]
        self.adj = [[] for _ in range(self.V)]

    def add_edge(self, u, v, cap):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.capacity[u][v] = cap

    def bfs(self, s, t, parent):
        visited = [False] * self.V
        queue = deque([s])
        visited[s] = True
        parent[s] = -1

        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if not visited[v] and self.capacity[u][v] > 0:
                    queue.append(v)
                    parent[v] = u
                    visited[v] = True
                    if v == t:
                        return True
        return False

    def max_flow(self, s, t):
        parent = [-1] * self.V
        max_flow = 0

        while self.bfs(s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v])
                v = u

            v = t
            while v != s:
                u = parent[v]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow
                v = u

            max_flow += path_flow

        return max_flow

# Array of possible node counts
node_counts = [10, 15, 20, 25, 30]

# Randomly select a node count
selected_node_count = random.choice(node_counts)
print(f"Randomly selected node count: {selected_node_count}")

# Create the graph with the selected number of nodes
graph = EdmondsKarp(selected_node_count)

# Create two edge sets for each possible node count
edge_sets = {
        10: [
        [
            (0, 1, 10), (1, 2, 8), (2, 3, 5), (3, 4, 7), (4, 5, 6),
            (5, 6, 4), (6, 7, 9), (7, 8, 3), (8, 9, 5), (0, 9, 2),
            (1, 5, 4), (2, 6, 3), (3, 7, 6), (4, 8, 5), (0, 5, 7)
        ],
        [
            (0, 2, 7), (2, 4, 5), (4, 6, 8), (6, 8, 6), (8, 1, 4),
            (1, 3, 9), (3, 5, 3), (5, 7, 5), (7, 9, 7), (9, 0, 2),
            (0, 7, 6), (1, 8, 3), (2, 9, 4), (3, 6, 5), (4, 5, 8)
        ]
    ],
    15: [
        [
            (0, 1, 12), (1, 2, 10), (2, 3, 8), (3, 4, 9), (4, 5, 7),
            (5, 6, 11), (6, 7, 6), (7, 8, 8), (8, 9, 5), (9, 10, 7),
            (10, 11, 9), (11, 12, 6), (12, 13, 8), (13, 14, 10), (0, 14, 5),
            (1, 7, 7), (2, 8, 6), (3, 9, 5), (4, 10, 8), (5, 11, 7),
            (6, 12, 9), (7, 13, 6), (8, 14, 8), (0, 10, 4), (1, 11, 5)
        ],
        [
            (0, 3, 9), (3, 6, 7), (6, 9, 8), (9, 12, 6), (12, 14, 5),
            (1, 4, 11), (4, 7, 8), (7, 10, 7), (10, 13, 9), (13, 0, 6),
            (2, 5, 10), (5, 8, 6), (8, 11, 8), (11, 14, 7), (14, 2, 5),
            (0, 8, 7), (1, 9, 6), (2, 10, 8), (3, 11, 5), (4, 12, 7),
            (5, 13, 9), (6, 14, 6), (7, 0, 8), (8, 1, 5), (9, 2, 7)
        ]
    ],
    20: [
        [
            (0, 1, 15), (1, 2, 12), (2, 3, 10), (3, 4, 8), (4, 5, 11),
            (5, 6, 9), (6, 7, 13), (7, 8, 7), (8, 9, 10), (9, 10, 6),
            (10, 11, 8), (11, 12, 12), (12, 13, 9), (13, 14, 11), (14, 15, 7),
            (15, 16, 10), (16, 17, 8), (17, 18, 9), (18, 19, 11), (0, 19, 6),
            (1, 10, 8), (2, 11, 7), (3, 12, 9), (4, 13, 6), (5, 14, 8),
            (6, 15, 7), (7, 16, 10), (8, 17, 6), (9, 18, 9), (10, 19, 7)
        ],
        [
            (0, 4, 11), (4, 8, 9), (8, 12, 8), (12, 16, 10), (16, 19, 7),
            (1, 5, 13), (5, 9, 7), (9, 13, 11), (13, 17, 8), (17, 0, 9),
            (2, 6, 10), (6, 10, 8), (10, 14, 9), (14, 18, 7), (18, 1, 11),
            (3, 7, 12), (7, 11, 9), (11, 15, 8), (15, 19, 10), (19, 2, 6),
            (0, 10, 8), (1, 11, 7), (2, 12, 9), (3, 13, 6), (4, 14, 10),
            (5, 15, 7), (6, 16, 9), (7, 17, 8), (8, 18, 6), (9, 19, 11)
        ]
    ],
    25: [
        [
            (0, 1, 18), (1, 2, 15), (2, 3, 12), (3, 4, 10), (4, 5, 14),
            (5, 6, 11), (6, 7, 16), (7, 8, 9), (8, 9, 13), (9, 10, 8),
            (10, 11, 10), (11, 12, 15), (12, 13, 11), (13, 14, 14), (14, 15, 9),
            (15, 16, 12), (16, 17, 10), (17, 18, 11), (18, 19, 13), (19, 20, 8),
            (20, 21, 10), (21, 22, 12), (22, 23, 9), (23, 24, 11), (0, 24, 7),
            (1, 12, 9), (2, 13, 8), (3, 14, 10), (4, 15, 7), (5, 16, 9),
            (6, 17, 8), (7, 18, 11), (8, 19, 7), (9, 20, 10), (10, 21, 8)
        ],
        [
            (0, 5, 14), (5, 10, 11), (10, 15, 10), (15, 20, 12), (20, 24, 9),
            (1, 6, 16), (6, 11, 9), (11, 16, 13), (16, 21, 10), (21, 0, 11),
            (2, 7, 12), (7, 12, 10), (12, 17, 11), (17, 22, 9), (22, 1, 13),
            (3, 8, 15), (8, 13, 11), (13, 18, 10), (18, 23, 12), (23, 2, 8),
            (4, 9, 13), (9, 14, 10), (14, 19, 12), (19, 24, 9), (24, 3, 11),
            (0, 12, 10), (1, 13, 9), (2, 14, 11), (3, 15, 8), (4, 16, 12),
            (5, 17, 9), (6, 18, 11), (7, 19, 10), (8, 20, 8), (9, 21, 13)
        ]
    ],
    30: [
        [
            (0, 1, 20), (1, 2, 17), (2, 3, 14), (3, 4, 12), (4, 5, 16),
            (5, 6, 13), (6, 7, 18), (7, 8, 11), (8, 9, 15), (9, 10, 10),
            (10, 11, 12), (11, 12, 17), (12, 13, 13), (13, 14, 16), (14, 15, 11),
            (15, 16, 14), (16, 17, 12), (17, 18, 13), (18, 19, 15), (19, 20, 10),
            (20, 21, 12), (21, 22, 14), (22, 23, 11), (23, 24, 13), (24, 25, 9),
            (25, 26, 11), (26, 27, 13), (27, 28, 10), (28, 29, 12), (0, 29, 8),
            (1, 15, 11), (2, 16, 10), (3, 17, 12), (4, 18, 9), (5, 19, 11),
            (6, 20, 10), (7, 21, 13), (8, 22, 9), (9, 23, 12), (10, 24, 10)
        ],
        [
            (0, 6, 16), (6, 12, 13), (12, 18, 12), (18, 24, 14), (24, 29, 11),
            (1, 7, 18), (7, 13, 11), (13, 19, 15), (19, 25, 12), (25, 0, 13),
            (2, 8, 14), (8, 14, 12), (14, 20, 13), (20, 26, 11), (26, 1, 15),
            (3, 9, 17), (9, 15, 13), (15, 21, 12), (21, 27, 14), (27, 2, 10),
            (4, 10, 15), (10, 16, 12), (16, 22, 14), (22, 28, 11), (28, 3, 13),
            (5, 11, 16), (11, 17, 11), (17, 23, 13), (23, 29, 10), (29, 4, 12),
            (0, 14, 12), (1, 15, 11), (2, 16, 13), (3, 17, 10), (4, 18, 14),
            (5, 19, 11), (6, 20, 13), (7, 21, 12), (8, 22, 10), (9, 23, 15)
        ]
    ]
    }

selected_edge_set = random.choice(edge_sets[selected_node_count])
print(f"Randomly selected edge set: {1 if selected_edge_set == edge_sets[selected_node_count][0] else 2}")

# Add edges from the selected edge set to the graph
for u, v, cap in selected_edge_set:
    graph.add_edge(u, v, cap)

source = 0
sink = selected_node_count - 1

# Measure execution time and memory usage
tracemalloc.start()  # Start tracing memory
start_time = time.time()
max_flow = graph.max_flow(source, sink)
end_time = time.time()
current, peak = tracemalloc.get_traced_memory()  # Get memory usage
tracemalloc.stop()  # Stop tracing memory

execution_time = end_time - start_time
print(f"Maximum flow from source ({source}) to sink ({sink}): {max_flow}")
print(f"Execution time: {execution_time:.6f} seconds")
print(f"Current memory usage: {current / 1024:.2f} KB")
print(f"Peak memory usage: {peak / 1024:.2f} KB")