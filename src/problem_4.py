
###############################################################################################
# Imports
#
###############################################################################################
import math
import time
import tracemalloc


###############################################################################################
# Function: possible_tax_deductions
# Description:
# Provides a dictionary with the possible tax deductions.
#
# Input:    N/A
# Output:   dictionary      A dictionary of possible tax deductions
###############################################################################################
def possible_tax_deductions():
    """
    Return the possible tax deductions in a dictionary

    """
    # Create the dictionary
    tax_deductions = {
        "Mortgage Interest": {"cost": 85, "benefit": 110},
        "Charitable Giving": {"cost": 60, "benefit": 72},
        "Education Expenses": {"cost": 45, "benefit": 65},
        "Retirement Savings": {"cost": 70, "benefit": 95},
        "Healthcare Costs": {"cost": 55, "benefit": 80},
        "Child Tax Credits": {"cost": 40, "benefit": 65},
        "Small Business Investment": {"cost": 50, "benefit": 78},
        "Political Donations": {"cost": 30, "benefit": 45}
    }

    return tax_deductions


###############################################################################################
# Function: solve_dp_top_down
# Description:
# Uses top-down dynamic programming (memoised recursion) to determine which tax deductions
# should be implemented to maximise economic benefit while staying within the budget.
#
# Input:    integer         The remaining budget
#           dictionary      The dictionary containing the possible tax deductions
#           list            The list of deduction names (stable ordering)
#           integer         The index of the deduction currently being considered
#           dictionary      The memo dictionary (stores previously computed subproblems)
#
# Output:   dictionary      The dynamic programming solution containing:
#                           - total_cost
#                           - total_benefit
#                           - chosen (dictionary of all deductions with Implement/Cost/Benefit)
###############################################################################################
def solve_dp_top_down(budget, tax_deductions, names, index, memo = None):
    """
    Return the dynamic programming solution for the tax deduction problem
    using top-down memoised recursion.

    """
    # If the memo is None
    if memo is None:

        # Create the memo dictionary
        memo = {}

    # ---------------------------------------------------------------------------------
    # BASE CASE:
    # If index has reached the end of the names list, no more deductions to consider.
    # Return an empty solution. The recursion will fill this in as it unwinds.
    # ---------------------------------------------------------------------------------
    # If index equals the number of names
    if index == len(names):

        # Create the empty solution
        empty_solution = {
            "total_cost": 0,
            "total_benefit": 0,
            "deductions": {}    # Empty dictionary for recursion to populate
        }

        # return the empty solution
        return empty_solution

    # ---------------------------------------------------------------------------------
    # MEMO CHECK:
    # If this subproblem has already been solved, return the stored result.
    # ---------------------------------------------------------------------------------
    # Create the key
    key = (index, budget)

    # If the key is in the memo
    if key in memo:

        # Return the stored result
        return memo[key]

    # Get the current deduction name, cost and benefit
    current_name = names[index]
    current_cost = tax_deductions[current_name]["cost"]
    current_benefit = tax_deductions[current_name]["benefit"]

    # ---------------------------------------------------------------------------------
    # OPTION A: EXCLUDE the current deduction
    # ---------------------------------------------------------------------------------
    exclude_solution = solve_dp_top_down(
        budget,
        tax_deductions,
        names,
        index + 1,
        memo
    )

    # Create a *copy* of the exclude solution so that memo doesn't get mutated.
    exclude_solution = {
        "total_cost": exclude_solution["total_cost"],
        "total_benefit": exclude_solution["total_benefit"],
        "deductions": exclude_solution["deductions"].copy()
    }

    # Mark the current deduction as NOT implemented
    exclude_solution["deductions"][current_name] = {
        "Implement": "Not Implemented",
        "Cost": 0,
        "Benefit": 0
    }

    # ---------------------------------------------------------------------------------
    # OPTION B: INCLUDE the current deduction (only if budget allows)
    # ---------------------------------------------------------------------------------
    # Set include_solution to None
    include_solution = None

    # If the current cost is less than or equal to the budget
    if current_cost <= budget:

        # Include the solution
        include_solution = solve_dp_top_down(
            budget - current_cost,
            tax_deductions,
            names,
            index + 1,
            memo
        )

        # Copy to avoid mutating memo entries
        include_solution = {
            "total_cost": include_solution["total_cost"],
            "total_benefit": include_solution["total_benefit"],
            "deductions": include_solution["deductions"].copy()
        }

        # Mark the current deduction as IMPLEMENTED
        include_solution["deductions"][current_name] = {
            "Implement": "Implemented",
            "Cost": current_cost,
            "Benefit": current_benefit
        }

        # Update totals
        include_solution["total_cost"] += current_cost
        include_solution["total_benefit"] += current_benefit

    # ---------------------------------------------------------------------------------
    # CHOOSE THE BETTER OPTION
    # ---------------------------------------------------------------------------------
    # If include_solution isn't None and the total benefit for the include_solution is 
    # greater than the total benefit of the exclude_solution
    if include_solution is not None and include_solution["total_benefit"] > exclude_solution["total_benefit"]:

        # Set the include_solution as the best_solution
        best_solution = include_solution

    # Else
    else:

        # Set the exclude_solution as the best solution
        best_solution = exclude_solution

    # ---------------------------------------------------------------------------------
    # STORE IN MEMO AND RETURN
    # ---------------------------------------------------------------------------------
    # Store the best_solution into the memo
    memo[key] = {
        "total_cost": best_solution["total_cost"],
        "total_benefit": best_solution["total_benefit"],
        "deductions": best_solution["deductions"].copy()
    }

    # Return the best_solution
    return best_solution


