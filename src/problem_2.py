
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
            parent (BTreeNode):
                The parent node for this node.
        """
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.keys_min = t - 1
        self.keys_max = 2 * t - 1
        self.children = []
        self.children_min = t
        self.children_max = 2 * t
        self.parent = None


    ###############################################################################################
    # Function: insert
    # Description:
    # Inserts the provided key in to the BTreeNode
    # 
    #
    # Input:    BTreeNode   The node to insert the key into
    #           key         The key to insert
    # Output:   N/A
    ###############################################################################################
    def insert(self, node, key):
        """
    Insert a key into the B-Tree starting at the given node.

    This method implements the standard B-Tree insertion algorithm for a
    minimum degree t, using a node-driven design. Keys are always inserted
    into a leaf node, and internal nodes are split as needed while descending
    the tree.

    Behaviour:
        • If the current node has children:
            - Determine which child subtree the key belongs to.
            - If that child is full (contains 2t-1 keys), split the child
              BEFORE descending. Splitting promotes the child's median key
              into the current node and replaces the child with two new
              children. After the split, the correct child index is recomputed.
            - Recursively continue insertion into the appropriate child.

        • If the current node is a leaf:
            - Insert the key into the node's key list and keep the keys sorted.

        • If the current node is full and is the root:
            - The root is split using split_root(), which promotes the median
              key and creates two children. Insertion then restarts at the
              updated root.

        • If the current node is full and is NOT the root:
            - The node is split using split_node(), which promotes the median
              key to its parent and replaces the node with two new children.

    Notes:
        • Full children must always be split BEFORE descending into them.
          This guarantees that insertion never enters a full node, ensuring
          that leaf insertion is always possible.

        • Internal node splits redistribute both keys and children so that
          each resulting node satisfies B-Tree degree constraints.

        • Root growth (creating a new root above the old one) is handled by
          the BTree class, not by this method.
        
        """
        # Check if there are children
        if len(node.children) > 0:

            # Then identify which child to insert into
            # Create an index variable
            i = 0

            # While loop to get the correct key index value
            while i < len(node.keys) and key > node.keys[i]:

                # Increment the index
                i += 1

            # Grab the child node
            child = node.children[i]

            # Check if the child's keys is full
            if len(child.keys) == child.keys_max:

                # Child is full, so split the child
                self.split_node(child)

                # Reset the index variable
                i = 0
                
                # While loop to re-get the key index value (as it may have changed)
                while i < len(node.keys) and key > node.keys[i]:
                
                    # Increment the index
                    i += 1
                
                # Grab the child node
                child = node.children[i]

            # Insert the key in to the child for that index
            self.insert(child, key)

            # Return out of function
            return

        # Else Check if the node is full
        elif len(node.keys) == node.keys_max:

            # Check if the node is the root
            if node.parent is None:

                # Split the node
                node.split_root(node)

                # Insert the key
                self.insert(node, key)

                # Return out of the function
                return

            # Else it is not the root node
            else:

                # Split the node
                self.split_node(node)

        # Else Check if the node is a leaf
        elif node.leaf:

            # Insert the key
            node.keys.append(key)

            # Sort the keys
            node.keys.sort()

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
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def split_root(self, node):
        """
        Split a full root node.

        The root is the only node allowed to have fewer than t children, so root
        splitting is handled differently from internal node splitting:

            • The median key becomes the new root key.
            • Two new child nodes are created:
                - The left child receives all keys before the median.
                - The right child receives all keys after the median.
            • The root transitions from a leaf to an internal node.
            • The new children are attached to the root, and their parent pointers
            are updated accordingly.

        After this operation, the height of the B-Tree increases by one level.
        
        """
        # Grab the degree value
        t = node.t

        # Create left and right child nodes
        child_left = BTreeNode(t, True)
        child_right = BTreeNode(t, True)

        # Add the root node as the parent for the child nodes
        child_left.parent = node
        child_right.parent = node

        # Determine the index to split the keys at
        median_index = t - 1
        
        # Store the median key
        median_key = node.keys[median_index]

        # Populate the left child with the keys before the median
        child_left.keys = node.keys[:median_index]

        # Populate the right child with the keys after the median
        child_right.keys = node.keys[median_index + 1:]

        # Update root to only have the median key
        node.keys = [median_key]

        # Update root to no longer be a leaf
        node.leaf = False

        # Attach children to the root node
        node.children = [child_left, child_right]
        

    ###############################################################################################
    # Function: split_node
    # Description:
    # Splits the keys in non-root nodes and creates children nodes to hold some of the keys
    # If the node being split is a parent node, redistribute the existing children 
    # amongst the two new children nodes.
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def split_node(self, node):
        """
        Split a full non-root node and promote its median key to the parent.

        This method handles splitting both leaf nodes and internal nodes:

            • For leaf nodes:
                - The node's keys are divided into two new leaf nodes.
                - The median key is promoted to the parent.
                - The parent replaces the original node with the two new nodes.

            • For internal nodes:
                - Keys are split around the median.
                - Children are redistributed: the left new node receives the first
                t children, and the right new node receives the last t children.
                - All redistributed children have their parent pointers updated.
                - The median key is promoted to the parent.
                - The parent replaces the original node with the two new nodes.

        The original node is logically removed from the tree structure once the
        parent replaces it. No further operations are performed on the old node.
        
        """
        # Grab the degree value
        t = node.t

        # Grab the parent node
        parent = node.parent

        # Create left and right replacement nodes
        child_left = BTreeNode(t, node.leaf)
        child_right = BTreeNode(t, node.leaf)

        # Add the parent pointers
        child_left.parent = parent
        child_right.parent = parent

        # Determine the index to split the keys at
        median_index = t - 1
        
        # Store the median key
        median_key = node.keys[median_index]

        # Populate the left child with the keys before the median
        child_left.keys = node.keys[:median_index]

        # Populate the right child with the keys after the median
        child_right.keys = node.keys[median_index + 1:]

        # If the non-root node is a parent node
        if not node.leaf:

            # Use the minimum degree to split the node's children up 
            # between the new child nodes
            child_left.children = node.children[:t]
            child_right.children = node.children[t:]

            # For each child in child_left
            for child in child_left.children:

                # Update the parent pointers
                child.parent = child_left

            # For each child in child_right
            for child in child_right.children:
            
                # Update the parent pointers
                child.parent = child_right

        # Find node's index in parent's children list
        parent_index = parent.children.index(node)

        # Insert median key in to parent
        parent.keys.insert(parent_index, median_key)

        # Replace node with child_left and child_right
        parent.children[parent_index] = child_left
        parent.children.insert(parent_index + 1, child_right)






        
        

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
    # Insert a key in to the B-Tree.
    # Grows the tree if the root node has the maximum number of children 
    # and splits the old root node.
    #
    # Input:    key     The key that you want to insert
    # Output:   N/A
    ###############################################################################################
    def insert(self, key):
        """
        Insert a key into the B-Tree.

        This method manages root growth and delegates all structural insertion
        logic to BTreeNode.insert().

        Behaviour:
            • If the root has the maximum number of children (2t), the tree must
            grow upward:
                - A new root is created.
                - The old root becomes its child.
                - The old root is split as a child of the new root.
                - The B-Tree's root pointer is updated.

            • After handling possible root growth, insertion proceeds by calling
            insert() on the root node, which performs all necessary splits and
            recursive descent.

        Notes:
            • Root growth is the only structural change that must be performed at
            the BTree level, because only the BTree object owns the root pointer.
            • All other splitting logic is handled by BTreeNode methods.
        
        """
        # Grab the root node
        root = self.root

        # Determine if the root has the maximum number of children
        if len(root.children) == root.children_max:

            # Create a new root
            new_root = BTreeNode(root.t, False)

            # Link the old root to the new one
            new_root.children.append(root)

            # Update the parent for the old root
            root.parent = new_root

            # Update the B-Tree's root pointer
            self.root = new_root

            # Split the old root node
            new_root.split_node(root)

        # Insert the key
        self.root.insert(self.root, key)


    ###############################################################################################
    # Function: print_tree
    # Description:
    # Prints the B-Tree
    #
    # Input:    BTreeNode     The node that the tree starts at
    # Output:   N/A
    ###############################################################################################
    def print_tree(self, node, level=0):
        """
        Recursively print the structure of the B-Tree starting at the given node.

        Each level of the tree is indented to visually represent the hierarchy.
        Internal nodes and leaf nodes are printed in the same format, showing only
        their key lists. Child nodes are printed beneath their parent with one
        additional level of indentation.

        This function is intended for debugging and visual verification of B-Tree
        structure after insertions and splits.
        
        """

        indent = "    " * level

        print(f"{indent}Node(keys={node.keys})")

        for child in node.children:

            self.print_tree(child, level + 1)


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
    print("Program started.\n")

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    
    b_tree.print_tree(b_tree.root)

    print("\n")

    print("Insert: 5")
    b_tree.insert(5)

    b_tree.print_tree(b_tree.root)

    print("\n")

    print("Insert: 2, 4, 5, 8")
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(6)
    b_tree.insert(8)

    b_tree.print_tree(b_tree.root)

    print("\n")

    print("Insert: 12, 14, 16, 18, 22, 24, 26, 28")
    b_tree.insert(12)
    b_tree.insert(14)
    b_tree.insert(16)
    b_tree.insert(18)
    b_tree.insert(22)
    b_tree.insert(24)
    b_tree.insert(26)
    b_tree.insert(28)

    b_tree.print_tree(b_tree.root)
    
    print("\n")
    
    print("Insert: 32, 34, 36")
    b_tree.insert(32)    
    b_tree.insert(34)    
    b_tree.insert(36)

    b_tree.print_tree(b_tree.root)
    print("\n")

    print("Insert: 38, 42, 44, 46, 48")
    b_tree.insert(38)
    b_tree.insert(42)
    b_tree.insert(44)
    b_tree.insert(46)
    b_tree.insert(48)

    b_tree.print_tree(b_tree.root)
        
    print("\n")

    print("Insert: 52, 54, 56, 58, 62, 64, 66, 68")
    b_tree.insert(52)    
    b_tree.insert(54)    
    b_tree.insert(56)
    b_tree.insert(58)
    b_tree.insert(62)
    b_tree.insert(64)
    b_tree.insert(66)
    b_tree.insert(68)

    b_tree.print_tree(b_tree.root)
            
    print("\n")



if __name__ == "__main__":
    problem_2()