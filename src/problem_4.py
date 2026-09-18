
###############################################################################################
# Imports
#
###############################################################################################
import time
import tracemalloc
import pulp


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
#                           - deductions (dictionary of all deductions with Implement/Cost/Benefit)
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
# Function: print_solution
# Description:
# Prints the solution in a clear, readable format in the 
# correct (original) deduction order.
#
# Input:    integer         The maximum budget
#           dictionary      The solution returned by dynamic_programming() or linear_programming()
#           list            The list of deduction names (original order)
#
# Output:   N/A             (Prints the solution to the console)
###############################################################################################
def print_solution(budget, solution, names):
    """
    Print the solution in a readable format, preserving the original deduction order.

    """

    # Print the maximum budget
    print(f"Maximum Budget: ${budget}B\n")

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

    # Print the Header
    print("Dynamic Programming Solution:\n")

    # Get the possible tax deductions
    tax_deductions = possible_tax_deductions()

    # Create a list of deduction names
    names = list(tax_deductions.keys())

    # Start a timer
    start_time = time.perf_counter()
        
    # Start memory allocation tracing
    tracemalloc.start()
    
    # Call the top-down solver starting at index 0
    solution = solve_dp_top_down(budget, tax_deductions, names, 0)
    
    # End the timer
    end_time = time.perf_counter()
        
    # Get the current and peak memory allocation
    memory_current, memory_peak = tracemalloc.get_traced_memory()
        
    # Stop memory allocation tracing
    tracemalloc.stop()
    
    # Calculate the length of time it took in milliseconds
    total_time = (end_time - start_time) * 1000
 
    # Print the time
    print(f"Time DP took: {total_time:.4f} ms ")
        
    # Print the memory usage
    print(f"DP had a peak memory usage of: {memory_peak} bytes\n")

    # Print the solution
    print_solution(budget, solution, names)

    # Return the solution
    return solution


###############################################################################################
# Function: solve_lp
# Description:
# Uses Linear Programming (PuLP) to determine which tax deductions should be implemented
# to maximise economic benefit while staying within the budget.
#
# Input:    integer         The maximum budget
#           dictionary      The dictionary containing the possible tax deductions
#           list            The list of deduction names (stable ordering)
#
# Output:   dictionary      The LP solution containing:
#                           - total_cost
#                           - total_benefit
#                           - deductions (dictionary of all deductions with Implement/Cost/Benefit)
###############################################################################################
def solve_lp(budget, tax_deductions, names):
    """
    Return the linear programming solution for the tax deduction problem.
    """

    # ---------------------------------------------------------------------------------
    # CREATE THE LP PROBLEM
    # ---------------------------------------------------------------------------------
    # Create a maximisation problem
    lp_problem = pulp.LpProblem("Tax_Deduction_Optimisation", pulp.LpMaximize)

    # ---------------------------------------------------------------------------------
    # CREATE DECISION VARIABLES
    # ---------------------------------------------------------------------------------
    # For each deduction, create a binary variable:
    # 1 = Implement the deduction
    # 0 = Do not implement the deduction
    x = {name: pulp.LpVariable(name, lowBound=0, upBound=1, cat=pulp.LpBinary)
         for name in names}

    # ---------------------------------------------------------------------------------
    # OBJECTIVE FUNCTION:
    # Maximise total benefit
    # ---------------------------------------------------------------------------------
    lp_problem += pulp.lpSum([tax_deductions[name]["benefit"] * x[name] for name in names])

    # ---------------------------------------------------------------------------------
    # BUDGET CONSTRAINT:
    # Total cost must not exceed the budget
    # ---------------------------------------------------------------------------------
    lp_problem += pulp.lpSum([tax_deductions[name]["cost"] * x[name] for name in names]) <= budget

    # ---------------------------------------------------------------------------------
    # SOLVE THE LP PROBLEM
    # ---------------------------------------------------------------------------------
    lp_problem.solve()

    status = pulp.LpStatus[lp_problem.status]

    if status != "Optimal":

        print(f"Warning: LP solver returned status '{status}'")

    # ---------------------------------------------------------------------------------
    # BUILD THE SOLUTION DICTIONARY (MATCHES DP FORMAT)
    # ---------------------------------------------------------------------------------
    solution = {
        "total_cost": 0,
        "total_benefit": 0,
        "deductions": {}
    }

    # Loop through each deduction and extract the LP decision
    for name in names:

        implemented = int(pulp.value(x[name]))  # 1 or 0

        cost = tax_deductions[name]["cost"] if implemented else 0

        benefit = tax_deductions[name]["benefit"] if implemented else 0

        # Add to the solution dictionary
        solution["deductions"][name] = {
            "Implement": "Implemented" if implemented else "Not Implemented",
            "Cost": cost,
            "Benefit": benefit
        }

        # Update totals
        solution["total_cost"] += cost

        solution["total_benefit"] += benefit

    # Return the LP solution
    return solution


###############################################################################################
# Function: linear_programming
# Description:
# Wrapper function that prepares the deduction list and calls the LP solver.
#
# Input:    integer         The maximum budget
# Output:   dictionary      The LP solution
###############################################################################################
def linear_programming(budget):
    """
    Return the linear programming solution.

    Gets the possible tax deductions and then calls the solve_lp function.
    """

    # Print the Header
    print("\nLinear Programming Solution:\n")

    # Get the possible tax deductions
    tax_deductions = possible_tax_deductions()

    # Create a list of deduction names
    names = list(tax_deductions.keys())

    # Start a timer
    start_time = time.perf_counter()
            
    # Start memory allocation tracing
    tracemalloc.start()
        
    # Solve using LP
    solution = solve_lp(budget, tax_deductions, names)
        
    # End the timer
    end_time = time.perf_counter()
            
    # Get the current and peak memory allocation
    memory_current, memory_peak = tracemalloc.get_traced_memory()
            
    # Stop memory allocation tracing
    tracemalloc.stop()
        
    # Calculate the length of time it took in milliseconds
    total_time = (end_time - start_time) * 1000
    
    # Print the time
    print(f"Time LP took: {total_time:.4f} ms ")
            
    # Print the memory usage
    print(f"LP had a peak memory usage of: {memory_peak} bytes\n")

    # Print the solution
    print_solution(budget, solution, names)

    return solution


###############################################################################################
# Function: run_programming
# Description:
# Wrapper function that runs each of the programming functions, one after the other 
# with the same provided budget.
#
# Input:    integer         The maximum budget
# Output:   N/A
###############################################################################################
def run_programming(budget):
    """
    Runs the dynamic programming function and then the linear programming function, 
    with the same budget.

    """
    # Validate that the budget is a number
    # If budget is not an integer or a float
    if not isinstance(budget, (int, float)):

        # Print an error message
        print("Error: Budget must be a numeric value.\n")

        # Return out of the program
        return
    
    # Run the dynamic programming
    dp_solution = dynamic_programming(budget)
    
    # Run the linear programming
    lp_solution = linear_programming(budget)


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
    Entry point for Problem 4.

        The function:
            - Calls the run_programming function with a budget amount

    """

    print("Program started.\n")

    # Run the programming
    run_programming(200)

    


if __name__ == "__main__":
    problem_4()