###############################################################################################
# Function: print_dp_solution
# Description:
# Prints the dynamic programming solution in a clear, readable format in the 
# correct (original) deduction order.
#
# Input:    integer         The maximum budget
#           dictionary      The dynamic programming solution returned by dynamic_programming()
#           list            The list of deduction names (original order)
#
# Output:   N/A             (Prints the solution to the console)
###############################################################################################
def print_dp_solution(budget, solution, names):
    """
    Print the dynamic programming solution in a readable format.

    """

    # Print the maximum budget
    print(f"Maximum Budget: ${budget}B\n")

    # Print the header
    print("Dynamic Programming Solution:\n")

    # Get the deductions dictionary
    deductions = solution["deductions"]

    # Loop through each deduction and print its details
    for name in names:
        details = deductions[name]
        implement = details["Implement"]
        cost = details["Cost"]
        benefit = details["Benefit"]

        print(f"{name}: {implement} (Cost: ${cost}B, Benefit: ${benefit}B)")

    # Print the totals
    print(f"\nTotal cost: ${solution['total_cost']}B")
    print(f"Total benefit: ${solution['total_benefit']}B\n")


###############################################################################################
# Function: dynamic_programming
# Description:
# Wrapper function that prepares the deduction list and calls the top-down DP solver.
#
# Input:    integer         The maximum budget
# Output:   dictionary      The dynamic programming solution
###############################################################################################
def dynamic_programming(budget):
    """
    Return the dynamic programming solution.

    Gets the possible tax deducations and then calls the solve_dp_top_down function

    """
    # Get the possible tax deductions
    tax_deductions = possible_tax_deductions()

    # Create a list of deduction names
    names = list(tax_deductions.keys())

    # Call the top-down solver starting at index 0
    solution = solve_dp_top_down(budget, tax_deductions, names, 0)

    # Print the solution
    print_dp_solution(budget, solution, names)

    # Return the solution
    return solution





###############################################################################################
# Function: problem_4
# Description:
# Entry Point for running Problem 4
# 
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_4():
    """
    Entry point for Problem 5.

        The function:
            - Calls the dynamic_programming function with a budget amount

    """

    print("Program started.\n")

    # Runs the dynamic programming
    solution = dynamic_programming(200)

    


if __name__ == "__main__":
    problem_4()