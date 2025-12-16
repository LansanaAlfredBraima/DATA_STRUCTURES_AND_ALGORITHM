"""
Dijkstra's Algorithm - Visualization
Author: DSA Project
Description: Interactive visualization of Dijkstra's Algorithm with graph rendering.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math

class DijkstraVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Algorithm - Visualization")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1a1a2e")
        
        # Style Configuration
        self.colors = {
            "bg": "#1a1a2e",
            "canvas_bg": "#16213e",
            "node": "#4ECDC4",      # Teal
            "node_highlight": "#FFE66D", # Yellow
            "node_visited": "#FF6B6B",   # Red/Pink
            "node_path": "#00ff88",      # Green
            "text": "#ffffff",
            "edge": "#535c68",
            "edge_highlight": "#ffffff"
        }
        
        self.current_graph = 1
        self.is_running = False
        self.animation_speed = 800
        
        # Graph Data (Adjacency List + Coordinates)
        self.nodes = {}
        self.edges = []
        
        self.setup_ui()
        self.load_graph(1)
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["bg"])
        header_frame.pack(pady=20)
        
        tk.Label(header_frame, text="Dijkstra's Algorithm", font=("Arial", 28, "bold"), 
                 bg=self.colors["bg"], fg="#00d4ff").pack()
        
        # Controls
        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(pady=10)
        
        # Graph Selection
        tk.Label(control_frame, text="Select Graph:", font=("Arial", 12), 
                 bg=self.colors["bg"], fg="white").pack(side=tk.LEFT, padx=10)
        
        self.graph_var = tk.StringVar(value="Figure 1")
        graph_combo = ttk.Combobox(control_frame, textvariable=self.graph_var, 
                                   values=["Figure 1", "Figure 2"], state="readonly", width=15)
        graph_combo.pack(side=tk.LEFT, padx=10)
        graph_combo.bind("<<ComboboxSelected>>", self.change_graph)
        
        # Buttons
        self.btn_run = tk.Button(control_frame, text="Run Dijkstra", bg="#00d4ff", fg="#1a1a2e",
                                 font=("Arial", 11, "bold"), command=self.run_dijkstra)
        self.btn_run.pack(side=tk.LEFT, padx=10)
        
        self.btn_reset = tk.Button(control_frame, text="Reset", bg="#ff6b6b", fg="white",
                                   font=("Arial", 11, "bold"), command=self.reset_graph)
        self.btn_reset.pack(side=tk.LEFT, padx=10)
        
        # Canvas
        self.canvas = tk.Canvas(self.root, bg=self.colors["canvas_bg"], height=500, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Log/Status
        self.status_label = tk.Label(self.root, text="Ready", font=("Courier", 12), 
                                     bg=self.colors["bg"], fg="#a0a0a0")
        self.status_label.pack(pady=10)

    def load_graph(self, graph_id):
        self.current_graph = graph_id
        self.nodes = {}
        self.edges = []  # List of (u, v, weight)
        
        width = 1100
        height = 500
        
        if graph_id == 1:
            # Figure 1 Coordinates
            self.nodes = {
                'A': (150, 100), 'B': (400, 100), 'C': (700, 100),
                'D': (300, 200), 'E': (600, 200),
                'F': (150, 300), 'G': (280, 280), 'H': (450, 280), 'I': (650, 300), 'J': (800, 300),
                'K': (350, 420), 'L': (800, 420)
            }
            # Edges (u, v, weight)
            self.edges = [
                ('A','D',4), ('B','D',8), ('B','C',2),
                ('C','E',5), ('C','J',10),
                ('D','F',6), ('D','G',3), ('D','K',6), ('D','H',9),
                ('E','H',4), ('E','I',9), ('E','J',2),
                ('F','G',1), ('F','K',7),
                ('G','K',4),
                ('H','I',3), ('H','K',6),
                ('I','J',7), ('J','L',1)
            ]
        else:
            # Figure 2 Coordinates
            self.nodes = {
                'A': (150, 100), 'B': (400, 120), 'C': (700, 150),
                'D': (300, 220), 'E': (550, 220), 'F': (800, 250),
                'G': (450, 320), 'H': (700, 350),
                'I': (350, 420), 'J': (650, 420)
            }
            # Edges
            self.edges = [
                ('A','B',2), ('A','D',15),
                ('B','C',3), ('B','D',5), ('B','E',17),
                ('C','E',12), ('C','F',18),
                ('D','E',4), ('D','G',6), 
                ('E','F',13), ('E','G',11),
                ('F','H',7),
                ('G','H',19), ('G','I',9),
                ('H','I',8), ('H','J',16),
                ('I','J',1)
            ]
            
        self.draw_graph()

    def draw_graph(self, highlighted_node=None, visited_nodes=None, path_edges=None):
        self.canvas.delete("all")
        visited_nodes = visited_nodes or set()
        path_edges = path_edges or set()
        
        # Draw Edges
        for u, v, w in self.edges:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            
            color = self.colors["edge"]
            width = 2
            
            # Check if this edge is part of the final path
            if (u, v) in path_edges or (v, u) in path_edges:
                color = self.colors["node_path"]
                width = 4
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
            
            # Draw Weight Label (midpoint)
            mx, my = (x1+x2)/2, (y1+y2)/2
            # Add small offset to not overlap line
            self.canvas.create_text(mx, my-10, text=str(w), fill="#a0a0a0", font=("Arial", 10, "bold"))

        # Draw Nodes
        r = 20 # Radius
        for node, (x, y) in self.nodes.items():
            color = self.colors["node"]
            if node == highlighted_node:
                color = self.colors["node_highlight"]
            elif node in visited_nodes:
                color = self.colors["node_visited"]
            elif node in [n for edge in path_edges for n in edge]: # Rough check for path nodes
                 # This logic is a bit loose, better to pass specific node colors
                 pass

            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=2)
            self.canvas.create_text(x, y, text=node, fill="#1a1a2e", font=("Arial", 12, "bold"))

    def change_graph(self, event):
        selection = self.graph_var.get()
        if selection == "Figure 1":
            self.load_graph(1)
        else:
            self.load_graph(2)
        self.status_label.config(text="Graph Loaded")

    def run_dijkstra(self):
        if self.is_running: return
        self.is_running = True
        self.status_label.config(text="Running Algorithm...", fg=self.colors["node_highlight"])
        
        start_node = 'A'
        target_node = 'L' if self.current_graph == 1 else 'I' # Example target for Fig 2
        
        # Build Adjacency List
        adj = {node: {} for node in self.nodes}
        for u, v, w in self.edges:
            adj[u][v] = w
            adj[v][u] = w
            
        # Dijkstra Logic with Generator for Animation
        def algorithm_step():
            pq = [(0, start_node)]
            distances = {node: float('inf') for node in self.nodes}
            distances[start_node] = 0
            parents = {node: None for node in self.nodes}
            visited = set()
            
            while pq:
                current_dist, current_node = heapq.heappop(pq)
                
                if current_node in visited:
                    continue
                
                visited.add(current_node)
                
                # YIELD STATE FOR ANIMATION
                yield ('VISITING', current_node, visited.copy(), distances.copy())
                
                if current_node == target_node:
                    break
                
                for neighbor, weight in adj[current_node].items():
                    if neighbor in visited:
                        continue
                    new_dist = current_dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        parents[neighbor] = current_node
                        heapq.heappush(pq, (new_dist, neighbor))
            
            # Reconstruct Path
            path = []
            curr = target_node
            while curr:
                path.append(curr)
                curr = parents[curr]
            path = path[::-1]
            
            # Identify path edges
            path_edges = set()
            for i in range(len(path)-1):
                path_edges.add((path[i], path[i+1]))
                
            yield ('FINISHED', path, distances[target_node], path_edges)

        self.anim_gen = algorithm_step()
        self.process_animation()

    def process_animation(self):
        try:
            state = next(self.anim_gen)
            type = state[0]
            
            if type == 'VISITING':
                current_node, visited, dists = state[1], state[2], state[3]
                self.draw_graph(highlighted_node=current_node, visited_nodes=visited)
                self.status_label.config(text=f"Visiting {current_node} (Distance: {dists[current_node]})")
                self.root.after(self.animation_speed, self.process_animation)
                
            elif type == 'FINISHED':
                path, cost, path_edges = state[1], state[2], state[3]
                self.draw_graph(path_edges=path_edges, visited_nodes=set(self.nodes.keys())) # Mark all as visited roughly
                self.status_label.config(text=f"Shortest Path: {' -> '.join(path)} | Cost: {cost}", fg=self.colors["node_path"])
                self.is_running = False
                
        except StopIteration:
            self.is_running = False

    def reset_graph(self):
        self.is_running = False
        self.load_graph(self.current_graph)
        self.status_label.config(text="Ready")

def main():
    root = tk.Tk()
    app = DijkstraVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
