"""
Binary Tree Traversals - Visual Implementation
Author: DSA Project
Description: Interactive visualization of Pre-order, In-order, Post-order, and Level-order traversals
"""

import tkinter as tk
from tkinter import ttk
from collections import deque
import time

class TreeNode:
    """Binary Tree Node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeTraversals:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree Traversals - Visual Implementation")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f0f1e")
        
        # Tree structure (example tree)
        self.tree_root = None
        self.build_sample_tree()
        
        # Visualization variables
        self.node_positions = {}
        self.is_animating = False
        self.current_traversal = []
        self.animation_speed = 800
        self.zoom_scale = 1.0
        
        # Colors
        self.node_color = "#4a90e2"
        self.visited_color = "#00ff88"
        self.current_color = "#ff6b6b"
        self.edge_color = "#ffffff"
        
        self.setup_ui()
        self.draw_tree()
        
    def build_sample_tree(self):
        """Build a sample binary tree"""
        # Creating a sample tree:
        #         1
        #       /   \
        #      2     3
        #     / \   / \
        #    4   5 6   7
        
        self.tree_root = TreeNode(1)
        self.tree_root.left = TreeNode(2)
        self.tree_root.right = TreeNode(3)
        self.tree_root.left.left = TreeNode(4)
        self.tree_root.left.right = TreeNode(5)
        self.tree_root.right.left = TreeNode(6)
        self.tree_root.right.right = TreeNode(7)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#0f0f1e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🌳 Binary Tree Traversals",
            font=("Arial", 32, "bold"),
            bg="#0f0f1e",
            fg="#4a90e2"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Pre-order • In-order • Post-order • Level-order",
            font=("Arial", 14),
            bg="#0f0f1e",
            fg="#a0a0a0"
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#0f0f1e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Tree visualization
        left_frame = tk.Frame(content_frame, bg="#0f0f1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            left_frame,
            width=800,
            height=500,
            bg="#1a1a2e",
            highlightthickness=0
        )
        
        h_scroll = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right side - Controls and output
        right_frame = tk.Frame(content_frame, bg="#0f0f1e", width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20)
        
        # Traversal buttons
        tk.Label(
            right_frame,
            text="Select Traversal:",
            font=("Arial", 16, "bold"),
            bg="#0f0f1e",
            fg="#ffffff"
        ).pack(pady=10)
        
        # Traversal buttons frame
        btn_grid = tk.Frame(right_frame, bg="#0f0f1e")
        btn_grid.pack(pady=10)

        button_configs = [
            ("Pre-order", self.preorder_traversal, "#ff6b6b", 0, 0),
            ("In-order", self.inorder_traversal, "#4ecdc4", 0, 1),
            ("Post-order", self.postorder_traversal, "#ffd93d", 1, 0),
            ("Level-order", self.levelorder_traversal, "#a55eea", 1, 1)
        ]
        
        for text, command, color, r, c in button_configs:
            btn = tk.Button(
                btn_grid,
                text=f"▶ {text}",
                font=("Arial", 12, "bold"),
                bg=color,
                fg="#ffffff",
                padx=10,
                pady=10,
                command=command,
                cursor="hand2",
                relief=tk.FLAT,
                width=15
            )
            btn.grid(row=r, column=c, padx=5, pady=5)
        
        # Reset button
        reset_btn = tk.Button(
            right_frame,
            text="🔄 Reset",
            font=("Arial", 12, "bold"),
            bg="#2d3436",
            fg="#ffffff",
            padx=20,
            pady=10,
            command=self.reset_visualization,
            cursor="hand2",
            relief=tk.FLAT,
            width=20
        )
        reset_btn.pack(pady=10)
        
        # Speed control
        tk.Label(
            right_frame,
            text="Animation Speed:",
            font=("Arial", 12),
            bg="#0f0f1e",
            fg="#ffffff"
        ).pack(pady=5)
        
        self.speed_scale = tk.Scale(
            right_frame,
            from_=200,
            to=2000,
            orient=tk.HORIZONTAL,
            length=250,
            bg="#0f0f1e",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#1a1a2e"
        )
        self.speed_scale.set(800)
        self.speed_scale.pack(pady=5)
        
        # Zoom Controls
        tk.Label(
            right_frame,
            text="Zoom:",
            font=("Arial", 12),
            bg="#0f0f1e",
            fg="#ffffff"
        ).pack(pady=5)
        
        zoom_frame = tk.Frame(right_frame, bg="#0f0f1e")
        zoom_frame.pack(pady=5)
        
        tk.Button(
            zoom_frame,
            text="🔍+",
            font=("Arial", 12, "bold"),
            bg="#4a90e2",
            fg="#ffffff",
            command=self.zoom_in,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            zoom_frame,
            text="🔍-",
            font=("Arial", 12, "bold"),
            bg="#4a90e2",
            fg="#ffffff",
            command=self.zoom_out,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Traversal output
        output_frame = tk.Frame(self.root, bg="#0f0f1e")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        tk.Label(
            output_frame,
            text="Traversal Sequence:",
            font=("Arial", 14, "bold"),
            bg="#0f0f1e",
            fg="#ffffff"
        ).pack(anchor=tk.W)
        
        self.output_text = tk.Text(
            output_frame,
            height=8,
            font=("Courier", 12),
            bg="#1a1a2e",
            fg="#00ff88",
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def calculate_positions(self, node, x, y, level, h_spacing):
        """Calculate positions for all nodes"""
        if node is None:
            return
        
        self.node_positions[node] = (x, y)
        
        # Calculate positions for children
        vertical_spacing = 80
        next_y = y + vertical_spacing
        
        if node.left:
            left_x = x - h_spacing
            self.calculate_positions(node.left, left_x, next_y, level + 1, h_spacing // 2)
        
        if node.right:
            right_x = x + h_spacing
            self.calculate_positions(node.right, right_x, next_y, level + 1, h_spacing // 2)
    
    def draw_tree(self):
        """Draw the binary tree"""
        self.canvas.delete("all")
        
        if self.tree_root is None:
            return
        
        # Calculate positions
        self.node_positions = {}
        canvas_width = 800 # Base width
        start_x = canvas_width // 2
        start_y = 50
        initial_spacing = 200
        
        self.calculate_positions(self.tree_root, start_x, start_y, 0, initial_spacing)
        
        # Draw edges first
        self.draw_edges(self.tree_root)
        
        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            self.draw_node(node, x, y, self.node_color)
            
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def draw_edges(self, node):
        """Draw edges between nodes"""
        if node is None:
            return
        
        x1, y1 = self.node_positions[node]
        # Apply zoom
        x1 *= self.zoom_scale
        y1 *= self.zoom_scale
        
        if node.left:
            x2, y2 = self.node_positions[node.left]
            x2 *= self.zoom_scale
            y2 *= self.zoom_scale
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=self.edge_color,
                width=2 * self.zoom_scale,
                tags="edge"
            )
            self.draw_edges(node.left)
        
        if node.right:
            x2, y2 = self.node_positions[node.right]
            x2 *= self.zoom_scale
            y2 *= self.zoom_scale
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=self.edge_color,
                width=2 * self.zoom_scale,
                tags="edge"
            )
            self.draw_edges(node.right)
    
    def draw_node(self, node, x, y, color):
        """Draw a single node"""
        # Apply zoom
        x *= self.zoom_scale
        y *= self.zoom_scale
        radius = 25 * self.zoom_scale
        
        # Circle
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline="#ffffff",
            width=3 * self.zoom_scale,
            tags=f"node_{id(node)}"
        )
        
        # Value
        self.canvas.create_text(
            x, y,
            text=str(node.value),
            font=("Arial", int(16*self.zoom_scale), "bold"),
            fill="#ffffff",
            tags=f"node_{id(node)}"
        )
    
    def highlight_node(self, node, color):
        """Highlight a specific node"""
        if node in self.node_positions:
            x, y = self.node_positions[node]
            self.canvas.delete(f"node_{id(node)}")
            self.draw_node(node, x, y, color)

    def zoom_in(self):
        self.zoom_scale *= 1.1
        self.draw_tree()

    def zoom_out(self):
        self.zoom_scale /= 1.1
        self.draw_tree()
    
    # Traversal Algorithms
    def preorder_helper(self, node, result):
        """Pre-order: Root -> Left -> Right"""
        if node:
            result.append(node)
            self.preorder_helper(node.left, result)
            self.preorder_helper(node.right, result)
    
    def inorder_helper(self, node, result):
        """In-order: Left -> Root -> Right"""
        if node:
            self.inorder_helper(node.left, result)
            result.append(node)
            self.inorder_helper(node.right, result)
    
    def postorder_helper(self, node, result):
        """Post-order: Left -> Right -> Root"""
        if node:
            self.postorder_helper(node.left, result)
            self.postorder_helper(node.right, result)
            result.append(node)
    
    def levelorder_helper(self, root):
        """Level-order: Breadth-first traversal"""
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def preorder_traversal(self):
        """Start pre-order traversal animation"""
        if self.is_animating:
            return
        
        self.reset_visualization()
        self.current_traversal = []
        self.preorder_helper(self.tree_root, self.current_traversal)
        
        self.output_text.insert(tk.END, "Pre-order Traversal (Root → Left → Right)\n", "header")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.animate_traversal(0, "Pre-order")
    
    def inorder_traversal(self):
        """Start in-order traversal animation"""
        if self.is_animating:
            return
        
        self.reset_visualization()
        self.current_traversal = []
        self.inorder_helper(self.tree_root, self.current_traversal)
        
        self.output_text.insert(tk.END, "In-order Traversal (Left → Root → Right)\n", "header")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.animate_traversal(0, "In-order")
    
    def postorder_traversal(self):
        """Start post-order traversal animation"""
        if self.is_animating:
            return
        
        self.reset_visualization()
        self.current_traversal = []
        self.postorder_helper(self.tree_root, self.current_traversal)
        
        self.output_text.insert(tk.END, "Post-order Traversal (Left → Right → Root)\n", "header")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.animate_traversal(0, "Post-order")
    
    def levelorder_traversal(self):
        """Start level-order traversal animation"""
        if self.is_animating:
            return
        
        self.reset_visualization()
        self.current_traversal = self.levelorder_helper(self.tree_root)
        
        self.output_text.insert(tk.END, "Level-order Traversal (Breadth-First)\n", "header")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.animate_traversal(0, "Level-order")
    
    def animate_traversal(self, index, traversal_name):
        """Animate the traversal step by step"""
        if index >= len(self.current_traversal):
            self.is_animating = False
            self.output_text.insert(tk.END, f"\n✅ {traversal_name} traversal complete!\n")
            
            # Show final sequence
            sequence = " → ".join([str(node.value) for node in self.current_traversal])
            self.output_text.insert(tk.END, f"\nFinal Sequence: {sequence}\n")
            return
        
        self.is_animating = True
        node = self.current_traversal[index]
        
        # Highlight current node
        self.highlight_node(node, self.current_color)
        
        # Add to output
        self.output_text.insert(tk.END, f"Step {index + 1}: Visit node {node.value}\n")
        self.output_text.see(tk.END)
        
        # Schedule next step
        delay = self.speed_scale.get()
        
        def next_step():
            # Mark as visited
            self.highlight_node(node, self.visited_color)
            self.animate_traversal(index + 1, traversal_name)
        
        self.root.after(delay, next_step)
    
    def reset_visualization(self):
        """Reset the visualization"""
        self.is_animating = False
        self.current_traversal = []
        self.output_text.delete(1.0, tk.END)
        self.draw_tree()


def main():
    root = tk.Tk()
    app = TreeTraversals(root)
    root.mainloop()


if __name__ == "__main__":
    main()
