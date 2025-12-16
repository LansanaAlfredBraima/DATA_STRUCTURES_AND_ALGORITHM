"""
Prim's Algorithm Implementation
Author: DSA Project
Description: Finds the Minimum Spanning Tree (MST) for the provided graphs.
"""

import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.nodes = list(vertices)
        # Adjacency matrix for printing (optional)
        self.matrix = [[0 if i == j else float('inf') for j in range(len(vertices))] 
                       for i in range(len(vertices))]
        self.node_map = {node: i for i, node in enumerate(self.nodes)}
        self.index_map = {i: node for i, node in enumerate(self.nodes)}
        
        # Adjacency list for Prim's: { node: [(weight, neighbor), ...] }
        self.adj = {node: [] for node in vertices}

    def add_edge(self, u, v, weight):
        # Update Adjacency Matrix
        i, j = self.node_map[u], self.node_map[v]
        self.matrix[i][j] = weight
        self.matrix[j][i] = weight
        
        # Update Adjacency List
        self.adj[u].append((weight, v))
        self.adj[v].append((weight, u))

    def prim_mst(self):
        # Resulting MST edges
        mst_edges = []
        total_weight = 0
        
        # Priority Queue: (weight, current_node, parent_node)
        # Start from the first node in the list
        start_node = self.nodes[0]
        pq = [(0, start_node, None)]
        
        visited = set()
        
        print(f"\nRunning Prim's Algorithm starting from '{start_node}'...")
        print(f"{'Step':<5} {'Edge Added':<15} {'Weight':<10} {'Total Cost'}")
        print("-" * 50)
        
        step = 0
        while pq:
            weight, current_node, parent = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if parent is not None:
                mst_edges.append((parent, current_node, weight))
                total_weight += weight
                step += 1
                print(f"{step:<5} {parent}-{current_node:<15} {weight:<10} {total_weight}")
            
            for edge_weight, neighbor in self.adj[current_node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_weight, neighbor, current_node))
                    
        return mst_edges, total_weight

def main():
    # --- FIGURE 1 ---
    print("="*60)
    print("FIGURE 1: Minimum Spanning Tree")
    print("="*60)
    nodes_fig1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    g1 = Graph(nodes_fig1)
    
    # Edges from Figure 1
    edges_fig1 = [
        ('A','D',4), ('B','D',8), ('B','C',2),
        ('C','E',5), ('C','J',10),
        ('D','F',6), ('D','G',3), ('D','K',6), ('D','H',9),
        ('E','H',4), ('E','I',9), ('E','J',2),
        ('F','G',1), ('F','K',7),
        ('G','K',4),
        ('H','I',3), ('H','K',6),
        ('I','J',7), ('J','L',1)
    ]
    for u, v, w in edges_fig1:
        g1.add_edge(u, v, w)

    mst_1, cost_1 = g1.prim_mst()
    print(f"\nFigure 1 MST Total Cost: {cost_1}")
    print("MST Edges:", [(u,v) for u,v,w in mst_1])
    

    # --- FIGURE 2 ---
    print("\n\n" + "="*60)
    print("FIGURE 2: Minimum Spanning Tree")
    print("="*60)
    nodes_fig2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    g2 = Graph(nodes_fig2)
    
    # Edges from Figure 2
    edges_fig2 = [
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
    for u, v, w in edges_fig2:
        g2.add_edge(u, v, w)

    mst_2, cost_2 = g2.prim_mst()
    print(f"\nFigure 2 MST Total Cost: {cost_2}")
    print("MST Edges:", [(u,v) for u,v,w in mst_2])

if __name__ == "__main__":
    main()
