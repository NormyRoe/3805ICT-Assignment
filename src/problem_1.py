###############################################################################################
# Imports
#
###############################################################################################
import math
import time
import tracemalloc


###############################################################################################
# Class: Intersection
# Description:
# Represents a single intersection node in the road network.
# Stores the intersection name, outgoing roads, and metadata used by Dijkstra's Algorithm.
###############################################################################################
class Intersection:
    def __init__(self, name):
        """
        Create a new Intersection object.

        Parameters:
            name (str):
                The name of the intersection.

        Attributes:
            name (str):
                The intersection's name.
            distance (float):
                The shortest known distance from the start node (used by Dijkstra).
            parent (Intersection or None):
                The previous intersection on the shortest path.
            neighbors (dict):
                A dictionary mapping neighbor intersection names to road distances.
        """

        self.name = name

        # Variables needed for Dijkstra:
        self.distance = math.inf
        self.parent = None

        # Adjacency list: neighbor_name -> weight
        self.neighbors = {}



###############################################################################################
# Class: RoadNetwork
# Description:
# Represents the entire directed road network as a graph.
# Stores intersections and provides methods to add nodes and roads.
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
        """
        Add a new intersection to the road network.

        Parameters:
            name (str):
                The name of the intersection to add.

        Side Effects:
            Creates and stores a new Intersection object unless the name already exists.
        """

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
        """
        Add a directed road between two intersections.

        Parameters:
            source (str):
                The name of the intersection the road starts from.
            target (str):
                The name of the intersection the road leads to.
            distance (int or float):
                The length of the road.

        Side Effects:
            Updates the adjacency list of the source intersection.
        """

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
    # Prints all intersections and their outgoing roads.
    ###############################################################################################
    def draw_network(self):
        """
        Print all intersections and their outgoing roads.

        This function outputs a readable adjacency list showing:
        - Each intersection
        - Each directed road originating from it
        - The distance associated with each road
        """
        
        print("\nRoad Network:")
        print("-------------")

        for name, intersection in self.intersections.items():

            print(f"{name}:")

            if len(intersection.neighbors) == 0:
                print("  (no outgoing roads)")
            else:
                for target, distance in intersection.neighbors.items():
                    print(f"  -> {target} (distance {distance})")

        print("-------------\n")




###############################################################################################
# Class: PriorityQueue
# Description:
# A simple priority queue used by Dijkstra's Algorithm.
# Stores intersections sorted by their current shortest known distance.
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
        """
        Add an intersection node to the priority queue.

        The queue is sorted by each node's `distance` attribute so that
        the node with the smallest distance is always processed first.
        """

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
        """
        Check whether the priority queue is empty.

        Returns:
            bool: True if the queue contains no nodes, otherwise False.
        """

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
        """
        Remove and return the intersection with the smallest known distance.

        Returns:
            Intersection:
                The next intersection to process in Dijkstra's Algorithm.
        """

        # Return the first node
        return self.queue_p.pop(0)


###############################################################################################
# Class: HeapNode
# Description:
# Represents a single node in a Fibonacci Heap.
# Stores the key (distance), the associated intersection, and structural links
# used by Fibonacci Heap operations such as insert, extract-min, and decrease-key.
#
###############################################################################################    
class HeapNode():
    def __init__(self, key, value):
        """
        Create a new Fibonacci Heap node.

        Parameters:
            key (float or int):
                The priority value for this node (used as the heap key).
            value (Intersection):
                The intersection object associated with this heap node.

        Attributes:
            key (float or int):
                The node's priority value (distance in Dijkstra's Algorithm).
            value (Intersection):
                The intersection stored in this heap node.
            parent (HeapNode or None):
                The node's parent in the heap tree.
            child (HeapNode or None):
                The node's first child in the heap tree.
            left (HeapNode):
                The node's left sibling in the circular doubly-linked list.
            right (HeapNode):
                The node's right sibling in the circular doubly-linked list.
            degree (int):
                The number of children this node has.
            mark (bool):
                Indicates whether the node has lost a child since becoming a child itself.
        """

        self.key = key          # Distance
        self.value = value       # Intersection object
        self.parent = None
        self.child = None
        self.degree = 0
        self.left = self
        self.right = self
        self.mark = False


