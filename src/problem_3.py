

###############################################################################################
# Imports
#
###############################################################################################
import math
import time
import tracemalloc


###############################################################################################
# Function: normalize
# Description:
# Performs z-score normalization on a series of voice numbers
#
# Input:    series      A series of voice numbers
# Output:   series      A normalized version of the series
###############################################################################################
def normalize(series):
    """
    Performs z-score normalization on a series of voice numbers

    The function:

        - Compute the mean
        - Compute the standard deviation
        - Uses the mean and standard deviation to normalize each value

    Normalization ensures the data has mean 0 and standard deviation 1, which is required 
    before applying the SAX transformation.

    """
    # Step 1: Compute the mean

    # Calculate the mean
    mean = sum(series) / len(series)

    # Step 2: Compute the standard deviation

    # Step 2-1: Compute differences from the mean
    # Create a differences list
    differences = []

    # For loop through the series
    for s in series:

        # Calculate the difference by subtracting the mean from the value
        diff = s - mean

        # Append the difference to the differences list
        differences.append(diff)

    # Step 2-2: Square the differences
    # Create a squared differences list
    differences_squared = []

    # For loop through the differences list
    for d in differences:

        # Calculate the squared difference by squaring the difference
        diff_sqr = d * d

        # Append the squared difference to the squared differences list
        differences_squared.append(diff_sqr)

    # Step 2-3: Compute the variance
    # Calculate the variance
    variance = sum(differences_squared) / len(series)

    # Step 2-4: Compute the standard deviation
    # Calculate the standard deviation
    std = variance ** 0.5

    # Step 3: Normalization - Update each value by subtracting the mean and then dividing by the standard deviation

    # Initialise a normalized series list
    series_normalized = []

    # For loop through the series
    for s in series:

        # Caculate it's new value
        new_value = (s - mean) / std

        # Append the new value to the normalized series list
        series_normalized.append(new_value)

    # Return the normalized series
    return series_normalized








###############################################################################################
# Function: problem_3
# Description:
# Entry Point for running Problem 3
# 
#
# Input:    N/A
# Output:   N/A
###############################################################################################
def problem_3():
    """
        main.py
        Entry point for the assignment.

        The function:
            - 
    """
    print("Program started.\n")



if __name__ == "__main__":
    problem_3()