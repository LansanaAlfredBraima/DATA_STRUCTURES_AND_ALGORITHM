"""
DSA Project Launcher
Author: DSA Project
Description: Main launcher for Data Structures and Algorithms Project
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class ProjectLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DSA Project - Interactive Solutions")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a2e")
        header_frame.pack(pady=40)
        
        tk.Label(
            header_frame,
            text="Data Structures & Algorithms",
            font=("Arial", 32, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        ).pack()
        
        tk.Label(
            header_frame,
            text="Project Assignment - Interactive Solutions",
            font=("Arial", 16),
            bg="#1a1a2e",
            fg="#a0a0a0"
        ).pack(pady=10)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=20, expand=True)
        
        # Problem Buttons
        problems = [
            ("Problem 1: Tower of Hanoi", "tower_of_hanoi.py", "#FF6B6B"),
            ("Problem 2: Tree Traversals", "tree_traversals.py", "#4ECDC4"),
            ("Problem 3: Huffman Coding", "huffman_coding.py", "#FFE66D"),
            ("Problem 4: Dijkstra's Algorithm", "dijkstra_algorithm.py", "#A55EEA")
        ]
        
        for text, script, color in problems:
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="#1a1a2e",
                width=30,
                pady=15,
                cursor="hand2",
                relief=tk.FLAT,
                command=lambda s=script: self.launch_script(s)
            )
            btn.pack(pady=10)
            
        # Footer
        footer_frame = tk.Frame(self.root, bg="#1a1a2e")
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        
        tk.Label(
            footer_frame,
            text="Developed with Python & Tkinter",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#535c68"
        ).pack()

    def launch_script(self, script_name):
        """Launch the selected script"""
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_dir, script_name)
            
            # Launch as separate process
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch {script_name}\n{str(e)}")

def main():
    root = tk.Tk()
    app = ProjectLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
