

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
# Function: sax_transformation
# Description:
# Transforms a normalized series into a SAX letter string
#
# Input:    series      A normalized series of voice frequency values
# Output:   string      A string of SAX letters representing the series
###############################################################################################
def sax_transformation(series):
    """
    Transforms a normalized series into a SAX letter string.

    The function:

        - Maps each normalized value to a letter ('a'-'e') based on SAX breakpoints.
        - Combines all letters into a single string.

    Symbolic Aggregate approXimation (SAX) converts normalized numeric values into symbols
    using breakpoints that divide the Gaussian distribution into equal-sized regions.

    """

    # Create a list to hold the letters
    list_letters = []

    # For loop through the series
    for s in series:

        # If the value is less than -0.67
        if s < -0.67:

            # Add 'a' to the list of letters
            list_letters.append('a')

        # else if the value is between -0.67 and -0.22
        elif s >= -0.67 and s < -0.22:

            # Add 'b' to the list of letters
            list_letters.append('b')


        # else if the value is between -0.22 and 0.22
        elif s >= -0.22 and s < 0.22:
        
            # Add 'c' to the list of letters
            list_letters.append('c')

        # else if the value is between 0.22 and 0.67
        elif s >= 0.22 and s < 0.67:
                
            # Add 'd' to the list of letters
            list_letters.append('d')

        # Else it is greater than 0.67
        else:

            # Add 'e' to the list of letters
            list_letters.append('e')

    # Combine the letters in to a string
    letters = ''.join(list_letters)

    # Return the letters
    return letters





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