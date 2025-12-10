"""
Tower of Hanoi - Recursive Algorithm with GUI Visualization
Author: DSA Project
Description: Interactive visualization of the Tower of Hanoi puzzle with step-by-step animation
"""

import tkinter as tk
from tkinter import ttk
import time

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi - Recursive Visualization")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a2e")
        
        # Algorithm variables
        self.num_disks = 3
        self.moves = []
        self.move_count = 0
        self.is_animating = False
        self.animation_speed = 500  # milliseconds
        self.zoom_scale = 1.0
        
        # Tower state: list of lists, each inner list represents a peg
        self.towers = [[], [], []]
        
        # Colors for disks (gradient from blue to purple)
        self.disk_colors = [
            "#FF6B6B", "#FFA07A", "#FFD93D", "#6BCF7F", 
            "#4ECDC4", "#45B7D1", "#5F27CD", "#A55EEA"
        ]
        
        self.setup_ui()
        self.reset_puzzle()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🗼 Tower of Hanoi",
            font=("Arial", 32, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Recursive Algorithm Visualization",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#a0a0a0"
        )
        subtitle_label.pack()
        
        # Canvas for drawing towers
        # Canvas for drawing towers
        canvas_frame = tk.Frame(self.root, bg="#1a1a2e")
        canvas_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=1100,
            height=400,
            bg="#16213e",
            highlightthickness=0
        )
        
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = tk.Frame(self.root, bg="#1a1a2e")
        control_frame.pack(pady=10)
        
        # Number of disks
        tk.Label(
            control_frame,
            text="Number of Disks:",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="#ffffff"
        ).grid(row=0, column=0, padx=10)
        
        self.disk_spinbox = tk.Spinbox(
            control_frame,
            from_=1,
            to=8,
            width=5,
            font=("Arial", 12),
            command=self.reset_puzzle
        )
        self.disk_spinbox.delete(0, tk.END)
        self.disk_spinbox.insert(0, "3")
        self.disk_spinbox.grid(row=0, column=1, padx=10)
        
        # Speed control
        tk.Label(
            control_frame,
            text="Animation Speed:",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="#ffffff"
        ).grid(row=0, column=2, padx=10)
        
        self.speed_scale = tk.Scale(
            control_frame,
            from_=100,
            to=2000,
            orient=tk.HORIZONTAL,
            length=150,
            bg="#1a1a2e",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#16213e"
        )
        self.speed_scale.set(500)
        self.speed_scale.grid(row=0, column=3, padx=10)
        
        # Buttons (Moved to control frame to save space)
        self.solve_button = tk.Button(
            control_frame,
            text="🚀 Solve",
            font=("Arial", 12, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            padx=20,
            pady=5,
            command=self.solve_puzzle,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.solve_button.grid(row=0, column=4, padx=10)
        
        self.reset_button = tk.Button(
            control_frame,
            text="🔄 Reset",
            font=("Arial", 12, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            padx=20,
            pady=5,
            command=self.reset_puzzle,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.reset_button.grid(row=0, column=5, padx=10)
        
        # Zoom Controls
        tk.Label(
            control_frame,
            text="Zoom:",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="#ffffff"
        ).grid(row=0, column=6, padx=10)
        
        zoom_frame = tk.Frame(control_frame, bg="#1a1a2e")
        zoom_frame.grid(row=0, column=7, padx=5)
        
        tk.Button(
            zoom_frame,
            text="🔍+",
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            command=self.zoom_in,
            cursor="hand2",
            relief=tk.FLAT,
            width=3
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            zoom_frame,
            text="🔍-",
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#1a1a2e",
            command=self.zoom_out,
            cursor="hand2",
            relief=tk.FLAT,
            width=3
        ).pack(side=tk.LEFT, padx=2)
        
        # Info panel
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(pady=10)
        
        self.move_label = tk.Label(
            info_frame,
            text="Moves: 0",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#00ff88"
        )
        self.move_label.grid(row=0, column=0, padx=20)
        
        self.total_moves_label = tk.Label(
            info_frame,
            text="Total Moves Required: 7",
            font=("Arial", 16),
            bg="#1a1a2e",
            fg="#a0a0a0"
        )
        self.total_moves_label.grid(row=0, column=1, padx=20)
        
        # Move sequence display
        sequence_frame = tk.Frame(self.root, bg="#1a1a2e")
        sequence_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=50)
        
        tk.Label(
            sequence_frame,
            text="Move Sequence:",
            font=("Arial", 12, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(anchor=tk.W)
        
        self.sequence_text = tk.Text(
            sequence_frame,
            height=6,
            font=("Courier", 10),
            bg="#16213e",
            fg="#00ff88",
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.sequence_text.pack(fill=tk.BOTH, expand=True)
        
    def reset_puzzle(self):
        """Reset the puzzle to initial state"""
        if self.is_animating:
            return
            
        self.num_disks = int(self.disk_spinbox.get())
        self.towers = [list(range(self.num_disks, 0, -1)), [], []]
        self.moves = []
        self.move_count = 0
        
        # Update labels
        total_moves = (2 ** self.num_disks) - 1
        self.move_label.config(text="Moves: 0")
        self.total_moves_label.config(text=f"Total Moves Required: {total_moves}")
        
        # Clear sequence
        self.sequence_text.delete(1.0, tk.END)
        
        self.draw_towers()
        
    def draw_towers(self):
        """Draw the current state of towers"""
        self.canvas.delete("all")
        
        # Draw base
        base_x1, base_y1 = 50 * self.zoom_scale, 350 * self.zoom_scale
        base_x2, base_y2 = 1050 * self.zoom_scale, 370 * self.zoom_scale
        
        self.canvas.create_rectangle(
            base_x1, base_y1, base_x2, base_y2,
            fill="#0f3460",
            outline=""
        )
        
        # Peg positions
        peg_positions = [250, 550, 850]
        peg_names = ["Source (A)", "Auxiliary (B)", "Destination (C)"]
        
        # Draw pegs
        for i, (x, name) in enumerate(zip(peg_positions, peg_names)):
            # Apply zoom
            x *= self.zoom_scale
            
            # Peg pole
            pole_y1 = 150 * self.zoom_scale
            pole_y2 = 350 * self.zoom_scale
            pole_w = 10 * self.zoom_scale
            
            self.canvas.create_rectangle(
                x - pole_w, pole_y1, x + pole_w, pole_y2,
                fill="#e94560",
                outline=""
            )
            
            # Peg label
            label_y = 380 * self.zoom_scale
            self.canvas.create_text(
                x, label_y,
                text=name,
                font=("Arial", int(14*self.zoom_scale), "bold"),
                fill="#ffffff"
            )
            
            # Draw disks on this peg
            for j, disk_size in enumerate(self.towers[i]):
                disk_width = (40 + (disk_size * 25)) * self.zoom_scale
                disk_height = 25 * self.zoom_scale
                y = (350 * self.zoom_scale) - (j + 1) * disk_height
                
                # Disk with gradient effect (simulated with outline)
                color_idx = disk_size - 1
                self.canvas.create_rectangle(
                    x - disk_width // 2, y,
                    x + disk_width // 2, y + disk_height - (5 * self.zoom_scale),
                    fill=self.disk_colors[color_idx % len(self.disk_colors)],
                    outline="#ffffff",
                    width=2 * self.zoom_scale
                )
                
                # Disk number
                self.canvas.create_text(
                    x, y + disk_height // 2 - (2 * self.zoom_scale),
                    text=str(disk_size),
                    font=("Arial", int(12*self.zoom_scale), "bold"),
                    fill="#ffffff"
                )
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        self.zoom_scale *= 1.1
        self.draw_towers()

    def zoom_out(self):
        self.zoom_scale /= 1.1
        self.draw_towers()
    
    def tower_of_hanoi(self, n, source, destination, auxiliary):
        """Recursive Tower of Hanoi algorithm"""
        if n == 1:
            self.moves.append((source, destination))
            return
        
        self.tower_of_hanoi(n - 1, source, auxiliary, destination)
        self.moves.append((source, destination))
        self.tower_of_hanoi(n - 1, auxiliary, destination, source)
    
    def solve_puzzle(self):
        """Solve the puzzle and animate"""
        if self.is_animating:
            return
            
        self.is_animating = True
        self.solve_button.config(state=tk.DISABLED)
        self.disk_spinbox.config(state=tk.DISABLED)
        
        # Generate moves
        self.moves = []
        self.tower_of_hanoi(self.num_disks, 0, 2, 1)
        
        # Start animation
        self.animate_moves(0)
    
    def animate_moves(self, move_index):
        """Animate the moves one by one"""
        if move_index >= len(self.moves):
            # Animation complete
            self.is_animating = False
            self.solve_button.config(state=tk.NORMAL)
            self.disk_spinbox.config(state=tk.NORMAL)
            
            self.sequence_text.insert(tk.END, "\n✅ Puzzle Solved!\n", "success")
            return
        
        # Get current move
        source, destination = self.moves[move_index]
        
        # Move disk
        disk = self.towers[source].pop()
        self.towers[destination].append(disk)
        
        # Update display
        self.move_count += 1
        self.move_label.config(text=f"Moves: {self.move_count}")
        
        # Add to sequence
        peg_names = ['A', 'B', 'C']
        move_text = f"Move {self.move_count}: Disk {disk} from {peg_names[source]} to {peg_names[destination]}\n"
        self.sequence_text.insert(tk.END, move_text)
        self.sequence_text.see(tk.END)
        
        # Redraw
        self.draw_towers()
        
        # Schedule next move
        delay = self.speed_scale.get()
        self.root.after(delay, lambda: self.animate_moves(move_index + 1))


def main():
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()


if __name__ == "__main__":
    main()
