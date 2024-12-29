import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class EdmondsKarp:
    def __init__(self, vertices):   
        self.V = vertices
        self.capacity = [[0] * self.V for _ in range(self.V)]
        self.adj = [[] for _ in range(self.V)]
        self.flow_paths = []
        self.current_step = 0
        self.total_flow = 0

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
            path = []

            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v])
                path.append((u, v))
                v = u
            path.reverse()
            self.flow_paths.append((path, path_flow))

            v = t
            while v != s:
                u = parent[v]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow
                v = u

            max_flow += path_flow

        self.total_flow = max_flow
        return max_flow

class MaxFlowVisualizer:
    def __init__(self, graph, source, sink):
        
        self.graph = graph
        self.source = source
        self.sink = sink
        self.G = nx.DiGraph()
        self.pos = None
        
        self.root = tk.Tk()
        self.root.title("Edmonds-Karp Algorithm Visualization")
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10)

        self.info_frame = ttk.Frame(self.root)
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        self.info_text = tk.Text(self.info_frame, wrap=tk.WORD, width=40, height=20)
        self.info_text.pack(expand=True, fill="both")

        self.next_button = ttk.Button(self.root, text="Next Step", command=self.next_step)
        self.next_button.grid(row=1, column=0, columnspan=2, pady=10)
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.next_button = ttk.Button(button_frame, text="Next Step", command=self.next_step)
        self.next_button.pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=10)

        self.initialize_graph()

    def initialize_graph(self):
        for u in range(self.graph.V):
            for v in self.graph.adj[u]:
                self.G.add_edge(u, v, capacity=self.graph.capacity[u][v])
        self.pos = nx.spring_layout(self.G)
        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        node_colors = ['lightgreen' if node == self.source else 'salmon' if node == self.sink else 'lightblue' for node in self.G.nodes()]
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_color=node_colors, node_size=700, font_size=8, arrows=False)
        
        edge_labels = nx.get_edge_attributes(self.G, 'capacity')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, arrows=False)

        if self.graph.current_step > 0 and self.graph.current_step <= len(self.graph.flow_paths):
            path, _ = self.graph.flow_paths[self.graph.current_step - 1]
            
            edge_colors = ['r' if (u, v) in path or (v, u) in path else 'k' for u, v in self.G.edges()]
            
            flow_graph = nx.DiGraph()
            for u, v in path:
                flow_graph.add_edge(u, v)
            
            nx.draw_networkx_edges(flow_graph, self.pos, ax=self.ax, edge_color='r', width=2, arrows=True, arrowstyle='->', arrowsize=20)

        self.ax.set_title(f"Step {self.graph.current_step}")
        self.canvas.draw()

    def next_step(self):
        if self.graph.current_step < len(self.graph.flow_paths):
            self.graph.current_step += 1
            self.update_graph()
            self.update_info()
        elif self.graph.current_step == len(self.graph.flow_paths):
            self.graph.current_step += 1
            self.update_info()
            self.next_button.config(state="disabled")

    def update_info(self):
        self.info_text.delete(1.0, tk.END)
        if self.graph.current_step == 0:
            self.info_text.insert(tk.END, "Initial Graph\n\n")
            self.info_text.insert(tk.END, f"Source: {self.source}\n")
            self.info_text.insert(tk.END, f"Sink: {self.sink}\n")
        elif self.graph.current_step <= len(self.graph.flow_paths):
            path, flow = self.graph.flow_paths[self.graph.current_step - 1]
            self.info_text.insert(tk.END, f"Step {self.graph.current_step}\n\n")
            self.info_text.insert(tk.END, f"Path: {' -> '.join(map(str, [u for u, v in path] + [self.sink]))}\n")
            self.info_text.insert(tk.END, f"Flow: {flow}\n")
        else:
            self.info_text.insert(tk.END, "Algorithm Complete\n\n")
            self.info_text.insert(tk.END, f"Maximum Flow: {self.graph.total_flow}\n")

    def run(self):
        self.update_info()
        self.root.mainloop()

def create_graph(node_count, edge_set):
    graph = EdmondsKarp(node_count)
    for u, v, cap in edge_set:
        graph.add_edge(u, v, cap)
    return graph

def main():
    node_counts = [10, 15, 20, 25, 30]
    selected_node_count = random.choice(node_counts)
    selected_edge_set = random.choice(edge_sets[selected_node_count])

    graph = create_graph(selected_node_count, selected_edge_set)
    source = 0
    sink = selected_node_count - 1

    graph.max_flow(source, sink)
    visualizer = MaxFlowVisualizer(graph, source, sink)
    visualizer.run()

if __name__ == "__main__":
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
    
    main()