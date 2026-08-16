"""
test_main.py
Basic pytest template for assignment testing.
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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(32)
    b_tree.insert(34)
    b_tree.insert(36)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48, 52, 54, 56, 58")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(32)
    b_tree.insert(34)
    b_tree.insert(36)
    b_tree.insert(38)
    b_tree.insert(42)
    b_tree.insert(44)
    b_tree.insert(46)
    b_tree.insert(48)
    b_tree.insert(52)
    b_tree.insert(54)
    b_tree.insert(56)
    b_tree.insert(58)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(32)
    b_tree.insert(34)
    b_tree.insert(36)

    # Print an empty line
    print("\n")

    b_tree.search(75)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(32)
    b_tree.insert(34)
    b_tree.insert(36)
    b_tree.insert(38)
    b_tree.insert(42)
    b_tree.insert(44)
    b_tree.insert(46)
    b_tree.insert(48)

    # Print an empty line
    print("\n")

    b_tree.search(40)

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

    b_tree = BTree(3)

    print("Insert: 10, 20, 30, 40, 50, 5, 2, 4, 32, 34, 36, 38, 42, 44, 46, 48")
    b_tree.insert(10)
    b_tree.insert(20)
    b_tree.insert(30)
    b_tree.insert(40)
    b_tree.insert(50)
    b_tree.insert(5)
    b_tree.insert(2)
    b_tree.insert(4)
    b_tree.insert(32)
    b_tree.insert(34)
    b_tree.insert(36)
    b_tree.insert(38)
    b_tree.insert(42)
    b_tree.insert(44)
    b_tree.insert(46)
    b_tree.insert(48)

    # Print an empty line
    print("\n")

    b_tree.traverse()

    # Print an empty line
    print("\n")

    