"""
Dijkstra's Algorithm - Visual Implementation
Author: DSA Project
Description: Interactive visualization of Dijkstra's Shortest Path Algorithm on a graph
"""

import tkinter as tk
from tkinter import ttk
import math
import time

class GraphNode:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class DijkstraAlgorithm:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Algorithm - Visual Implementation")
        self.root.geometry("900x600")
        self.root.configure(bg="#222831")
        
        # Graph data
        self.nodes = {}
        self.edges = {}
        self.adj_matrix = []
        self.node_ids = []
        
        # Algorithm state
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.current_node = None
        self.is_animating = False
        self.animation_speed = 1000
        self.zoom_scale = 1.0
        
        # Colors
        self.colors = {
            'bg': "#222831",
            'node': "#00adb5",
            'node_text': "#eeeeee",
            'edge': "#393e46",
            'visited': "#76b041",
            'current': "#ff2e63",
            'path': "#fce38a",
            'infinity': "∞"
        }
        
        self.setup_graph()
        self.setup_ui()
        self.draw_graph()
        
    def setup_graph(self):
        """Setup the graph structure (based on typical assignment graphs)"""
        # Define nodes with positions
        # Using a layout similar to the assignment figure (assumed)
        node_positions = {
            'A': (100, 300),
            'B': (300, 100),
            'C': (300, 500),
            'D': (500, 100),
            'E': (500, 500),
            'F': (700, 300)
        }
        
        for id, (x, y) in node_positions.items():
            self.nodes[id] = GraphNode(id, x, y)
            self.node_ids.append(id)
            
        # Define edges with weights
        self.edges = {
            ('A', 'B'): 4, ('A', 'C'): 2,
            ('B', 'C'): 1, ('B', 'D'): 5,
            ('C', 'D'): 8, ('C', 'E'): 10,
            ('D', 'E'): 2, ('D', 'F'): 6,
            ('E', 'F'): 3
        }
        
        # Initialize adjacency matrix
        n = len(self.node_ids)
        self.adj_matrix = [[0] * n for _ in range(n)]
        
        for (u, v), w in self.edges.items():
            i, j = self.node_ids.index(u), self.node_ids.index(v)
            self.adj_matrix[i][j] = w
            self.adj_matrix[j][i] = w  # Undirected graph

    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="📍 Dijkstra's Shortest Path",
            font=("Arial", 32, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['node']
        )
        title_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Graph Visualization
        left_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            left_frame,
            width=800,
            height=600,
            bg="#393e46",
            highlightthickness=0
        )
        
        h_scroll = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right side - Controls and Table
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'], width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        
        # Controls
        control_frame = tk.LabelFrame(
            right_frame,
            text="Controls",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['node_text'],
            padx=10, pady=10
        )
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            control_frame,
            text="Start Node:",
            bg=self.colors['bg'],
            fg=self.colors['node_text']
        ).grid(row=0, column=0, padx=5)
        
        self.start_node_var = tk.StringVar(value='A')
        self.start_combo = ttk.Combobox(
            control_frame,
            textvariable=self.start_node_var,
            values=self.node_ids,
            width=5,
            state="readonly"
        )
        self.start_combo.grid(row=0, column=1, padx=5)
        
        self.run_btn = tk.Button(
            control_frame,
            text="▶ Run Algorithm",
            font=("Arial", 11, "bold"),
            bg=self.colors['node'],
            fg="#ffffff",
            command=self.run_algorithm,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.run_btn.grid(row=0, column=2, padx=10)
        
        self.reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset",
            font=("Arial", 11, "bold"),
            bg=self.colors['current'],
            fg="#ffffff",
            command=self.reset_graph,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # Speed control
        tk.Label(
            control_frame,
            text="Speed:",
            bg=self.colors['bg'],
            fg=self.colors['node_text']
        ).grid(row=1, column=0, padx=5, pady=10)
        
        self.speed_scale = tk.Scale(
            control_frame,
            from_=200,
            to=2000,
            orient=tk.HORIZONTAL,
            bg=self.colors['bg'],
            fg=self.colors['node_text'],
            highlightthickness=0,
            length=200
        )
        self.speed_scale.set(1000)
        self.speed_scale.grid(row=1, column=1, columnspan=3)
        
        # Zoom Controls
        tk.Label(
            control_frame,
            text="Zoom:",
            bg=self.colors['bg'],
            fg=self.colors['node_text']
        ).grid(row=2, column=0, padx=5, pady=10)
        
        zoom_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        zoom_frame.grid(row=2, column=1, columnspan=3, sticky="w")
        
        tk.Button(
            zoom_frame,
            text="🔍+",
            font=("Arial", 10, "bold"),
            bg=self.colors['node'],
            fg="#ffffff",
            command=self.zoom_in,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            zoom_frame,
            text="🔍-",
            font=("Arial", 10, "bold"),
            bg=self.colors['node'],
            fg="#ffffff",
            command=self.zoom_out,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Distance Table
        table_frame = tk.LabelFrame(
            right_frame,
            text="Shortest Path Distances",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['node_text'],
            padx=10, pady=10
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('node', 'dist', 'prev')
        self.tree_view = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        self.tree_view.heading('node', text='Node')
        self.tree_view.heading('dist', text='Distance')
        self.tree_view.heading('prev', text='Previous')
        
        self.tree_view.column('node', width=80, anchor='center')
        self.tree_view.column('dist', width=100, anchor='center')
        self.tree_view.column('prev', width=100, anchor='center')
        
        self.tree_view.pack(fill=tk.BOTH, expand=True)
        
        # Log/Status
        self.status_label = tk.Label(
            right_frame,
            text="Ready to start...",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg="#fce38a",
            wraplength=350,
            justify=tk.LEFT
        )
        self.status_label.pack(fill=tk.X, pady=10)

    def draw_graph(self):
        """Draw the graph on canvas"""
        self.canvas.delete("all")
        
        # Draw edges
        for (u, v), w in self.edges.items():
            n1 = self.nodes[u]
            n2 = self.nodes[v]
            
            # Apply zoom
            x1, y1 = n1.x * self.zoom_scale, n1.y * self.zoom_scale
            x2, y2 = n2.x * self.zoom_scale, n2.y * self.zoom_scale
            
            # Determine edge color
            color = self.colors['edge']
            width = 2 * self.zoom_scale
            
            # Highlight path edges
            if self.is_edge_in_path(u, v):
                color = self.colors['path']
                width = 4 * self.zoom_scale
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color, width=width, tags="edge"
            )
            
            # Draw weight
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Background for weight text
            r = 12 * self.zoom_scale
            self.canvas.create_oval(
                mid_x-r, mid_y-r, mid_x+r, mid_y+r,
                fill="#222831", outline=""
            )
            self.canvas.create_text(
                mid_x, mid_y,
                text=str(w),
                fill="#eeeeee",
                font=("Arial", int(10*self.zoom_scale), "bold")
            )
            
        # Draw nodes
        for id, node in self.nodes.items():
            color = self.colors['node']
            if id in self.visited:
                color = self.colors['visited']
            if id == self.current_node:
                color = self.colors['current']
                
            x, y = node.x * self.zoom_scale, node.y * self.zoom_scale
            r = 25 * self.zoom_scale
            
            self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill=color, outline="#eeeeee", width=2
            )
            
            # Node ID
            self.canvas.create_text(
                x, y,
                text=id,
                fill="#ffffff",
                font=("Arial", int(14*self.zoom_scale), "bold")
            )
            
            # Distance label (above node)
            dist_text = "∞"
            if id in self.distances:
                dist_text = str(self.distances[id])
                
            self.canvas.create_text(
                x, y - 40*self.zoom_scale,
                text=f"d={dist_text}",
                fill="#fce38a",
                font=("Arial", int(10*self.zoom_scale))
            )
            
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        self.zoom_scale *= 1.1
        self.draw_graph()

    def zoom_out(self):
        self.zoom_scale /= 1.1
        self.draw_graph()

    def is_edge_in_path(self, u, v):
        """Check if edge is part of shortest path tree"""
        if v in self.previous and self.previous[v] == u:
            return True
        if u in self.previous and self.previous[u] == v:
            return True
        return False

    def update_table(self):
        """Update the distance table"""
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
            
        for node in self.node_ids:
            dist = self.distances.get(node, float('inf'))
            dist_str = "∞" if dist == float('inf') else str(dist)
            prev = self.previous.get(node, "-")
            
            self.tree_view.insert('', 'end', values=(node, dist_str, prev))

    def run_algorithm(self):
        """Start Dijkstra's algorithm"""
        if self.is_animating:
            return
            
        start_node = self.start_node_var.get()
        self.reset_graph(keep_start=True)
        
        # Initialize
        self.distances = {node: float('inf') for node in self.node_ids}
        self.distances[start_node] = 0
        self.unvisited = set(self.node_ids)
        
        self.is_animating = True
        self.run_btn.config(state=tk.DISABLED)
        self.start_combo.config(state=tk.DISABLED)
        
        self.animate_step()

    def animate_step(self):
        """Execute one step of Dijkstra's"""
        if not self.unvisited:
            self.is_animating = False
            self.current_node = None
            self.draw_graph()
            self.status_label.config(text="Algorithm Complete! Shortest paths found.")
            self.run_btn.config(state=tk.NORMAL)
            self.start_combo.config(state=tk.NORMAL)
            return

        # Find node with min distance in unvisited
        current = min(self.unvisited, key=lambda node: self.distances[node])
        
        if self.distances[current] == float('inf'):
            # Remaining nodes unreachable
            self.is_animating = False
            self.status_label.config(text="Remaining nodes are unreachable.")
            return
            
        self.current_node = current
        self.unvisited.remove(current)
        self.visited.add(current)
        
        self.status_label.config(text=f"Visiting node {current} (Distance: {self.distances[current]})")
        
        # Update neighbors
        for neighbor in self.node_ids:
            if neighbor in self.unvisited:
                # Check if edge exists
                edge_weight = None
                if (current, neighbor) in self.edges:
                    edge_weight = self.edges[(current, neighbor)]
                elif (neighbor, current) in self.edges:
                    edge_weight = self.edges[(neighbor, current)]
                
                if edge_weight is not None:
                    new_dist = self.distances[current] + edge_weight
                    if new_dist < self.distances[neighbor]:
                        self.distances[neighbor] = new_dist
                        self.previous[neighbor] = current
        
        self.draw_graph()
        self.update_table()
        
        delay = self.speed_scale.get()
        self.root.after(delay, self.animate_step)

    def reset_graph(self, keep_start=False):
        """Reset the graph state"""
        self.is_animating = False
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.current_node = None
        self.unvisited = set()
        
        if not keep_start:
            self.start_node_var.set('A')
            
        self.draw_graph()
        self.update_table()
        self.status_label.config(text="Ready to start...")
        self.run_btn.config(state=tk.NORMAL)
        self.start_combo.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = DijkstraAlgorithm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
