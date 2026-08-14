
###############################################################################################
# Imports
#
###############################################################################################
import math
import time
import tracemalloc



###############################################################################################
# Class: BTreeNode
# Description:
# Represents a single node in a B-Tree.
# Stores the minimum degree and whether this node is a leaf or not.
# Also stores the list of key values held by this node, and the list of children 
# connected to this node.
#
###############################################################################################
class BTreeNode:
    def __init__(self, t, leaf):
        """
        Create a new B-Tree node.
        
        Parameters:
            t (int):
                The minimum degree for the B-Tree.
            leaf (bool):
                Whether this node is a leaf
        
        Attributes:
            t (int):
                The minimum degree for the B-Tree
            leaf (bool):
                Whether this node is a leaf
            keys (list):
                The index values contained in this node.
            keys_min (int):
                The minimum number of values that must be in the keys list
            keys_max (int):
                The maximum number of values that can be in the keys list
            children (list):
                The child nodes connected to this node.
            children_min (int):
                Minimum number of children for a non-root, non-leaf node.
            children_max (int):
                Maximum number of children for any node.
        """
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.keys_min = t - 1
        self.keys_max = 2 * t - 1
        self.children = []
        self.children_min = t
        self.children_max = 2 * t


    ###############################################################################################
    # Function: insert
    # Description:
    # Inserts the provided key in to the BTreeNode
    # 
    #
    # Input:    key         The key to insert
    # Output:   N/A
    ###############################################################################################
    def insert(self, key):
        """
        Insert a key in to the B-Tree node.
        
        Parameters:
            key (int):
                The value to insert        
        
        """
        # Check if there are children
        if len(self.children) > 0:

            # Then identify which child to insert into
            # Create an index variable
            i = 0

            # While loop to get the correct key index value
            while i < len(self.keys) and key > self.keys[i]:

                # Increment the index
                i += 1

            # Insert the key in to the child for that index
            self.children[i].insert(key)

            # Return out of function
            return

        # Else Check if the node is full
        elif len(self.keys) == self.keys_max:

            # Then need to split the node
            self.split_root()

            # Insert the key
            self.insert(key)

            # Return out of the function
            return

        # Else Check if the node is a leaf
        elif self.leaf:

            # Insert the key
            self.keys.append(key)

            # Sort the keys
            self.keys.sort()

        # Else the insert can't be done
        else:

            # Print Error Message
            print("Error: Insert cannot be achieved as there is no valid node.")


    ###############################################################################################
    # Function: split_root
    # Description:
    # Splits the keys in the root node and creates children nodes to hold some of the keys
    # 
    #
    # Input:    key         The key to insert
    # Output:   N/A
    ###############################################################################################
    def split_root(self):
        """
        Splits a full root node up by creating children nodes
        
        """
        # Grab the degree value
        t = self.t

        # Create left and right child nodes
        child_left = BTreeNode(t, True)
        child_right = BTreeNode(t, True)

        # Determine the index to split the keys at
        median_index = t - 1
        
        # Store the median key
        median_key = self.keys[median_index]

        # Populate the left child with the keys before the median
        child_left.keys = self.keys[:median_index]

        # Populate the right child with the keys after the median
        child_right.keys = self.keys[median_index + 1:]

        # Update root to only have the median key
        self.keys = [median_key]

        # Update root to no longer be a leaf
        self.leaf = False

        # Attach children to the root node
        self.children = [child_left, child_right]
        
        




        
        

    ###############################################################################################
    # Function: search
    # Description:
    # Searches for the provided key
    # 
    #
    # Input:    BTreeNode   The node to conduct the search in
    #           key         The key to be search for
    # Output:   BTreeNode   The node that contains the key
    ###############################################################################################
    def search(self, node, key):
        """
        Search a B-Tree node.
        
        Parameters:
            node (BTreeNode):
                The node to be searched.
            key (int):
                The value to search for        
        
        """

        # For loop through the keys
        for index, k in enumerate(self.keys):

            # If the stored key is greater than or equal to the search value
            if self.keys[index] >= key:

                # Determine if the key has been found
                if self.keys[index] == key:

                    # Return this node
                    return node

                # Else if node is a leaf
                elif self.leaf == True:

                    # Return none as key cannot be found
                    return None
        


    

    def split_child(self, index):
        pass

    def traverse(self):
        pass

    def remove(self, key):
        pass

    def remove_from_leaf(self, idx):
        pass

    def remove_from_non_leaf(self, idx):
        pass

    def borrow_from_prev(self, idx):
        pass

    def merge(self, idx):
        pass

    def fill(self, idx):
        pass



###############################################################################################
# Class: BTree
# Description:
# Creates and Represents the entire B-Tree.
# Stores the minimum degree and the root BTreeNode.
#
###############################################################################################
class BTree:
    def __init__(self, t):
        """
        Create a new B-Tree.
                
        Parameters:
            t (int):
                The minimum degree for the B-Tree.
                
        Attributes:
            t (int):
                The minimum degree for the B-Tree
            root (BTreeNode):
                The root node for the B-Tree
        """
        self.t = t
        self.root = BTreeNode(t, True)


    ###############################################################################################
    # Function: insert
    # Description:
    # Insert a key in to the B-Tree
    #
    # Input:    key     The key that you want to insert
    # Output:   N/A
    ###############################################################################################
    def insert(self, key):
        """
        Inserts a key in to the B-Tree.
                
        Parameters:
            key (int):
                The key to insert.
        
        """

        # Insert the key
        self.root.insert(key)



    ###############################################################################################
    # Function: search
    # Description:
    # Searches the B-Tree for the specified key.
    # Starts at the root node in order to perform the search.
    #
    # Input:    key     The key that you want to search for
    # Output:   bool    Whether the search was successful
    ###############################################################################################
    def search(self, key):
        """
        Search a B-Tree.
        
        Parameters:
            key (int):
                The value to search for        
        
        """

    

    def delete(self, key):
        pass

    def traverse(self):
        pass























###############################################################################################
# Function: problem_2
# Description:
# Entry Point for running Problem 2
# 
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_2():
    """
    main.py
    Entry point for the assignment.

    This template includes standard imports (numpy, matplotlib)
    so you can begin coding immediately.
    """
    print("Program started.")
    # TODO: Add your assignment logic here

    # Example placeholder using numpy
    example_array = np.array([1, 2, 3])
    print("Example numpy array:", example_array)

    # Example placeholder using matplotlib
    # plt.plot(example_array)
    # plt.show()


if __name__ == "__problem_2__":
    problem_2()