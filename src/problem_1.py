###############################################################################################
# Imports
#
###############################################################################################
import math
import networkx as nx
import matplotlib.pyplot as plt


###############################################################################################
# Class: Intersection
# Description:
# Represents a single intersection node in the road network.
# Stores which other intersections can be reached from this intersection.
###############################################################################################
class Intersection:
    def __init__(self, name):
        self.name = name

        # Variables needed for Dijkstra:
        self.distance = math.inf
        self.parent = None

        # Adjacency list: neighbor_name -> weight
        self.neighbors = {}



###############################################################################################
# Class: RoadNetwork
# Description:
# Represents the entire road network (graph).
###############################################################################################
class RoadNetwork:
    def __init__(self):
        # Dictionary: name -> Intersection object
        self.intersections = {}


    ###############################################################################################
    # Function: add_intersection
    # Description:
    # Creates a new Intersection and adds it to the intersection dictionary
    #
    # Input:    name       The intersection's name
    # Output:   N/A
    ###############################################################################################
    def add_intersection(self, name):

        # Check that the intersection doesn't exist
        if name not in self.intersections:

            # Add to the intersections
            self.intersections[name] = Intersection(name)

        # else
        else:

            # Advise that it already exists
            print(f"Intersection {name} already exists.")


    ###############################################################################################
    # Function: add_road
    # Description:
    # Creates the connection between two intersections and details the distance for the road
    #
    # Input:    source       The intersection the road goes from
    #           target       The intersection the road goes to
    #           distance     The length of the road
    # Output:   N/A
    ###############################################################################################
    def add_road(self, source, target, distance):

        # Check that both intersections exist
        if source in self.intersections and target in self.intersections:

            # Add directed edge: source -> target
            self.intersections[source].neighbors[target] = distance

        # Else
        else:

            # Advise that the road cannot be added
            print(f"Invalid road: {source} and/or {target} do not exist.")


    ###############################################################################################
    # Function: draw_network
    # Description:
    # Draws the road network as a visual graph with nodes and weighted edges.
    ###############################################################################################
    def draw_network(self):
        
        G = nx.DiGraph()

        # Add nodes
        for name in self.intersections:
            G.add_node(name)

        # Add edges with weights
        for source, intersection in self.intersections.items():
            for target, distance in intersection.neighbors.items():
                G.add_edge(source, target, weight=distance)

        # Kamada-Kawai layout (best for road networks)
        pos = nx.kamada_kawai_layout(G)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightblue")

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10)

        # Draw edges
        nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

        # Draw edge labels (weights)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Road Network Graph")
        plt.axis("off")
        plt.show()




###############################################################################################
# Class: PriorityQueue
# Description:
# Creates a Priority Queue list object for the Dijkstra algorithm to use.
#
###############################################################################################

class PriorityQueue():
    def __init__(self):
        self.queue_p = []

    ###############################################################################################
    # Function: add_node
    # Description:
    # Add the provided node to the priority queue
    # Sorts the priority queue based on node.distance
    #
    # Input:    node       The node to add to the queue
    # Output:   N/A
    ###############################################################################################
    def add_node(self, node):
        self.queue_p.append(node)

        # Sort the queue by distance
        self.queue_p.sort(key=lambda n: n.distance)


    ###############################################################################################
    # Function: empty
    # Description:
    # Checks whether the queue is empty
    #
    # Input:    N/A
    # Output:   Bool    Whether the queue is empty
    ###############################################################################################
    def empty(self):

        return len(self.queue_p) == 0

    
    ###############################################################################################
    # Function: remove_node
    # Description:
    # Removes the first node in the queue.
    # Since the queue is sorted when nodes are added, the first node will have the smallest distance
    #
    # Input:    N/A
    # Output:   Node        The node that is first in the queue
    ###############################################################################################
    def remove_node(self):

        # Return the first node
        return self.queue_p.pop(0)




###############################################################################################
# Function: problem_1
# Description:
# Entry Point for running Problem 1
# Creates the road network and calls the appropriate algorithm functions.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_1():
    """
    problem_1.py
    Entry point for the assignment - Problem 1.


    """
    print("Program started...")

    # Create Road Network
    network = RoadNetwork()

    # Create intersections
    network.add_intersection("Buffy Avenue")
    network.add_intersection("Angel Road")
    network.add_intersection("Charmed Drive")
    network.add_intersection("Supernatural Circuit")
    network.add_intersection("Xena Road")
    network.add_intersection("Hercules Avenue")

    # Create directional roads
    network.add_road("Buffy Avenue", "Angel Road", 5)
    network.add_road("Buffy Avenue", "Supernatural Circuit", 10)
    network.add_road("Angel Road", "Charmed Drive", 5)
    network.add_road("Angel Road", "Xena Road", 10)
    network.add_road("Charmed Drive", "Hercules Avenue", 5)
    network.add_road("Charmed Drive", "Xena Road", 10)
    network.add_road("Supernatural Circuit", "Angel Road", 5)
    network.add_road("Supernatural Circuit", "Charmed Drive", 10)
    network.add_road("Xena Road", "Buffy Avenue", 5)
    network.add_road("Xena Road", "Hercules Avenue", 10)
    network.add_road("Hercules Avenue", "Angel Road", 5)
    network.add_road("Hercules Avenue", "Supernatural Circuit", 15)

    network.draw_network()

if __name__ == "__main__":
    problem_1()

    


###############################################################################################
# Class: HeapNode
# Description:
# Inherits from the Node class
# This is the class used for each Fibonacci Heap node.
#
#
###############################################################################################
    
#class HeapNode(Node):
#    def __init__(self, node):
#        self.node = node
#        self.parent = None
#        self.degree = 0
#        self.child = None
#        self.mark = False
#        self.left = self
#        self.right = self
