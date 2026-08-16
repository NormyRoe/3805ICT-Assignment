"""
test_problem_2.py
Pytest file for testing the Assignment's Problem 2.
"""

from src.problem_2 import BTree


###############################################################################################
# Test Function: test_case_1_root_full
# Description:
# Tests what happens when the root node is full
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_1_root_full():

    # Print what is being tested
    print("Test Case 1: Root is full\n")

    # Create the B-Tree
    b_tree = BTree(3)
    
    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50]:

        # Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be inserted
    print("Insert: 5")

    # Insert the key
    b_tree.insert(5)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")

    


###############################################################################################
# Test Function: test_case_2_root_child_full
# Description:
# Tests what happens when one of the root's children is full
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_2_root_child_full():

    # Print what is being tested
    print("Test Case 2: Root Child is full\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36]:

        # Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be inserted
    print("Insert: 38")

    # Insert the key
    b_tree.insert(38)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_3_root_max_children
# Description:
# Tests what happens when the root has max children
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_3_root_max_children():

    # Print what is being tested
    print("Test Case 3: Root has max children\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 70, 75")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 70, 75]:

        # Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be inserted
    print("Insert: 80")

    # Insert the key
    b_tree.insert(80)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_4_non_root_max_children
# Description:
# Tests what happens when a non-root has max children
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_4_non_root_max_children():

    # Print what is being tested
    print("Test Case 4: Non-Root has max children\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, " \
            "70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 
              54, 56, 70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125]:

        # Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

        # Print what will be inserted
    print("Insert: 130")

    # Insert the key
    b_tree.insert(130)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_5_search_nonexistent
# Description:
# Tests what happens when you search for a key that doesn't exist
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_5_search_nonexistent():

    # Print what is being tested
    print("Test Case 5: Search - Key doesn't exist\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Search for key
    b_tree.search(75)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_6_search_exists
# Description:
# Tests what happens when you search for a key that exists in one of the root's children
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_6_search_exists():

    # Print what is being tested
    print("Test Case 6: Search - Key exists\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Search for key
    b_tree.search(40)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_7_traversal
# Description:
# Tests the In_order traversal of the B-Tree
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_7_traversal():

    # Print what is being tested
    print("Test Case 7: Traversal\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Search for key
    b_tree.traverse()

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_8_delete_fail
# Description:
# Tests the deletion for a key that doesn't exist in the B-Tree
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_8_delete_fail():

    # Print what is being tested
    print("Test Case 8: Delete Failed\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 58")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 58]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be deleted
    print("Delete: 72")

    # Delete key
    b_tree.delete(72)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_9_delete_succeed
# Description:
# Tests the deletion for a key that does exist in the B-Tree
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_9_delete_succeed():

    # Print what is being tested
    print("Test Case 9: Delete Succeeds\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, " \
            "70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 
              54, 56, 70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be deleted
    print("Delete: 44")

    # Delete key
    b_tree.delete(44)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_10_delete_shrink
# Description:
# Tests the deletion for a key that does exist in the B-Tree and that results 
# in the B-Tree shrinking one level.
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_10_delete_shrink():

    # Print what is being tested
    print("Test Case 10: Delete Shrink\n")

    # Create the B-Tree
    b_tree = BTree(3)

    # Print what will be inserted
    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 70, 75, 80")

    # For loop for insertion
    for k in [10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 70, 75, 80]:

		# Insert the key
        b_tree.insert(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print what will be deleted
    print("Delete: 42, 36")

    # For loop for deletion
    for k in [42, 36]:

        # Delete key
        b_tree.delete(k)

    # Print an empty line
    print("\n")

    # Print the B-Tree
    b_tree.print_tree(b_tree.root)

    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


if __name__ == "__main__":
    test_case_1_root_full()
    test_case_2_root_child_full()
    test_case_3_root_max_children()
    test_case_4_non_root_max_children()
    test_case_5_search_nonexistent()
    test_case_6_search_exists()
    test_case_7_traversal()
    test_case_8_delete_fail()
    test_case_9_delete_succeed()
    test_case_10_delete_shrink()