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

    ###############################################################################################
    # Function: is_empty
    # Description:
    # Checks whether the queue is empty
    #
    # Input:    N/A
    # Output:   Bool    Whether the heap is empty
    ###############################################################################################
    def is_empty(self):
        """
        Check whether the heap is empty.

        Returns:
            bool: True if the heap contains no nodes, otherwise False.
        """

        # Return if the heap is empty
        return self.min_node is None

    ###############################################################################################
    # Function: _merge_with_heap
    # Description:
    # Merges the provided HeapNode into the existing Fibonacci Heap
    #
    # Input:    HeapNode     The node to merge into the existing heap
    # Output:   N/A
    ###############################################################################################
    def _merge_with_heap(self, node):
        """
        Merge a new node into the existing Fibonacci Heap.

        Parameters:
            node (HeapNode):
                The node to merge into the existing heap.

        Side Effects:
            - Adds the node to the existing heap.
            - Updates the minimum node pointer if necessary.
        """

        # If the heap is empty
        if self.min_node is None:

            # Initialise the root list
            self.min_node = node
            node.left = node
            node.right = node

            # Then return
            return
    
        # Insert node to the right of the min_node
        node.left = self.min_node
        node.right = self.min_node.right

        # Update the min_node's pointers
        self.min_node.right.left = node
        self.min_node.right = node

        # Check if there is a new min_node in the heap
        if node.key < self.min_node.key:

            # Select the new min_node
            self.min_node = node


    ###############################################################################################
    # Function: insert
    # Description:
    # Inserts the provided HeapNode into the Fibonacci Heap
    #
    # Input:    HeapNode     The node to insert into the heap
    # Output:   N/A
    ###############################################################################################
    def insert(self, node):
        """
        Insert a new node into the Fibonacci Heap.

        Parameters:
            node (HeapNode):
                The node to insert into the heap.

        Side Effects:
            - Adds the node to the root list.
            - Updates the minimum node pointer if necessary.
            - Increments the total node count.
        """

        # Check if the heap is empty
        if self.is_empty():

            # Add the node to the root
            self.min_node = node

            # Increase counter
            self.total_nodes += 1

        # Else
        else:

            # Merge the node with the existing heap
            self._merge_with_heap(node)

            # Increase counter
            self.total_nodes += 1


    ###############################################################################################
    # Function: _link
    # Description:
    # Links child nodes to parent nodes
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def _link(self, child_node, parent_node):
        """
        Make child_node a child of parent_node.

        This operation:
        - Removes child_node from the root list
        - Inserts child_node into parent_node's child circular list
        - Increases parent_node's degree by 1
        - Resets child_node's mark
        - Does not modify ancestor degrees
        """

        # Remove child_node from root list
        child_node.left.right = child_node.right
        child_node.right.left = child_node.left

        # Set parent variable for child_node
        child_node.parent = parent_node

        # If parent_node has no children yet
        if parent_node.child is None:

            # Update the parent_node to have a child
            parent_node.child = child_node

            # Set the child node to point to itself
            child_node.left = child_node
            child_node.right = child_node

        # Else
        else:

            # Insert child_node into parent's child list
            child_node.left = parent_node.child
            child_node.right = parent_node.child.right

            # Update the parent's child node
            parent_node.child.right.left = child_node
            parent_node.child.right = child_node

        # Increase parent's degree
        parent_node.degree += 1

        # Reset child's mark
        child_node.mark = False


    ###############################################################################################
    # Function: _consolidate
    # Description:
    # Consolidates the Fibonacci Heap so that no two roots have the same degree
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def _consolidate(self):
        """
        Consolidate the root list so that no two roots have the same degree.

        This operation:
        - Gathers all current roots into a list
        - Repeatedly links trees of equal degree using _link()
        - Rebuilds the root list from the merged trees
        - Resets each root's pointers before reinsertion
        - Updates the heap's min_node automatically
        """

        # Dictionary: degree -> root node
        degree_dict = {}

        # Step 1: Gather all roots into a list

        # Create a roots list
        roots_list = []

        # Set the current_node as the min_node
        current_node = self.min_node

        # While true loop
        while True:

            # Add the current node to the roots_list
            roots_list.append(current_node)

            # Update the current_node to be the node on the right
            current_node = current_node.right

            # If current_node is the min_node
            if current_node == self.min_node:

                # Break out of while loop
                break

        # Step 2: Process each root
        for root in roots_list:

            # Set x_node as the tree that we are currently working with
            x_node = root

            # Set degree as the x_node's degree
            degree = x_node.degree

            # While x_node's degree already exists in degree_dict
            while degree in degree_dict:

                # Set that other node as y_node
                y_node = degree_dict[degree]

                # Check if y_node is the smaller root
                if y_node.key < x_node.key:

                    # Change which variables hold the nodes
                    # x_node is the parent and must have a smaller key
                    x_node, y_node = y_node, x_node

                # Link y_node under x_node
                self._link(y_node, x_node)

                # Remove the degree entry from the dictionary
                del degree_dict[degree]

                # After linking, x_node's degree has increased
                # Update degree variable
                degree = x_node.degree

            # Store x_node under its final degree
            degree_dict[degree] = x_node

        # Step 3: Rebuild the root list from the degree_dict

        # Set min_node to None
        self.min_node = None

        # For loop through degree_dict
        for node in degree_dict.values():

            # Reset the root node's left and right pointers to point to itself
            # This is necessary because the old root list is being discarded.
            # Each node must be reset before being reinserted into the new root list.
            node.left = node
            node.right = node
            node.parent = None

            # Merge the node back into the root list
            # This also updates min_node automatically
            self._merge_with_heap(node)



    ###############################################################################################
    # Function: extract_min
    # Description:
    # Extracts the min_node from the heap
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def extract_min(self):
        """
        Extract the minimum node from the Fibonacci Heap.

        This operation:
        - Promotes all children of the minimum node to the root list
        - Removes the minimum node from the root list
        - Consolidates the heap to merge trees of equal degree
        - Updates the heap's min_node
        - Returns the extracted minimum node
        """
        # Step 1: Check if the FibonacciHeap is empty

        # Check if the heap is empty
        if self.is_empty():

            # Print error message
            print("The FibonacciHeap is empty, there is no minimum node to extract")

            # Return None
            return None

        # Step 2: Retrieve the min_node

        # Create a new variable for the min_node
        x_node = self.min_node


        # Step 3: Check if the min-node has a child

        # Identify if the min_node has a child
        if x_node.child is not None:

            # Step 4: Promote children to the root list

            # Retrieve the first child
            first_child = x_node.child

            # Set a variable for current child
            current_child = first_child

            # While loop through the children
            while True:

                # Set the next child to be retrieved
                next_child = current_child.right

                # Remove the parent from the current child
                current_child.parent = None

                # Promote the current child to the root list
                self._merge_with_heap(current_child)

                # Check if next_child is the same as first_child
                if next_child == first_child:

                    # Break out of while loop
                    break

                # Set next_child as current_child
                current_child = next_child


        # Step 5: Remove min_node from the heap

        # Check if x_node is the only node in the root list
        if x_node.right == x_node:

            # Set min_node to None
            self.min_node = None

            # Update total_nodes
            self.total_nodes -= 1

        # Else
        else:

            # Remove x_node from the circular list
            x_node.left.right = x_node.right
            x_node.right.left = x_node.left            

            # Temporarily set min_node to some other root
            self.min_node = x_node.right

            # Update total_nodes
            self.total_nodes -= 1
        

        # Step 6: Check if the heap is empty

        # Check if the heap is empty
        if self.is_empty():

            # Return x_node
            return x_node


        # Step 7: Consolidate the heap

        # Run the consolidate() function on the heap
        # Consolidation rebuilds the root list and updates min_node automatically
        self._consolidate()

        # Step 8: Return the extracted min_node
        return x_node


    ###############################################################################################
    # Function: _cut
    # Description:
    # Cuts a node from its parent and moves it to the root list
    #
    # Input:    node          The node being cut
    #           parent_node   The parent of the node
    # Output:   N/A
    ###############################################################################################
    def _cut(self, node, parent_node):
        """
        Cut a node from its parent and move it to the root list.

        This operation:
        - Removes node from the parent's child circular list
        - Decreases the parent's degree
        - Adds node to the root list
        - Resets node.mark to False
        """

        # Step 1: Remove node from parent's child list

        # If node is the only child
        if node.right == node:

            # Update the parent to have no child
            parent_node.child = None

        # Else
        else:

            # Remove node from the circular child list
            node.left.right = node.right
            node.right.left = node.left

            # If node was the parent's child pointer
            if parent_node.child == node:

                # Update the parent's child pointer to the next child in the list
                parent_node.child = node.right


        # Step 2: Decrease parent's degree

        # Decrease degree by 1
        parent_node.degree -= 1


        # Step 3: Add node to the root list

        # The node must be reset before being reinserted into the root list.
        # Reset the node's left and right pointers to point to itself              
        node.left = node
        node.right = node

        # Set the node's parent to None  
        node.parent = None

        # Merge the node in to the root list
        self._merge_with_heap(node)


        # Step 4: Reset node's mark

        # Set the node's mark as being false
        node.mark = False


    ###############################################################################################
    # Function: _cascading_cut
    # Description:
    # Performs cascading cuts up the tree when a node loses a child
    #
    # Input:    node   The node to evaluate for cascading cuts
    # Output:   N/A
    ###############################################################################################
    def _cascading_cut(self, node):
        """
        Perform cascading cuts starting from a given node.

        This operation:
        - Marks a node if it loses one child
        - Cuts the node if it loses a second child
        - Recursively applies cascading cuts up the tree
        """

        # Step 1: Retrieve the parent of the node

        # Get the node's parent node
        parent_node = node.parent

        # If there is no parent node
        if parent_node is None:

            # Stop and return
            return

        # Step 2: If node is not marked, mark it

        # If the node has a mark of false
        if node.mark is False:

            # Change it to be true
            node.mark = True

            # Then return out of the function
            return

        # Step 3: If node is already marked, cut it and recurse

        # Perform a cut on the node
        self._cut(node, parent_node)

        # Recurse through the node's parent to perform any further required cuts
        self._cascading_cut(parent_node)



    ###############################################################################################
    # Function: decrease_key
    # Description:
    # Decreases the key value of a node in the Fibonacci Heap
    #
    # Input:    node        The node whose key is being decreased
    #           new_key     The new key value
    # Output:   N/A
    ###############################################################################################
    def decrease_key(self, node, new_key):
        """
        Decrease the key value of a node in the Fibonacci Heap.

        This operation:
        - Updates the node's key
        - Cuts the node from its parent if the heap-order property is violated
        - Performs cascading cuts if necessary
        - Updates the heap's min_node when appropriate
        """

        # Step 1: Check that new_key is valid

        # If the new_key is greater than the existing key
        if new_key > node.key:

            # Raise an error
            raise ValueError("Error: new_key is greater than the current key")

        # Step 2: Update the node's key

        # Set the node's key to be the new key
        node.key = new_key

        # Step 3: Check if heap-order property is violated

        # Grab the parent node of this node
        parent_node = node.parent

        # Check that parent_node is not none and that the node's key is less than the parent's key
        if parent_node is not None and node.key < parent_node.key:

            # Step 4: Cut the node from its parent
            self._cut(node, parent_node)

            # Step 5: Perform cascading cuts
            self._cascading_cut(parent_node)

        # Step 6: Update min_node if necessary
        if node.key < self.min_node.key:
            self.min_node = node
 


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

    # Check if the starting intersection exists
    if start_name not in network.intersections:

        # Print a message saying intersection doesn't exist
        print(f'Starting intersection {start_name} does not exist')

        # Return out of the function
        return

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
# Function: dijkstra_using_heap
# Description:
# Runs Dijkstra's Algorithm using the Fibonacci Heap
#
# Input:    RoadNetwork     The road network being searched
#           String          The name of the starting intersection
# Output:   N/A
###############################################################################################
def dijkstra_using_heap(network, start_name):
    """
    Compute the shortest paths from a starting intersection using Dijkstra's Algorithm
    with a Fibonacci Heap priority queue.

    This function updates each Intersection object in the provided RoadNetwork by:
    - Setting its `distance` attribute to the shortest known distance from the start node.
    - Setting its `parent` attribute to the previous node on the shortest path.
    - Maintaining a `heap_node` reference so each intersection can be updated efficiently
      using decrease-key operations.

    Parameters:
        network (RoadNetwork):
            The road network containing all intersections and directed roads.
        start_name (str):
            The name of the intersection from which shortest paths will be calculated.

    Algorithm Overview:
        1. Reset all intersections (distance = infinity, parent = None).
        2. Insert every intersection into a Fibonacci Heap, storing a reference to its heap node.
        3. Set the starting intersection's distance to 0.
        4. Repeatedly extract the intersection with the smallest known distance.
        5. Relax each outgoing road:
            - If a shorter path to a neighbour is found, update its distance and parent.
            - Apply a decrease-key operation to the neighbour's heap node.
        6. Continue until the heap is empty.

    Side Effects:
        Modifies the `distance`, `parent`, and `heap_node` attributes of Intersection objects
        inside `network`.

    Returns:
        None
        (Results are stored directly in the network's Intersection objects.)


    """
    # Create a Dijkstra's Fibonacc Heap Priority Queue
    dijkstra_heap = FibonacciHeap()

    # Ensure that all intersections start off with fresh settings    
    for intersection in network.intersections.values():

        # Set distance to infinity
        intersection.distance = math.inf

        # Set parent to None
        intersection.parent = None

        # Set an empty Heap Node variable
        intersection.heap_node = None

    # Check if the starting intersection exists
    if start_name not in network.intersections:

        # Print a message saying intersection doesn't exist
        print(f'Starting intersection {start_name} does not exist')

        # Return out of the function
        return

    # Retrieve the starting intersection
    start_node = network.intersections[start_name]

    # Initialise the distance for the starting intersection to zero
    start_node.distance = 0

    # For loop thorugh all intersections
    for intersection in network.intersections.values():

        # Create a Heap Node for this intersection
        heap_node = HeapNode(intersection.distance, intersection)

        # Insert the heap node in to the dijkstra heap
        dijkstra_heap.insert(heap_node)

        # Store the heap node as a reference
        # This allows us to use it later
        intersection.heap_node = heap_node

    # Main Dijkstra loop
    # While the heap isn't empty
    while not dijkstra_heap.is_empty():

        # Extract the heap node with the smallest distance
        current_heap_node = dijkstra_heap.extract_min()

        # Extract the intersection from the heap node
        current_intersection = current_heap_node.value

        # Relax Edges
        # For each neighbour of the heap node's intersection object
        for neighbor_name, weight in current_intersection.neighbors.items():

            # Retrieve the neighbor intersection object
            neighbor = network.intersections[neighbor_name]

            # Calculate the new distance for the neighbor intersection
            new_distance = current_intersection.distance + weight

            # Check if the new distance is less the the neighbor's existing distance
            if new_distance < neighbor.distance:

                # Update the neighbor's distance
                neighbor.distance = new_distance

                # Update the neighbor's parent
                neighbor.parent = current_intersection

                # Decrease the neighbor's key
                dijkstra_heap.decrease_key(neighbor.heap_node, new_distance)


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
# Output is restricted to only 15 Intersections
#
# Input:    RoadNetwork     The road network that was searched
#           String          The name of the starting intersection
# Output:   N/A
###############################################################################################
def print_distances(network, start_name):
    """
    Print the shortest distances and reconstructed paths from the starting intersection.

    The output is limited to just 15 intersections, as printing for every intersection 
    in a large road network is not practical.

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

    # Initialise a count to limit output
    count = 0

    # Loop through the Road Network's intersections
    for intersection in network.intersections.values():

        # If count is greater than or equal to 15
        if count >= 15:

            # Break out of loop
            break

        # Print the name and distance values for the intersection
        print(f'{intersection.name}: {intersection.distance}')

        # Reconstruct the path
        path = reconstruct_path(intersection)

        # Print the path
        print(f'Path {" -> ".join(path)}\n')

        # Increase count
        count += 1


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
    Run Dijkstra's Algorithm twice—first using a simple Priority Queue,
    then using a Fibonacci Heap—and report performance metrics for both.

    This function performs the following steps for each algorithm variant:
    - Starts a high-precision timer.
    - Begins memory allocation tracing.
    - Executes Dijkstra's Algorithm from the specified starting intersection.
    - Captures total execution time in milliseconds.
    - Captures peak memory usage during the run.
    - Prints timing and memory statistics.
    - Prints the shortest distances and reconstructed paths for all intersections.

    Parameters:
        network (RoadNetwork):
            The road network containing all intersections and directed roads.
        start_name (str):
            The name of the intersection from which Dijkstra's Algorithm will begin.

    Output:
        Prints, for both algorithm variants:
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

    # Start a timer
    start_time = time.perf_counter()
        
    # Start memory allocation tracing
    tracemalloc.start()
    
    # Run Dijstra's Algorithm using a Fibonacci Heap
    dijkstra_using_heap(network, start_name)
    
    # End the timer
    end_time = time.perf_counter()
        
    # Get the current and peak memory allocation
    heap_memory_current, heap_memory_peak = tracemalloc.get_traced_memory()
        
    # Stop memory allocation tracing
    tracemalloc.stop()
    
    # Calculate the length of time it took in milliseconds
    heap_total_time = (end_time - start_time) * 1000
    
    # Print the Algorithm's stats
    print(f'\n\nDijkstra with Heap time: {heap_total_time:.4f} ms')
    print(f'Dijkstra with Heap memory: {heap_memory_peak} bytes')
    
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
    - Creates the road network.
    - Adds all intersections.
    - Adds all directed roads.
    - Prints the network structure.
    - Runs Dijkstra's Algorithm twice:
        - Once using a Priority Queue.
        - Once using a Fibonacci Heap.
    - Prints shortest distances and reconstructed paths for each run.
    - Prints timing and memory usage statistics for each algorithm variant.

    It serves as the main driver for testing and comparing both implementations
    of Dijkstra's Algorithm.
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