###############################################################################################
# Class: FibonacciHeap
# Description:
# Creates a Fibonacci Heap.
# Stores each provided HeapNode object and ensures that the heap maintains balance and integrity
#
###############################################################################################    
class FibonacciHeap():
    def __init__(self):
        """
        Create a new Fibonacci Heap node.

        Attributes:
            min_node:
                A pointer to the smallest node in the heap.
            total_nodes:
                A count of all nodes currently in the heap
        """

        self.min_node = None
        self.total_nodes = 0

    def is_empty(self):

        # Return if the heap is empty
        return self.min_node is None

    def insert(self, node):
        pass

    def extract_min(self):
        pass

    def decrease_key(self, node, new_key):
        pass

    def _merge_with_root_list(self, node):
        pass

    def _remove_from_root_list(self, node):
        pass

    def _link(self, node1, node2):
        pass

    def _consolidate(self):
        pass

    def _cut(self, node, parent):
        pass

    def _cascading_cut(self, node):
        pass


###############################################################################################
# Function: dijkstra
# Description:
# Runs Dijkstra's Algorithm using the Priority Queue
#
# Input:    RoadNetwork     The road network being searched
#           String          The name of the starting intersection
# Output:   N/A
###############################################################################################
def dijkstra(network, start_name):
    """
    Compute the shortest paths from a starting intersection using Dijkstra's Algorithm.

    This function updates each Intersection object in the provided RoadNetwork by:
    - Setting its `distance` attribute to the shortest known distance from the start node.
    - Setting its `parent` attribute to the previous node on the shortest path.

    Parameters:
        network (RoadNetwork):
            The road network containing all intersections and directed roads.
        start_name (str):
            The name of the intersection from which shortest paths will be calculated.

    Algorithm Overview:
        1. All intersections are reset (distance = infinity, parent = None).
        2. The starting intersection is assigned distance = 0 and added to a priority queue.
        3. The queue repeatedly selects the intersection with the smallest known distance.
        4. Each outgoing road is "relaxed":
            - If a shorter path to a neighbour is found, update its distance and parent.
            - The neighbour is re-added to the priority queue for further processing.
        5. When the queue is empty, all reachable intersections contain their final shortest
           distances and parent pointers.

    Side Effects:
        Modifies the `distance` and `parent` attributes of Intersection objects inside `network`.

    Returns:
        None
        (Results are stored directly in the network's Intersection objects.)


    """
    # Create a Dijkstra's queue
    dijkstra_queue = PriorityQueue()

    # Ensure that all intersections start off with fresh settings    
    for intersection in network.intersections.values():

        # Set distance to infinity
        intersection.distance = math.inf

        # Set parent to None
        intersection.parent = None

    # Retrieve the starting intersection
    start_node = network.intersections[start_name]

    # Initialise the distance for the starting intersection to zero
    start_node.distance = 0

    # Add the starting intersection to the queue
    dijkstra_queue.add_node(start_node)

    # While the queue isn't empty
    while not dijkstra_queue.empty():

        # Pop the first intersection node from the queue
        current_node = dijkstra_queue.remove_node()
        
        # For each neighbour of the intersection node
        for neighbor_name, weight in current_node.neighbors.items():

            # Retrieve the neighbor intersection object
            neighbor = network.intersections[neighbor_name]

            # Calculate the new distance for the neighbor intersection
            new_distance = current_node.distance + weight

            # Check if the new distance is less the the neighbor's existing distance
            if new_distance < neighbor.distance:

                # Update the neighbor's distance
                neighbor.distance = new_distance

                # Update the neighbor's parent
                neighbor.parent = current_node

                # Add the neighbor to the queue for processing
                dijkstra_queue.add_node(neighbor)

###############################################################################################
# Function: reconstruct_path
# Description:
# Reconstruct the shortest path to the given intersection using parent pointers
#
# Input:    Intersection     The destination intersection
# Output:   List             The path from the start to the destination
###############################################################################################
def reconstruct_path(intersection):
    """
    Reconstruct the shortest path to the given intersection.

    This function follows the `parent` pointers assigned by Dijkstra's Algorithm
    to build the path from the start node to the destination.

    Parameters:
        intersection (Intersection):
            The destination intersection.

    Returns:
        list[str]:
            A list of intersection names representing the shortest path.
    """

    # Create an empty path list
    path = []

    # Initialise a current intersection variable to the provided intersection
    current = intersection

    # Walk backwards through parent pointers
    # While current is not set to None
    while current is not None:

        # Add the intersection to the path list
        path.append(current.name)

        # Set current as being the current intersection's parent
        current = current.parent

    # Reverse to get start → destination order
    path.reverse()

    # Return the path list
    return path


