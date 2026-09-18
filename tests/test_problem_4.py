"""
test_main.py
Pytest file for testing the Assignment's Problem 4.
"""

from src.problem_4 import run_programming

###############################################################################################
# Test Function: test_case_1_invalid_budget
# Description:
# Tests what happens when a non-number variable is provided as the budget
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_1_invalid_budget():

    # Print what is being tested
    print("Test Case 1: Invalid Budget\n")

    # Create the budget amount
    budget = "80"
    
    # Run the programming functions
    run_programming(budget)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_2_zero_budget
# Description:
# Tests what happens when the provided budget is zero
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_2_zero_budget():

    # Print what is being tested
    print("Test Case 2: Zero Budget\n")

    # Create the budget amount
    budget = 0
    
    # Run the programming functions
    run_programming(budget)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_3_exact_budget
# Description:
# Tests what happens when the provided budget exactly covers all possible deductions
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_3_exact_budget():

    # Print what is being tested
    print("Test Case 3: Exact Budget\n")

    # Create the budget amount
    budget = 435
    
    # Run the programming functions
    run_programming(budget)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_4_not_enough_budget
# Description:
# Tests what happens when the provided budget is not enough to cover all possible deductions
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_4_not_enough_budget():

    # Print what is being tested
    print("Test Case 4: Not Enough Budget\n")

    # Create the budget amount
    budget = 235
    
    # Run the programming functions
    run_programming(budget)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


###############################################################################################
# Test Function: test_case_5_too_much_budget
# Description:
# Tests what happens when the provided budget is more than the total cost of all possible deductions
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def test_case_5_too_much_budget():

    # Print what is being tested
    print("Test Case 5: Too Much Budget\n")

    # Create the budget amount
    budget = 550
    
    # Run the programming functions
    run_programming(budget)
    
    # Print an empty line
    print("\n")

    # Print a separator line
    print("=" * 80)

    # Print an empty line
    print("\n")


if __name__ == "__main__":
    test_case_1_invalid_budget()
    test_case_2_zero_budget()
    test_case_3_exact_budget()
    test_case_4_not_enough_budget()
    test_case_5_too_much_budget()
