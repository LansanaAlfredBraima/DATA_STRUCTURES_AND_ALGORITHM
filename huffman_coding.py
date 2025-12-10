"""
Huffman Coding - Visual Implementation
Author: DSA Project
Description: Interactive visualization of Huffman Coding algorithm with tree construction and encoding generation
"""

import tkinter as tk
from tkinter import ttk
import heapq
import collections

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding - Visual Implementation")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")
        
        # Algorithm variables
        self.nodes = []
        self.huffman_tree = None
        self.codes = {}
        self.node_positions = {}
        self.animation_step = 0
        self.steps = []
        self.is_animating = False
        self.zoom_scale = 1.0
        
        # Colors
        self.colors = {
            'bg': "#1e1e2e",
            'node': "#f38ba8",
            'leaf': "#a6e3a1",
            'edge': "#cdd6f4",
            'text': "#cdd6f4",
            'highlight': "#f9e2af"
        }
        
        self.setup_ui()
        self.reset_default()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🗜️ Huffman Coding",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg="#89b4fa"
        )
        title_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Controls and Input
        left_frame = tk.Frame(content_frame, bg=self.colors['bg'], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Input area
        input_group = tk.LabelFrame(
            left_frame, 
            text="Symbol Frequencies", 
            font=("Arial", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            padx=5, pady=5
        )
        input_group.pack(fill=tk.X, pady=5)
        
        tk.Label(
            input_group,
            text="Format: char:freq (comma separated)",
            bg=self.colors['bg'],
            fg="#a6adc8",
            font=("Arial", 9),
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        self.input_entry = tk.Entry(
            input_group,
            font=("Courier", 11),
            bg="#313244",
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.insert(0, "a:2, b:4, c:8, d:16, e:16")
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.build_btn = tk.Button(
            btn_frame,
            text="🔨 Build Tree",
            font=("Arial", 11, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            command=self.start_build,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.build_btn.pack(fill=tk.X, pady=2)
        
        self.reset_btn = tk.Button(
            btn_frame,
            text="🔄 Reset",
            font=("Arial", 11, "bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            command=self.reset_default,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.reset_btn.pack(fill=tk.X, pady=2)
        
        # Zoom Controls
        zoom_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        zoom_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            zoom_frame,
            text="🔍+",
            font=("Arial", 12, "bold"),
            bg="#fab387",
            fg="#1e1e2e",
            command=self.zoom_in,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        tk.Button(
            zoom_frame,
            text="🔍-",
            font=("Arial", 12, "bold"),
            bg="#fab387",
            fg="#1e1e2e",
            command=self.zoom_out,
            cursor="hand2",
            relief=tk.FLAT,
            width=5
        ).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Encoding Table
        table_group = tk.LabelFrame(
            left_frame,
            text="Encoding Table",
            font=("Arial", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            padx=5, pady=5
        )
        table_group.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for codes
        columns = ('char', 'freq', 'code', 'bits')
        self.tree_view = ttk.Treeview(
            table_group, 
            columns=columns, 
            show='headings',
            height=8
        )
        
        self.tree_view.heading('char', text='Sym')
        self.tree_view.heading('freq', text='Freq')
        self.tree_view.heading('code', text='Code')
        self.tree_view.heading('bits', text='Bits')
        
        self.tree_view.column('char', width=40, anchor='center')
        self.tree_view.column('freq', width=40, anchor='center')
        self.tree_view.column('code', width=80, anchor='center')
        self.tree_view.column('bits', width=40, anchor='center')
        
        self.tree_view.pack(fill=tk.BOTH, expand=True)
        
        # Stats
        self.stats_label = tk.Label(
            left_frame,
            text="Waiting to build...",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg="#a6e3a1",
            justify=tk.LEFT
        )
        self.stats_label.pack(fill=tk.X, pady=5)
        
        # Right side - Visualization
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(
            right_frame,
            bg="#181825",
            highlightthickness=0
        )
        
        h_scroll = tk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_shift_mousewheel(event):
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)
        
        # Step info
        self.step_label = tk.Label(
            right_frame,
            text="Ready",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg="#f9e2af"
        )
        self.step_label.pack(pady=5)

    def parse_input(self):
        """Parse input string into frequency map"""
        try:
            text = self.input_entry.get()
            pairs = [p.strip() for p in text.split(',')]
            freq_map = {}
            for p in pairs:
                char, freq = p.split(':')
                freq_map[char.strip()] = int(freq.strip())
            return freq_map
        except Exception as e:
            self.step_label.config(text=f"Error: Invalid input format", fg="#f38ba8")
            return None

    def build_huffman_tree(self, freq_map):
        """Build Huffman tree and record steps"""
        heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
        heapq.heapify(heap)
        
        steps = []
        # Initial state
        steps.append({
            'nodes': [n for n in heap],
            'msg': "Initial priority queue of nodes"
        })
        
        while len(heap) > 1:
            # Get two smallest nodes
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # Create internal node
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
            
            # Record step
            steps.append({
                'nodes': [n for n in heap],
                'msg': f"Merged nodes with freq {left.freq} and {right.freq} into new node {merged.freq}"
            })
            
        return heap[0], steps

    def generate_codes(self, node, code=""):
        """Generate Huffman codes recursively"""
        if node is None:
            return
            
        if node.char is not None:
            self.codes[node.char] = code
            return
            
        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")

    def calculate_positions(self, node, x, y, level, width):
        """Calculate tree node positions"""
        if node is None:
            return
            
        self.node_positions[node] = (x, y)
        
        if node.left or node.right:
            dx = width / (2 ** (level + 2))
            self.calculate_positions(node.left, x - dx, y + 80, level + 1, width)
            self.calculate_positions(node.right, x + dx, y + 80, level + 1, width)

    def draw_tree(self, nodes_to_draw):
        """Draw the current state of the forest/tree"""
        self.canvas.delete("all")
        self.node_positions = {}
        
        # Calculate positions for forest
        canvas_width = self.canvas.winfo_width()
        # Adjust section width based on zoom, but keep relative layout logic
        # Ideally, we want the whole drawing to scale.
        # Let's calculate base positions then scale them.
        
        section_width = (canvas_width / len(nodes_to_draw)) 
        
        for i, node in enumerate(nodes_to_draw):
            x = (i * section_width) + (section_width / 2)
            self.calculate_positions(node, x, 50, 0, section_width * 2)
            
        # Draw edges
        for node in self.node_positions:
            x, y = self.node_positions[node]
            # Apply zoom
            x *= self.zoom_scale
            y *= self.zoom_scale
            
            if node.left:
                lx, ly = self.node_positions[node.left]
                lx *= self.zoom_scale
                ly *= self.zoom_scale
                
                self.canvas.create_line(x, y, lx, ly, fill=self.colors['edge'], width=2 * self.zoom_scale)
                # Label 0
                self.canvas.create_text((x+lx)/2 - 10*self.zoom_scale, (y+ly)/2, text="0", fill="#fab387", font=("Arial", int(10*self.zoom_scale), "bold"))
                
            if node.right:
                rx, ry = self.node_positions[node.right]
                rx *= self.zoom_scale
                ry *= self.zoom_scale
                
                self.canvas.create_line(x, y, rx, ry, fill=self.colors['edge'], width=2 * self.zoom_scale)
                # Label 1
                self.canvas.create_text((x+rx)/2 + 10*self.zoom_scale, (y+ry)/2, text="1", fill="#fab387", font=("Arial", int(10*self.zoom_scale), "bold"))

        # Draw nodes
        for node, (bx, by) in self.node_positions.items():
            x = bx * self.zoom_scale
            y = by * self.zoom_scale
            
            color = self.colors['leaf'] if node.char else self.colors['node']
            text = f"{node.char}:{node.freq}" if node.char else str(node.freq)
            
            # Node circle
            r = 25 * self.zoom_scale
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=self.colors['text'])
            self.canvas.create_text(x, y, text=text, fill="#1e1e2e", font=("Arial", int(10*self.zoom_scale), "bold"))
            
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        self.zoom_scale *= 1.1
        if self.animation_step > 0 and self.steps:
             # Redraw current step
             step = self.steps[self.animation_step - 1]
             self.draw_tree(step['nodes'])
        elif self.huffman_tree:
             self.draw_tree([self.huffman_tree])

    def zoom_out(self):
        self.zoom_scale /= 1.1
        if self.animation_step > 0 and self.steps:
             step = self.steps[self.animation_step - 1]
             self.draw_tree(step['nodes'])
        elif self.huffman_tree:
             self.draw_tree([self.huffman_tree])

    def animate_step(self):
        """Animate one step of construction"""
        if self.animation_step < len(self.steps):
            step = self.steps[self.animation_step]
            self.draw_tree(step['nodes'])
            self.step_label.config(text=step['msg'])
            self.animation_step += 1
            self.root.after(1500, self.animate_step)
        else:
            self.is_animating = False
            self.step_label.config(text="Huffman Tree Construction Complete!", fg="#a6e3a1")
            self.update_table()

    def update_table(self):
        """Update the encoding table and stats"""
        # Clear table
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
            
        # Generate codes
        self.codes = {}
        self.generate_codes(self.huffman_tree)
        
        # Calculate stats
        total_bits = 0
        original_bits = 0
        
        for char, code in sorted(self.codes.items()):
            freq = 0
            # Find freq from input
            freq_map = self.parse_input()
            if freq_map:
                freq = freq_map[char]
                
            bits = len(code) * freq
            total_bits += bits
            original_bits += 8 * freq  # Assuming 8-bit ASCII
            
            self.tree_view.insert('', 'end', values=(char, freq, code, len(code)))
            
        # Update stats label
        compression = (1 - total_bits/original_bits) * 100 if original_bits > 0 else 0
        stats_text = (
            f"Original Size: {original_bits} bits\n"
            f"Compressed Size: {total_bits} bits\n"
            f"Compression Ratio: {compression:.1f}%"
        )
        self.stats_label.config(text=stats_text)

    def start_build(self):
        """Start the building process"""
        if self.is_animating:
            return
            
        freq_map = self.parse_input()
        if not freq_map:
            return
            
        self.huffman_tree, self.steps = self.build_huffman_tree(freq_map)
        self.animation_step = 0
        self.is_animating = True
        self.animate_step()

    def reset_default(self):
        """Reset to default state"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "a:2, b:4, c:8, d:16, e:16")
        self.canvas.delete("all")
        self.step_label.config(text="Ready")
        self.stats_label.config(text="Waiting to build...")
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        self.is_animating = False

def main():
    root = tk.Tk()
    app = HuffmanCoding(root)
    root.mainloop()

if __name__ == "__main__":
    main()
