
"""
main.py
Entry point for the assignment.

This template includes standard imports (numpy, matplotlib)
so you can begin coding immediately.
"""

import numpy as np
import matplotlib.pyplot as plt


def problem_1():
    print("Program started.")
    # TODO: Add your assignment logic here

    # Example placeholder using numpy
    example_array = np.array([1, 2, 3])
    print("Example numpy array:", example_array)

    # Example placeholder using matplotlib
    # plt.plot(example_array)
    # plt.show()


if __name__ == "__problem_1__":
    problem_1()

    
# ===================================================================
# Integrating Fibonacci Heaps into Dijkstra's Algorithm (PSEUDOCODE)
# ===================================================================

"""
function DIJKSTRA_FIB_HEAP(G, s):

    # G[u] is adjacency list of u: list of (v, weight) pairs
    for each vertex v in G:
        d[v] = infinity     # Initialize all distances to infinity
    d[s] = 0

    # Step 1: Create a Fibonacci Heap and insert all vertices
    Q = MAKE_FIB_HEAP()
    for each vertex v in G:
        fibNode[v] = FIB_HEAP_INSERT(Q, v, d[v])

    # Step 2: Process vertices in order of shortest distance
    while (Q is not empty):
        uNode = FIB_HEAP_EXTRACT_MIN(Q)     # Extract vertex with min distance
        u = uNode.vertex

        # Step 3: Relaxation for each neighbor v of u
        for (v, weight) in G[u]:
            if d[u] + weight < d[v]:    # Found a shorter path
                d[v] = d[u] + weight
                FIB_HEAP_DECREASE_KEY(Q, fibNode[v], d[v])  # Update priority

    return d    # Final shortest distances

    """