###############################################################################################
# Function: print_distances
# Description:
# Output the Road Network's distances and reconstructed paths
# after Dijkstra's Algorithm was run on it
#
# Input:    RoadNetwork     The road network that was searched
#           String          The name of the starting intersection
# Output:   N/A
###############################################################################################
def print_distances(network, start_name):
    """
    Print the shortest distances and reconstructed paths from the starting intersection.

    Parameters:
        network (RoadNetwork):
            The road network containing all intersections.
        start_name (str):
            The name of the intersection from which Dijkstra's Algorithm was run.

    Output:
        Prints each intersection's shortest distance and the full path taken to reach it.
    """

    # Print Message
    print(f'Below are the shortest distances and paths from {start_name} to each intersection:\n')

    # Loop through the Road Network's intersections
    for intersection in network.intersections.values():

        # Print the name and distance values for the intersection
        print(f'{intersection.name}: {intersection.distance}')

        # Reconstruct the path
        path = reconstruct_path(intersection)

        # Print the path
        print(f'Path {" -> ".join(path)}\n')


###############################################################################################
# Function: run_algorithm
# Description:
# Runs Dijkstra's Algorithm on the provided Road Network using a Priority Queue.
# Measures execution time and peak memory usage, then prints the algorithm results.
#
# Input:    RoadNetwork     The road network that is to be searched
#           String          The name of the starting intersection
# Output:   N/A
###############################################################################################
def run_algorithm(network, start_name):
    """
    Execute Dijkstra's Algorithm using a Priority Queue and report performance metrics.

    This function performs the following steps:
    - Starts a high-precision timer.
    - Begins memory allocation tracing.
    - Runs Dijkstra's Algorithm from the specified starting intersection.
    - Captures the total execution time in milliseconds.
    - Captures the peak memory usage during the algorithm.
    - Prints the timing and memory results.
    - Prints the shortest distances and reconstructed paths for all intersections.

    Parameters:
        network (RoadNetwork):
            The road network containing all intersections and directed roads.
        start_name (str):
            The name of the intersection from which Dijkstra's Algorithm will begin.

    Output:
        Prints:
            - Total execution time (ms)
            - Peak memory usage (bytes)
            - Shortest distances to each intersection
            - Reconstructed shortest paths
    """

    # Start a timer
    start_time = time.perf_counter()
    
    # Start memory allocation tracing
    tracemalloc.start()

    # Run Dijstra's Algorithm using a Priority Queue
    dijkstra(network, start_name)

    # End the timer
    end_time = time.perf_counter()
    
    # Get the current and peak memory allocation
    queue_memory_current, queue_memory_peak = tracemalloc.get_traced_memory()
    
    # Stop memory allocation tracing
    tracemalloc.stop()

    # Calculate the length of time it took in milliseconds
    queue_total_time = (end_time - start_time) * 1000

    # Print the Algorithm's stats
    print(f'Dijkstra with Queue time: {queue_total_time:.4f} ms')
    print(f'Dijkstra with Queue memory: {queue_memory_peak} bytes')

    # Print the Algorithm's distances
    print_distances(network, start_name)


###############################################################################################
# Function: problem_1
# Description:
# Entry Point for running Problem 1
# Builds the road network, displays its structure, and runs Dijkstra's Algorithm.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_1():
    """
    Entry point for Problem 1.

    This function:
    - Creates the road network
    - Adds all intersections
    - Adds all directed roads
    - Prints the network structure
    - Runs Dijkstra's Algorithm using a Priority Queue
    - Prints shortest distances and reconstructed paths
    - Prints timing and memory usage statistics

    It serves as the main driver for testing the Problem 1 implementation.
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
    network.add_road("Hercules Avenue", "Charmed Drive", 5)
    network.add_road("Hercules Avenue", "Supernatural Circuit", 15)

    # Draw Network
    network.draw_network()

    # Run Dijkstra's Algorithm
    run_algorithm(network, "Buffy Avenue")


if __name__ == "__main__":
    problem_1()


