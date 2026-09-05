"""
test_main.py
Pytest file for testing the Assignment's Problem 3.
"""

from src.problem_5 import run_algorithms


###############################################################################################
# Test Function: test_case_1_not_valid
# Description:
# Tests what happens when there is no possible convex hull
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_1_not_valid():

    # Print what is being tested
    print("Test Case 1: Not Valid\n")

    # Create Co-ordinates
    coordinates = [(3, 3), (4, 5)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_2_no_convex
# Description:
# Tests what happens when there is no polygon convex hull
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_2_no_convex():

    # Print what is being tested
    print("Test Case 2: No Convex\n")

    # Create Co-ordinates
    coordinates = [(3, 3), (4, 4), (1, 1), (2, 2)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_3_no_issues
# Description:
# Tests what happens when there are no potential issues
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_3_no_issues():

    # Print what is being tested
    print("Test Case 3: No Issues\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (5, 2), (1, 1), (8, 5), (7, 9), 
                   (2, 6), (4, 7), (9, 3), (6, 1), (0, 3)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_4_single_collinear
# Description:
# Tests what happens when there two points on the same line
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_4_single_collinear():

    # Print what is being tested
    print("Test Case 4: Single Collinear\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (5, 2), (1, 1), (8, 5), (7, 9), 
                   (2, 6), (4, 7), (9, 3), (6, 1), (0, 3), 
                   (5, 3)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_5_multiple_collinear
# Description:
# Tests what happens when there two points on the same line, in multiple locations
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_5_multiple_collinear():

    # Print what is being tested
    print("Test Case 5: Multiple Collinear\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (5, 2), (1, 1), (8, 5), (7, 9), 
                   (2, 6), (4, 7), (9, 3), (6, 1), (0, 3), 
                   (5, 3), (8, 4), (1, 3)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_6_densely_clustered
# Description:
# Tests what happens when the points are densely clustered together
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_6_densely_clustered():

    # Print what is being tested
    print("Test Case 6: Densely Clustered\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (2, 3), (1, 1), (4, 5), (1, 3), 
                   (2, 4), (3, 2), (1, 4), (2, 5), (3, 3), 
                   (2, 2), (3, 1), (1, 2), (2, 1), (4, 2), 
                   (1, 6)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_7_sparsely_clustered
# Description:
# Tests what happens when the points are sparsely clustered
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_7_sparsely_clustered():

    # Print what is being tested
    print("Test Case 7: Sparsely Clustered\n")

    # Create Co-ordinates
    coordinates = [(3, 4), (2, 2), (1, 0), (4, 5), (1, 5), 
                   (2, 6), (6, 6), (5, 1)]
    
    # Run the algorithms
    run_algorithms(coordinates)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")




if __name__ == "__main__":
    test_case_1_not_valid()
    test_case_2_no_convex()
    test_case_3_no_issues()
    test_case_4_single_collinear()
    test_case_5_multiple_collinear()
    test_case_6_densely_clustered()
    test_case_7_sparsely_clustered()
