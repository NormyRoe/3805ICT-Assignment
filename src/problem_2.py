
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

        This method implements node-driven B-Tree insertion for minimum degree t.
        Keys are always inserted into a leaf node, and full nodes are split as
        needed while descending the tree.

        Behaviour:
            • If the current node has children:
                - Determine which child subtree the key belongs to.
                - If that child is full (contains 2t-1 keys), split the child
                BEFORE descending. Splitting promotes the child's median key
                into the current node and replaces the child with two new
                children. After the split, the correct child index is recomputed.
                - Recursively continue insertion into the appropriate child.

            • If the current node is full and is the root:
                - The root is split using split_root(), promoting the median key
                and creating two children.
                - Insertion restarts at the updated root.

            • If the current node is full and is NOT the root:
                - The node is split using split_node(), promoting the median key
                to its parent and replacing the node with two new children.
                - Insertion restarts at the parent node, because the correct
                subtree may have changed after the split.

            • If the current node is a leaf:
                - Insert the key into the node's key list and keep the keys sorted.

        Notes:
            • Full children must always be split BEFORE descending into them.
            This ensures insertion never enters a full node, guaranteeing that
            leaf insertion is always possible.

            • Internal node splits redistribute both keys and children so that
            each resulting node satisfies B-Tree degree constraints.

            • After splitting a non-root node, insertion must restart at the
            parent, because the promoted median changes the parent's key ranges
            and therefore the correct subtree for the key.

            • Root growth (creating a new root above the old one) is handled by
            the BTree class, not by this method.
        
        """
        # Check if there are children
        if len(node.children) > 0:

            # Then identify which child to insert into
            # Get the index variable
            i = node.find_key_index(key)

            # Grab the child node
            child = node.children[i]

            # Check if the child has the maximum keys
            if len(child.keys) == child.keys_max:

                # Split the child
                self.split_node(child)

                # Re-get the index variable
                i = node.find_key_index(key)

                # Select the correct child node
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

                # Grab the parent node
                parent = node.parent

                # Split the node
                self.split_node(node)

                # Insert the key using the parent node
                self.insert(parent, key)

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
    # Input:    node    The root node to be split
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
    # Input:    node    The non-root node to be split
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

        After this operation, the original node is no longer part of the B-Tree 
        structure; it is replaced entirely by the two new nodes.
        
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
    #           key         The key to be searched for
    # Output:   BTreeNode   The node that contains the key
    ###############################################################################################
    def search(self, node, key):
        """
        Recursively search a B-Tree node for a specific key.

        Behaviour:
            • If the key exists in the current node's key list:
                - Return the current node.

            • If the current node is a leaf:
                - The key cannot be found anywhere below this point.
                - Return None.

            • Otherwise (internal node):
                - Determine which child subtree the key belongs to by scanning
                the node's keys.
                - Recursively search the selected child.
                - Return the result of the recursive search.

        Parameters:
            node (BTreeNode):
                The node to search within.
            key (int):
                The value to search for.

        Returns:
            BTreeNode or None:
                The node containing the key if found, otherwise None.
        
        """

        # For loop through the keys
        if key in node.keys:

            # Return the node
            return node

        # Else if there are no children
        elif len(node.children) == 0:

            # Key not found
            return None
        
        # Else identify which child to search
        else:

            # Get the index variable
            i = node.find_key_index(key)

            # Grab the child node
            child = node.children[i]

            # Search the child node
            return self.search(child, key)
        

    ###############################################################################################
    # Function: traverse
    # Description:
    # Performs an in-order traversal of a B-Tree node.
    # Appends all keys to the provided result list in sorted order.
    #
    # Input:    node    The BTreeNode to traverse
    #           result  A list used to collect keys during traversal
    # Output:   N/A
    ###############################################################################################  
    def traverse(self, node, result):
        """
        Perform an in-order traversal of a B-Tree node.

        In-order traversal visits keys in strictly sorted order by:
            • Recursively traversing each child subtree before its corresponding key.
            • Appending each key to the result list.
            • Traversing the final child after all keys have been processed.

        This logic applies to both leaf and internal nodes. Leaf nodes simply
        append their keys, while internal nodes recursively traverse their children
        in the correct in-order sequence.

        Parameters:
            node (BTreeNode):
                The node to traverse.
            result (list):
                A list that accumulates all keys encountered during traversal.

        Returns:
            None
                Keys are appended to the result list; no value is returned.
        """

        # For each key in the node
        for i in range(len(node.keys)):

            # If the node has children
            if len(node.children) > 0:

                # Traverse through the child for that key
                self.traverse(node.children[i], result)

            # Add the key to the result list
            result.append(node.keys[i])


        # If the node has children
        if len(node.children) > 0:

            # Traverse the last child
            self.traverse(node.children[len(node.keys)], result)

    ###############################################################################################
    # Function: delete
    # Description:
    # Deletes the provided key
    # 
    #
    # Input:    key         The key to be deleted
    # Output:   Bool        The result of the deletion
    ###############################################################################################
    def delete(self, key):
        """
        Delete the specific key from the B-Tree starting at this node.

        Behaviour:
            • If the key is found in this node:
                - If this node is a leaf, remove the key directly.
                - If this node is internal, use successor/predecessor or merge
                children to maintain B-Tree properties.
            • If the key is not in this node but this node has children:
                - Determine the child subtree where the key should be.
                - If that child is at minimum capacity, fix it (borrow or merge)
                before descending.
                - Recursively delete the key from the chosen child.
            • If the key is not in this node and this node is a leaf:
                - The key does not exist; return False.

        Returns:
            bool:
                True if the key was deleted, False if the key was not found.
        
        """

        # Step 1: Find the index of the key or the child to descend into
        index = self.find_key_index(key)

        # Step 2: Case A: Key is in this node

        # If the index is less then the count of keys
        # And the key at that index matches the provided key
        if index < len(self.keys) and self.keys[index] == key:

            # Case A-1: Node is a Leaf

            # Check if the node is a leaf
            if self.leaf:

                # Delete the key
                del self.keys[index]

                # return true
                return True

            # Case A-2: Node is not a Leaf

            # Else the node is not a leaf
            else:

                # Indentify the children either side of the index
                child_left = self.children[index]
                child_right = self.children[index + 1]

                # Case A-2-2: Use Successor

                # Check if the right child has more than the minimum keys
                if len(child_right.keys) > self.keys_min:

                    # Find the successor (smallest key in right child)
                    successor = child_right.get_successor()

                    # Replace the key with the successor
                    self.keys[index] = successor

                    # Delete the successor from the right child
                    return child_right.delete(successor)

                # Case A-2-3: Use Predecessor

                # Else if the left child has more than the minimum keys
                elif len(child_left.keys) > self.keys_min:
                
                    # Find the predecessor (largest key in left child)
                    predecessor = child_left.get_predecessor()
                
                    # Replace the key with the predecessor
                    self.keys[index] = predecessor
                
                    # Delete the predecessor from the left child
                    return child_left.delete(predecessor)

                # Case A-2-4: Merge Children

                # Else neither children have enough keys
                else:

                    # Merge the children
                    self.merge_children(index)

                    # After merging, the merged node is at children[index]
                    merged_child = self.children[index]

                    # Delete the key from the merged child
                    return merged_child.delete(key)

        # Step 2: Case B: Key is not in this node

        # Else if the node has children
        elif len(self.children) > 0:

            # Determine the child to descend into
            child = self.children[index]

            # Check if the child has at least t keys
            if len(child.keys) == self.keys_min:

                # Fix the child
                self.fix_child(index)

                # Re-calculate index
                index = self.find_key_index(key)

                # Re-grab the child
                child = self.children[index]

            # Descend in to the child
            return child.delete(key)

        # Step 3: Case C: Key doesn't exist

        # Else key doesn't exist
        else:

            # Return False
            return False


    ###############################################################################################
    # Function: find_key_index
    # Description:
    # Finds the index of the key in the node, or the child index to descend into.
    #
    # Input:    key         The key being searched for
    # Output:   int         The index position
    ###############################################################################################
    def find_key_index(self, key):
        """
        Find the index of the key in this node, or the index of the child
        subtree where the key should be located.

        Behaviour:
            • Scans the node's keys from left to right.
            • If a key >= the target key is found:
                - Returns its index.
            • If all keys are smaller:
                - Returns len(self.keys), which corresponds to the last child.

        Parameters:
            key (int):
                The key to locate.

        Returns:
            int:
                The index of the key if present, or the child index to descend into.
        """
        # Create an index variable
        i = 0
        
        # While loop to get the correct key index value
        while i < len(self.keys) and key > self.keys[i]:
        
            # Increment the index
            i += 1

        # Return the index
        return i


    ###############################################################################################
    # Function: get_successor
    # Description:
    # Finds the successor of a key by locating the smallest key in the right subtree.
    #
    # Input:    None (uses self as the subtree root)
    # Output:   int  The successor key
    ###############################################################################################
    def get_successor(self):
        """
        Find the successor key in this subtree.

        Behaviour:
            • Start at this node (the right child of the key being deleted).
            • Descend left until reaching a leaf.
            • The first key in that leaf is the successor.

        Returns:
            int:
                The smallest key in the subtree (the successor).
        """

        # Start at this node
        current = self

        # Descend left until reaching a leaf
        while not current.leaf:

            # Move to the leftmost child
            current = current.children[0]

        # Now current is a leaf; the first key is the successor
        return current.keys[0]


    ###############################################################################################
    # Function: get_predecessor
    # Description:
    # Finds the predecessor of a key by locating the largest key in the left subtree.
    #
    # Input:    None (uses self as the subtree root)
    # Output:   int  The predecessor key
    ###############################################################################################
    def get_predecessor(self):
        """
        Find the predecessor key in this subtree.

        Behaviour:
            • Start at this node (the left child of the key being deleted).
            • Descend right until reaching a leaf.
            • The last key in that leaf is the predecessor.

        Returns:
            int:
                The largest key in the subtree (the predecessor).
        """

        # Start at this node
        current = self

        # Descend right until reaching a leaf
        while not current.leaf:

            # Move to the rightmost child
            current = current.children[-1]

        # Now current is a leaf; the last key is the predecessor
        return current.keys[-1]


    ###############################################################################################
    # Function: merge_children
    # Description:
    # Merges two children so that key deletion can occur
    #
    # Input:    index   The index around which the children need to be merged
    # Output:   N/A
    ###############################################################################################
    def merge_children(self, index):
        """
        Merge the child at index with the child at index+1,
        bringing the parent's key at 'index' down between them.

        Behaviour:
            • The parent's key at 'index' is moved down between the two children.
            • The right child is merged into the left child (keys and children).
            • The parent removes the key and the right child.

        """

        # Step 1: Identify the two children

        # Grab the two children
        child_left = self.children[index]
        child_right = self.children[index + 1]

        # Step 2: Bring the parent's key down into the left child

        # Grab the key from the parent
        key_from_parent = self.keys[index]

        # Add this key to the end of the left child's keys
        child_left.keys.append(key_from_parent)

        # Step 3: Append all keys from the right child

        # Add all of the right child's keys to the left child's keys
        child_left.keys.extend(child_right.keys)

        # Empty the right child of keys
        child_right.keys = []

        # Step 4: Append all children from the right child (if any)

        # If the right child has children
        if len(child_right.children) > 0:

            # For each of the right child's children
            for c in child_right.children:
            
                # Update their parent pointer
                c.parent = child_left

            # Add those children to the left child's children list
            child_left.children.extend(child_right.children)

            # Empty the right child of children
            child_right.children = []

        # Step 5: Remove the key from the parent
        self.keys.pop(index)

        # Step 6: Remove the right child from the parent's children list
        self.children.pop(index + 1)

        # Step 7: Update the merged child's parent pointer
        child_left.parent = self


    ###############################################################################################
    # Function: fix_child
    # Description:
    # Ensures the child at the specified index has at least t keys before descending.
    #
    # Input:    int         The index of the child to fix
    # Output:   None
    ###############################################################################################
    def fix_child(self, index):
        """
        Ensure that the child at the specified index has at least t keys before descending.

        Behaviour:
            • If the right sibling exists and has > keys_min keys:
                - Borrow a key from the right sibling.
                
            • Else if the left sibling exists and has > keys_min keys:
                - Borrow a key from the left sibling.

            • Else:
                - Merge the child with a sibling.
                - After merging, the child to descend into changes.

        Parameters:
            index (int):
                The index of the child to fix.

        Returns:
            None
        """

        # Case 1: Borrow from right sibling

        # If index is less than the number of children, and the right child has more keys
        if index < len(self.children) - 1 and len(self.children[index + 1].keys) > self.keys_min:

            # Borrow from the right sibling
            self.borrow_from_right(index)

            # return
            return
        

        # Case 2: Borrow from left sibling

        # If index is greater than 0, and the left child has more keys
        elif index > 0 and len(self.children[index - 1].keys) > self.keys_min:
        
            # Borrow from the left sibling
            self.borrow_from_left(index)
        
            # return
            return        

        # Case 3: Merge with a sibling
        else:

            # Case 3-A: Merge with right sibling

            # If index is less than the number of children
            if index < len(self.children) - 1:

                # Merge child with right sibling
                self.merge_children(index)
                return
            
            # Case 3-B: Merge with left sibling

            # Else index is greater than 0
            else:

                # Merge child with left sibling
                self.merge_children(index - 1)
                return


    ###############################################################################################
    # Function: borrow_from_right
    # Description:
    # Borrows a key from the right sibling so that the child at index
    # has enough keys to safely descend into.
    #
    # Input:    index   The index of the child needing keys
    # Output:   N/A
    ###############################################################################################
    def borrow_from_right(self, index):
        """
        Borrow one key from the right sibling of the child at 'index'.

        Behaviour:
            • Move the parent's separator key down into the child.
            • Move the right sibling's first key up into the parent.
            • Move the right sibling's first child (if any) into the child.
        """

        # Grab the child
        child = self.children[index]

        # Grab the child's right sibling
        right_sibling = self.children[index + 1]

        # Step 1: Move the parent's separator key down into the child

        # The separator key is at 'index' in the parent's key list
        child.keys.append(self.keys[index])

        # Step 2: Replace the parent's separator key with the right sibling's first key
        self.keys[index] = right_sibling.keys.pop(0)

        # Step 3: If the sibling has children, move its first child into 'child'
        if len(right_sibling.children) > 0:

            # Grab the first child pointer
            moved_child = right_sibling.children.pop(0)

            # Update its parent pointer
            moved_child.parent = child

            # Add it to the end of the child's children list
            child.children.append(moved_child)
    

    ###############################################################################################
    # Function: borrow_from_left
    # Description:
    # Borrows a key from the left sibling so that the child at index
    # has enough keys to safely descend into.
    #
    # Input:    index   The index of the child needing keys
    # Output:   N/A
    ###############################################################################################
    def borrow_from_left(self, index):
        """
        Borrow one key from the left sibling of the child at 'index'.

        Behaviour:
            • Move the parent's separator key down into the child.
            • Move the left sibling's last key up into the parent.
            • Move the left sibling's last child (if any) into the child.
        """

        # Grab the child
        child = self.children[index]

        # Grab the child's left sibling
        left_sibling = self.children[index - 1]

        # Step 1: Move the parent's separator key down into the child

        # The separator key is at 'index - 1' in the parent's key list
        child.keys.insert(0, self.keys[index - 1])

        # Step 2: Replace the parent's separator key with the sibling's last key
        self.keys[index - 1] = left_sibling.keys.pop()

        # Step 3: If the sibling has children, move its last child into 'child'
        if len(left_sibling.children) > 0:

            # Grab the last child pointer
            moved_child = left_sibling.children.pop()

            # Update its parent pointer
            moved_child.parent = child

            # Add it to the front of the child's children list
            child.children.insert(0, moved_child)



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
    # Function: print_node
    # Description:
    # Prints the B-Tree node that contains the key searched for
    #
    # Input:    BTreeNode     The node that contains the key
    #           Key           The key that was searched for
    # Output:   N/A
    ###############################################################################################
    def print_node(self, node, key):
        """
        Print a message indicating that the search was successful and display
        the B-Tree node containing the requested key.

        Parameters:
            node (BTreeNode):
                The node in which the key was found.
            key (int):
                The key that was searched for.

        Returns:
            None
                This method prints output directly.
        
        """
        # Print success message
        print(f'Search Successful: {key} found in the below node')

        # Print the node
        print(f"Node(keys={node.keys})")
        

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
        Search the B-Tree for a specific key, starting at the root node.

        This method performs a user-facing search operation. It delegates the
        actual recursive search logic to BTreeNode.search(), which returns either
        the node containing the key or None.

        Behaviour:
            • If the key is found:
                - print_node() is called to display a success message and the
                node containing the key.

            • If the key is not found:
                - A message is printed indicating that the key does not exist
                in the B-Tree.

        Parameters:
            key (int):
                The value to search for.

        Returns:
            None
                This method does not return the node; it prints the result
                directly for user feedback.
        
        """

        # Search for the provided key
        result = self.root.search(self.root, key)

        # If result is not None
        if result is not None:

            # Print the BTreeNode
            self.print_node(result, key)

        # Else no result
        else:

            # Print a message
            print(f'Search unsuccessful: {key} does not exist')


    ###############################################################################################
    # Function: traverse
    # Description:
    # Performs an in-order traversal of the entire B-Tree.
    # Prints all keys in sorted order.
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def traverse(self):
        """
        Perform an in-order traversal of the entire B-Tree.

        This method begins traversal at the root node and collects all keys
        in sorted order using BTreeNode.traverse(). Once traversal is complete,
        the keys are printed as a comma-separated list.

        In-order traversal is useful for:
            • Verifying structural correctness of the B-Tree.
            • Debugging insertion and deletion operations.
            • Producing a sorted list of all keys stored in the tree.

        Returns:
            None
                This method prints output directly.
        """

        # Print an empty line
        print("In-Order Traversal of the B-Tree:\n")

        # Create an empty result list
        result = []
        
        # Traverse from the root BTreeNode
        self.root.traverse(self.root, result)

        # Print the results with a comma and space separating each key
        print(", ".join(str(k) for k in result))

        # Print an empty line
        print()


    ###############################################################################################
    # Function: delete
    # Description:
    # Deletes the specified key from the B-Tree
    # Prints a message for the user
    #
    # Input:    N/A
    # Output:   N/A
    ###############################################################################################
    def delete(self, key):
        """
        Deletes a specific key from the B-Tree.

        This method performs a user-facing delete operation. It delegates the
        actual recursive deletion logic to BTreeNode.delete(), which returns either
        True or False.

        Behaviour:
            • If the key is deleted:
                - Display a success message

            • If the key is not deleted:
                - Displays a message indicating that the key does not exist
                in the B-Tree.

        Parameters:
            key (int):
                The value to delete.

        Returns:
            None
                This method does not return anything; it prints the result
                directly for user feedback.
        
        """

        # Delete the provided key
        result = self.root.delete(key)

        # If root becomes empty and has children
        if len(self.root.keys) == 0 and len(self.root.children) > 0:

            # Replace the root with its only child
            self.root = self.root.children[0]

            # Update the new root to have no parent
            self.root.parent = None

        # If result is true
        if result:

            # Print a confirmation message
            print(f'Successfully Deleted key: {key}')

        # Else result is false
        else:

            # Print a message
            print(f'Deletion Unsuccessful: Unable to find key {key}')



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

    b_tree.search(75)

    print("\n")
    
    b_tree.search(16)

    print("\n")
    
    b_tree.search(36)

    print("\n")
    
    b_tree.search(46)

    print("\n")

    b_tree.traverse()



if __name__ == "__main__":
    problem_2()