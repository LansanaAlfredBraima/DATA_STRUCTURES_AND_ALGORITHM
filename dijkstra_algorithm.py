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
        self.path_edges = set() # Stores edges for the final path
        self.is_animating = False
        self.animation_speed = 1000
        self.zoom_scale = 1.0
        
        # Colors - Premium Palette
        self.colors = {
            'bg': "#0f172a",          # Deep slate blue/black
            'canvas_bg': "#1e293b",   # Lighter slate for canvas
            'node': "#3b82f6",        # Bright Blue
            'node_border': "#60a5fa", # Lighter Blue
            'node_text': "#f8fafc",   # White-ish
            'edge': "#475569",        # Slate gray
            'visited': "#10b981",     # Emerald Green
            'current': "#f43f5e",     # Rose Red
            'path': "#fbbf24",        # Bright Yellow-Orange (Amber-400)
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
            bg=self.colors['canvas_bg'],
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

        tk.Label(
            control_frame,
            text="Target Node:",
            bg=self.colors['bg'],
            fg=self.colors['node_text']
        ).grid(row=0, column=2, padx=5)

        self.target_node_var = tk.StringVar(value='F')
        self.target_combo = ttk.Combobox(
            control_frame,
            textvariable=self.target_node_var,
            values=self.node_ids,
            width=5,
            state="readonly"
        )
        self.target_combo.grid(row=0, column=3, padx=5)
        
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
        self.run_btn.grid(row=0, column=4, padx=10)
        
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
        self.reset_btn.grid(row=0, column=5, padx=5)
        
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
            width = 3 * self.zoom_scale
            
            # Highlight path edges
            if self.is_edge_in_path(u, v):
                color = self.colors['path']
                width = 6 * self.zoom_scale
                # Glow effect for path
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=width+4, tags="edge",
                    stipple="gray50" # Simple glow simulation
                )
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color, width=width, tags="edge",
                capstyle=tk.ROUND
            )
            
            # Draw weight badge
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Background for weight text (Pill shape)
            text_len = len(str(w)) * 10
            r = 12 * self.zoom_scale
            self.canvas.create_rectangle(
                mid_x-15, mid_y-10, mid_x+15, mid_y+10,
                fill=self.colors['canvas_bg'], outline=self.colors['edge'],
                width=1
            )
            self.canvas.create_text(
                mid_x, mid_y,
                text=str(w),
                fill=self.colors['node_text'],
                font=("Segoe UI", int(10*self.zoom_scale), "bold")
            )
            
        # Draw nodes
        for id, node in self.nodes.items():
            fill_color = self.colors['node']
            outline_color = self.colors['node_border']
            
            if id in self.visited:
                fill_color = self.colors['visited']
                outline_color = "#34d399"
            if id == self.current_node:
                fill_color = self.colors['current']
                outline_color = "#fb7185"
                
            x, y = node.x * self.zoom_scale, node.y * self.zoom_scale
            r = 28 * self.zoom_scale
            
            # Shadow/Glow effect
            self.canvas.create_oval(
                x-r-2, y-r-2, x+r+2, y+r+2,
                fill="#000000", outline="", stipple="gray25"
            )
            
            # Main Node Body
            self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill=fill_color, outline=outline_color, width=3
            )
            
            # Inner Shine (Gradient emulation)
            self.canvas.create_oval(
                x-r+5, y-r+5, x+r-5, y+r-5,
                fill="", outline="#ffffff", width=1, tags="shine"
            )
            
            # Node ID
            self.canvas.create_text(
                x, y,
                text=id,
                fill="#ffffff",
                font=("Segoe UI", int(16*self.zoom_scale), "bold")
            )
            
            # Distance label (above node)
            dist_text = "∞"
            dist_color = self.colors['edge']
            if id in self.distances and self.distances[id] != float('inf'):
                dist_text = str(self.distances[id])
                dist_color = self.colors['path']
                
            # Distance Pill
            self.canvas.create_rectangle(
                 x-20, y - 50*self.zoom_scale - 10, x+20, y - 50*self.zoom_scale + 10,
                 fill=self.colors['bg'], outline=dist_color, width=1
            )
            
            self.canvas.create_text(
                x, y - 50*self.zoom_scale,
                text=dist_text,
                fill=self.colors['node_text'],
                font=("Segoe UI", int(10*self.zoom_scale), "bold")
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
        # Only highlight if explicitly in the final path set
        return (u, v) in self.path_edges or (v, u) in self.path_edges

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
        target_node = self.target_node_var.get()
        
        if start_node == target_node:
             tk.messagebox.showwarning("Invalid Selection", "Start and Target nodes must be different!")
             return

        self.reset_graph(keep_start=True)
        
        # Initialize
        self.distances = {node: float('inf') for node in self.node_ids}
        self.distances[start_node] = 0
        self.unvisited = set(self.node_ids)
        
        self.is_animating = True
        self.run_btn.config(state=tk.DISABLED)
        self.start_combo.config(state=tk.DISABLED)
        self.target_combo.config(state=tk.DISABLED)
        
        self.animate_step()

    def animate_step(self):
        """Execute one step of Dijkstra's"""
        if not self.unvisited:
            self.is_animating = False
            self.current_node = None
            self.draw_graph()
            self.current_node = None
            self.draw_graph()
            self.status_label.config(text="Exploration Complete! Tracing shortest path...")
            self.root.after(1000, self.trace_path)
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

    def trace_path(self):
        """Trace path from Start to Target"""
        target = self.target_node_var.get()
        start = self.start_node_var.get()
        
        path = []
        curr = target
        while curr in self.previous:
            path.append(curr)
            curr = self.previous[curr]
            if curr == start:
                path.append(start)
                break
        
        if not path or path[-1] != start:
             self.status_label.config(text=f"No path found from {start} to {target}!")
             self.finish_animation()
             return

        path.reverse() # Start to Target
        self.animate_path_sequence(path, 0)

    def animate_path_sequence(self, path, index):
        if index >= len(path):
            dist = self.distances[self.target_node_var.get()]
            path_str = " -> ".join(path)
            self.status_label.config(
                text=f"✅ Destination Reach! Path: {path_str} | Total Distance: {dist}", 
                font=("Arial", 12, "bold")
            )
            self.finish_animation()
            return
            
        node = path[index]
        
        # Add edge to path_edges if not the first node
        if index > 0:
            prev = path[index-1]
            self.path_edges.add((prev, node))
            self.path_edges.add((node, prev))
            
        self.current_node = node
        self.draw_graph()
        
        # Highlight accumulated edges logic could go here if we wanted to show the worm crawling
        
        delay = self.speed_scale.get()
        self.root.after(delay, lambda: self.animate_path_sequence(path, index + 1))

    def finish_animation(self):
        self.is_animating = False
        self.run_btn.config(state=tk.NORMAL)
        self.start_combo.config(state=tk.NORMAL)
        self.target_combo.config(state=tk.NORMAL)

    def reset_graph(self, keep_start=False):
        """Reset the graph state"""
        self.is_animating = False
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.current_node = None
        self.path_edges = set()
        self.unvisited = set()
        
        if not keep_start:
            self.start_node_var.set('A')
            self.target_node_var.set('F')
            
        self.draw_graph()
        self.update_table()
        self.status_label.config(text="Ready to start...", font=("Arial", 12))
        self.run_btn.config(state=tk.NORMAL)
        self.start_combo.config(state=tk.NORMAL)
        self.target_combo.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = DijkstraAlgorithm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
